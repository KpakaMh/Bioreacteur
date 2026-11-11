import pytest
from control.pid import PIDController
from control.sensors import Sensor

def test_sensor_noise_generation():
    sensor = Sensor(noise_std=0.02)
    true_val = 100.0
    readings = [sensor.read(true_val) for _ in range(20)]
    
    # Vérifie que les valeurs lues fluctuent autour de la vraie valeur
    assert all(r > 0 for r in readings)
    assert any(r != true_val for r in readings), "Le capteur doit introduire des variations légères."

def test_pid_corrective_action():
    # Consigne de pH = 7.0, mesure actuelle = 6.5 (trop acide)
    pid = PIDController(Kp=10.0, Ki=1.0, Kd=0.1, setpoint=7.0, output_limits=(0.0, 50.0))
    output = pid.compute(measurement=6.5, dt=0.1)
    
    assert output > 0.0, "Le PID doit déclencher une addition de base (output > 0)."

def test_pid_saturation_limits():
    # Test de la limite maximale de commande (Anti-windup)
    pid = PIDController(Kp=100.0, Ki=10.0, Kd=0.0, setpoint=10.0, output_limits=(0.0, 100.0))
    output = pid.compute(measurement=0.0, dt=1.0)
    
    assert output == 100.0, "La commande ne doit pas dépasser la limite maximale définie."