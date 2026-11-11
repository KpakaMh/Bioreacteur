from core.state import BioreactorState
from core.kinetics import KineticModel
from core.solver import ODESolver

class BioreactorTwinEngine:
    """Moteur d'orchestration temporelle du jumeau virtuel."""
    
    def __init__(self, initial_state: BioreactorState = None, model: KineticModel = None):
        self.state = initial_state or BioreactorState()
        self.model = model or KineticModel()
        self.solver = ODESolver(self.model)

    def step(self, dt: float = 0.1, F_in: float = 0.0, S_in: float = 0.0, RPM: float = 300.0) -> BioreactorState:
        """Fait avancer la simulation de dt heures avec les consignes actuelles."""
        y0 = [
            self.state.biomass,
            self.state.substrate,
            self.state.product,
            self.state.dissolved_o2,
            self.state.volume
        ]
        
        t_span = (self.state.time, self.state.time + dt)
        y_next = self.solver.step(y0, t_span, F_in=F_in, S_in=S_in, RPM=RPM)
        
        # Mise à jour de l'état du bioréacteur (borné à 0 pour éviter les valeurs négatives)
        self.state.time += dt
        self.state.biomass = max(0.0, y_next[0])
        self.state.substrate = max(0.0, y_next[1])
        self.state.product = max(0.0, y_next[2])
        self.state.dissolved_o2 = max(0.0, y_next[3])
        self.state.volume = max(0.0, y_next[4])
        self.state.agitation = RPM

        return self.state