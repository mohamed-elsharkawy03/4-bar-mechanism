import numpy as np
from scipy.optimize import fsolve

class FourBarMechanism:
    def __init__(self, a, b, c, d):
        """
        Initialize with link lengths.
        a: crank length
        b: coupler length
        c: rocker length
        d: ground length
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def position_analysis(self, theta2):
        """
        Solve for theta3 and theta4 given theta2.
        Returns: theta3, theta4
        """
        def equations(vars):
            theta3, theta4 = vars
            eq1 = self.a * np.cos(theta2) + self.b * np.cos(theta3) - self.c * np.cos(theta4) - self.d
            eq2 = self.a * np.sin(theta2) + self.b * np.sin(theta3) - self.c * np.sin(theta4)
            return [eq1, eq2]
        
        # Initial guess: slightly offset from theta2
        initial_guess = [theta2 + 0.1, theta2 + 0.1]
        sol = fsolve(equations, initial_guess)
        theta3, theta4 = sol
        return theta3, theta4

    def velocity_analysis(self, theta2, omega2, theta3, theta4):
        """
        Solve for omega3 and omega4 given theta2, omega2, and positions.
        Returns: omega3, omega4
        """
        # Coefficients from differentiated loop equations
        A11 = -self.b * np.sin(theta3)
        A12 = self.c * np.sin(theta4)
        A21 = self.b * np.cos(theta3)
        A22 = -self.c * np.cos(theta4)
        
        B1 = -self.a * omega2 * np.sin(theta2)
        B2 = self.a * omega2 * np.cos(theta2)
        
        # Matrix form: A * [omega3, omega4]^T = B
        A = np.array([[A11, A12], [A21, A22]])
        B = np.array([B1, B2])
        
        omega3, omega4 = np.linalg.solve(A, B)
        return omega3, omega4

    def acceleration_analysis(self, theta2, omega2, alpha2, theta3, theta4, omega3, omega4):
        """
        Solve for alpha3 and alpha4 given theta2, omega2, alpha2, positions, and velocities.
        Returns: alpha3, alpha4
        """
        # Second derivatives of loop equations
        A11 = -self.b * np.sin(theta3)
        A12 = self.c * np.sin(theta4)
        A21 = self.b * np.cos(theta3)
        A22 = -self.c * np.cos(theta4)
        
        # Right-hand side includes accelerations and velocity terms
        B1 = -self.a * (alpha2 * np.sin(theta2) + omega2**2 * np.cos(theta2)) + \
             self.b * omega3**2 * np.cos(theta3) - self.c * omega4**2 * np.cos(theta4)
        B2 = self.a * (alpha2 * np.cos(theta2) - omega2**2 * np.sin(theta2)) - \
             self.b * omega3**2 * np.sin(theta3) + self.c * omega4**2 * np.sin(theta4)
        
        A = np.array([[A11, A12], [A21, A22]])
        B = np.array([B1, B2])
        
        alpha3, alpha4 = np.linalg.solve(A, B)
        return alpha3, alpha4

    def analyze(self, theta2, omega2=1.0, alpha2=0.0):
        """
        Full analysis: position, velocity, acceleration.
        Returns: dict with theta3, theta4, omega3, omega4, alpha3, alpha4
        """
        theta3, theta4 = self.position_analysis(theta2)
        omega3, omega4 = self.velocity_analysis(theta2, omega2, theta3, theta4)
        alpha3, alpha4 = self.acceleration_analysis(theta2, omega2, alpha2, theta3, theta4, omega3, omega4)
        
        return {
            'theta3': theta3,
            'theta4': theta4,
            'omega3': omega3,
            'omega4': omega4,
            'alpha3': alpha3,
            'alpha4': alpha4
        }

# Example usage
if __name__ == "__main__":
    # Define a four-bar mechanism (example lengths)
    mechanism = FourBarMechanism(a=1.0, b=2.0, c=1.5, d=2.5)
    
    # Input: crank angle (radians), angular velocity, angular acceleration
    theta2 = np.pi / 4  # 45 degrees
    omega2 = 1.0  # rad/s
    alpha2 = 0.0  # rad/s²
    
    # Perform analysis
    results = mechanism.analyze(theta2, omega2, alpha2)
    
    # Print results
    print("Four-Bar Mechanism Analysis:")
    print(f"Input: θ₂ = {theta2:.3f} rad, ω₂ = {omega2} rad/s, α₂ = {alpha2} rad/s²")
    print(f"θ₃ = {results['theta3']:.3f} rad")
    print(f"θ₄ = {results['theta4']:.3f} rad")
    print(f"ω₃ = {results['omega3']:.3f} rad/s")
    print(f"ω₄ = {results['omega4']:.3f} rad/s")
    print(f"α₃ = {results['alpha3']:.3f} rad/s²")
    print(f"α₄ = {results['alpha4']:.3f} rad/s²")
