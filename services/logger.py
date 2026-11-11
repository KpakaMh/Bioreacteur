import pandas as pd
from core.state import BioreactorState

class SimulationLogger:
    """Enregistre et stocke les états successifs du bioréacteur sous forme de séries temporelles."""
    
    def __init__(self):
        self._history = []

    def log(self, state: BioreactorState):
        """Ajoute l'état instantané dans l'historique."""
        self._history.append({
            "time": state.time,
            "biomass": state.biomass,
            "substrate": state.substrate,
            "product": state.product,
            "dissolved_o2": state.dissolved_o2,
            "volume": state.volume,
            "temperature": state.temperature,
            "ph": state.ph,
            "agitation": state.agitation
        })

    def to_dataframe(self) -> pd.DataFrame:
        """Convertit l'historique en DataFrame Pandas."""
        return pd.DataFrame(self._history)

    def clear(self):
        """Réinitialise l'historique."""
        self._history.clear()

    @property
    def count(self) -> int:
        return len(self._history)