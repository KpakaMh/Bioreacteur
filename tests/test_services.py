import pytest
from core.state import BioreactorState
from services.logger import SimulationLogger
from services.exporter import DataExporter

def test_logger_accumulates_data():
    logger = SimulationLogger()
    state1 = BioreactorState(time=0.0, biomass=0.5)
    state2 = BioreactorState(time=0.1, biomass=0.55)
    
    logger.log(state1)
    logger.log(state2)
    
    df = logger.to_dataframe()
    assert logger.count == 2
    assert len(df) == 2
    assert df.loc[1, "biomass"] == 0.55

def test_exporter_csv_and_json(tmp_path):
    logger = SimulationLogger()
    logger.log(BioreactorState(time=0.0, biomass=0.5))
    df = logger.to_dataframe()
    
    csv_file = tmp_path / "run_test.csv"
    json_file = tmp_path / "run_test.json"
    
    DataExporter.export_to_csv(df, str(csv_file))
    DataExporter.export_to_json(df, str(json_file))
    
    assert csv_file.exists()
    assert json_file.exists()