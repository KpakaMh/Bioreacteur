class PIDController:
    """Régulateur Proportionnel-Intégral-Dérivé pour le contrôle en boucle fermée."""
    
    def __init__(self, Kp: float, Ki: float, Kd: float, setpoint: float, output_limits: tuple = (0.0, 100.0)):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.min_output, self.max_output = output_limits
        
        self._integral = 0.0
        self._prev_error = 0.0

    def compute(self, measurement: float, dt: float) -> float:
        """Calcule la commande U(t) en fonction de l'écart à la consigne."""
        error = self.setpoint - measurement
        
        # Terme Intégral avec accumulation
        self._integral += error * dt
        
        # Terme Dérivé
        derivative = (error - self._prev_error) / dt if dt > 0 else 0.0
        
        # Calcul de la sortie brute
        output = (self.Kp * error) + (self.Ki * self._integral) + (self.Kd * derivative)
        
        # Anti-windup (saturation des limites de sortie)
        output = max(self.min_output, min(self.max_output, output))
        self._prev_error = error
        
        return output

    def reset(self):
        """Réinitialise la mémoire intégrale et l'erreur précédente."""
        self._integral = 0.0
        self._prev_error = 0.0