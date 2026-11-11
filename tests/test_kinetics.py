import pytest
from core.kinetics import KineticModel

def test_growth_rate_zero_substrate():
    model = KineticModel()
    mu = model.compute_growth_rate(S=0.0, DO=100.0)
    assert mu == 0.0, "Le taux de croissance doit être strictement nul sans substrat."

def test_growth_rate_nominal():
    model = KineticModel()
    mu = model.compute_growth_rate(S=10.0, DO=100.0)
    assert 0.0 < mu < model.params.mu_max, "Le taux de croissance doit être positif et inférieur à mu_max."

def test_derivatives_batch_mode():
    model = KineticModel()
    # État initial y0 = [X, S, P, DO, V]
    y0 = [0.5, 20.0, 0.0, 100.0, 2.0]
    derivatives = model.compute_derivatives(t=0.0, y=y0, F_in=0.0, RPM=300.0)
    
    dXdt, dSdt, dPdt, dDOdt, dVdt = derivatives
    assert dXdt > 0, "La biomasse doit augmenter en début de culture."
    assert dSdt < 0, "Le substrat doit être consommé."
    assert dVdt == 0, "Le volume doit rester constant sans alimentation (Batch)."