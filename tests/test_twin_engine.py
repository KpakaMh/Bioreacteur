import pytest
from core.twin_engine import BioreactorTwinEngine

def test_simulation_step_progresses_time():
    engine = BioreactorTwinEngine()
    initial_time = engine.state.time
    
    # Simuler un pas de 1.0 heure
    new_state = engine.step(dt=1.0)
    
    assert new_state.time == initial_time + 1.0
    assert new_state.biomass > 0.5, "La biomasse doit augmenter après 1h."
    assert new_state.substrate < 20.0, "Le substrat doit avoir diminué après 1h."

def test_fed_batch_volume_increase():
    engine = BioreactorTwinEngine()
    initial_volume = engine.state.volume
    
    # Simuler 1h avec une alimentation F_in = 0.2 L/h
    new_state = engine.step(dt=1.0, F_in=0.2, S_in=100.0)
    
    assert pytest.approx(new_state.volume, 0.01) == initial_volume + 0.2