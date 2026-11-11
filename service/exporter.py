from pathlib import Path
import pandas as pd

class DataExporter:
    """Gère l'exportation des séries temporelles vers le disque."""
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, filepath: str) -> str:
        """Exporte le DataFrame au format CSV."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)
        return str(path.resolve())

    @staticmethod
    def export_to_json(df: pd.DataFrame, filepath: str) -> str:
        """Exporte le DataFrame au format JSON."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_json(path, orient="records", indent=2)
        return str(path.resolve())