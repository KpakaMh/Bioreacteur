from dataclasses import dataclass
from core.state import BioreactorState

@dataclass
class KineticParameters:
    """Paramètres cinétiques biologiques et constantes de transfert."""
    mu_max: float = 0.45      # Taux de croissance spécifique max (h^-1)
    K_s: float = 0.5          # Constante d'affinité pour le glucose (g/L)
    K_o2: float = 5.0         # Constante d'affinité pour l'O2 (%)
    Y_xs: float = 0.5         # Rendement de conversion Biomasse/Substrat (g/g)
    alpha: float = 0.1        # Synthèse produit associée à la croissance (g/g)
    beta: float = 0.02        # Synthèse produit associée au maintien (g/g·h)
    K_d: float = 0.01         # Taux de mortalité cellulaire (h^-1)
    q_o2_max: float = 0.2     # Consommation spécifique max d'O2 (mmol/g·h)

class KineticModel:
    """Modèle mathématique calculant les dérivées temporelles dy/dt."""
    
    def __init__(self, params: KineticParameters = None):
        self.params = params or KineticParameters()

    def compute_growth_rate(self, S: float, DO: float) -> float:
        """Calcul du taux de croissance mu avec double limitation (Monod)."""
        if S <= 0 or DO <= 0:
            return 0.0
        mu_s = S / (self.params.K_s + S)
        mu_o2 = DO / (self.params.K_o2 + DO)
        return self.params.mu_max * mu_s * mu_o2

    def compute_kLa(self, RPM: float) -> float:
        """Estimation empirique du coefficient de transfert d'oxygène (kLa)."""
        # kLa augmente avec la vitesse d'agitation (RPM)
        return 5.0 + 0.05 * (RPM ** 1.1)

    def compute_derivatives(self, t: float, y: list, F_in: float = 0.0, S_in: float = 0.0, RPM: float = 300.0) -> list:
        """
        Calcule le système d'ODE pour le solveur scipy.
        Vecteur d'état y = [Biomasse (X), Substrat (S), Produit (P), Oxygène (DO), Volume (V)]
        """
        X, S, P, DO, V = max(0.0, y[0]), max(0.0, y[1]), max(0.0, y[2]), max(0.0, y[3]), max(0.0, y[4])
        
        # 1. Taux de croissance instantané
        mu = self.compute_growth_rate(S, DO)
        kLa = self.compute_kLa(RPM)
        
        # 2. Dérivées (dX/dt, dS/dt, dP/dt, dDO/dt, dV/dt)
        dXdt = (mu - self.params.K_d) * X - (F_in / V) * X
        dSdt = -(1.0 / self.params.Y_xs) * mu * X + (F_in / V) * (S_in - S)
        dPdt = (self.params.alpha * mu + self.params.beta) * X - (F_in / V) * P
        
        # Consommation O2 vs Reconstitution via kLa
        q_o2 = self.params.q_o2_max * (S / (self.params.K_s + S))
        dDOdt = kLa * (100.0 - DO) - (q_o2 * X * 10.0)
        
        dVdt = F_in

        return [dXdt, dSdt, dPdt, dDOdt, dVdt]