import random

class Sensor:
    """Simule une sonde physique avec du bruit de mesure gaussien."""
    
    def __init__(self, noise_std: float = 0.01):
        self.noise_std = noise_std  # Écart-type du bruit (1% par défaut)

    def read(self, true_value: float) -> float:
        """Retourne la valeur mesurée injectée d'un bruit instrumental."""
        if true_value <= 0:
            return 0.0
        noise = random.gauss(0, self.noise_std * true_value)
        return max(0.0, float(true_value + noise))