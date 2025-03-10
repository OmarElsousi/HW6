class Resistor:
    """
    A class representing an electrical resistor.

    Attributes:
    - Resistance (float): The resistance value in ohms.
    - Current (float): The current flowing through the resistor in amps.
    - Name (str): The name of the resistor, typically based on connected node names.
    - V (float): The voltage drop across the resistor.
    """

    def __init__(self, R=1.0, i=0.0, name='ab'):
        """
        Initializes a resistor with a given resistance, current, and name.

        Parameters:
        - R (float, optional): Resistance in ohms (default is 1.0).
        - i (float, optional): Current in amps (default is 0.0).
        - name (str, optional): Name of the resistor (default is 'ab').
        """
        self.Resistance = R  # Stores the resistance value
        self.Current = i  # Stores the current value
        self.Name = name  # Stores the resistor's name
        self.V = self.DeltaV()  # Computes initial voltage drop

    def DeltaV(self):
        """
        Calculates and updates the voltage drop across the resistor using Ohm's Law (V = IR).

        Returns:
        - float: The voltage drop across the resistor.
        """
        self.V = self.Current * self.Resistance  # Ohm's Law: V = IR
        return self.V
