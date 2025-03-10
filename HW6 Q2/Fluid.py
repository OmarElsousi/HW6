class Fluid:
    """
    Represents a fluid with properties such as dynamic viscosity and density.
    Default values correspond to water at room temperature.
    """

    def __init__(self, mu=0.00089, rho=1000):
        """
        Initializes the Fluid object with given properties.

        :param mu: Dynamic viscosity in Pa·s (kg/(m·s)). Default is 0.00089 for water.
        :param rho: Density in kg/m³. Default is 1000 for water.
        """
        self.mu = mu  # Store dynamic viscosity
        self.rho = rho  # Store density
        self.nu = self.mu / self.rho  # Compute and store kinematic viscosity (m²/s)