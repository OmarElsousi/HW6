class VoltageSource:
    """
    A class representing a voltage source in a circuit.

    Attributes:
    - Voltage (float): The voltage value.
    - Name (str): The name of the voltage source.
    - Type (str): The type of voltage source (default is "DC").
    """

    def __init__(self, V=12.0, name='ab'):
        """
        Initializes a voltage source with a given voltage and name.

        Parameters:
        - V (float, optional): Voltage in volts (default is 12.0).
        - name (str, optional): Name of the voltage source (default is 'ab').
        """
        self.Voltage = V  # Sets voltage value
        self.Name = name  # Sets name of the source
        self.Type = "DC"  # Default to DC source
