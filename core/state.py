from dataclasses import dataclass #this commmand import data

@dataclass
class BioreactorState: # class defined
    """Représente l'état instantané des variables physico-chimiques et biologiques du bioréacteur."""
    time: float = 0.0          # Temps de culture (heures)
    biomass: float = 0.5       # X : Biomasse (g/L)
    substrate: float = 20.0    # S : Glucose / Substrat (g/L)
    product: float = 0.0       # P : Protéine d'intérêt / Anticorps (g/L)
    dissolved_o2: float = 100.0# DO : Oxygène dissous (% saturation)
    volume: float = 2.0        # V : Volume utile (L)
    temperature: float = 37.0  # T : Température (°C)
    ph: float = 7.0            # pH : Potentiel d'hydrogène
    agitation: float = 300.0   # RPM : Vitesse de l'hélice