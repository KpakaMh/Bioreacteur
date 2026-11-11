from scipy.integrate import solve_ivp
from core.kinetics import KineticModel

class ODESolver:
    """Solveur numérique basé sur scipy.integrate.solve_ivp."""
    
    def __init__(self, kinetic_model: KineticModel):
        self.model = kinetic_model

    def step(self, y0: list, t_span: tuple, F_in: float = 0.0, S_in: float = 0.0, RPM: float = 300.0) -> list:
        """
        Intègre le système d'équations différentielles sur l'intervalle t_span = (t_start, t_end).
        Retourne le nouveau vecteur d'état y à la fin de l'intervalle.
        """
        sol = solve_ivp(
            fun=lambda t, y: self.model.compute_derivatives(t, y, F_in, S_in, RPM),
            t_span=t_span,
            y0=y0,
            method='RK45'
        )
        # Extraire le dernier état calculé par le solveur
        return [float(val) for val in sol.y[:, -1]]