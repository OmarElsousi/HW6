from Steam_stem import steam  # Ensure correct import of steam properties class


class Rankine:
    """
    Represents a Rankine power cycle for thermodynamic analysis.
    This class calculates efficiency, work, and heat transfer for the cycle.
    """

    def __init__(self, p_low=8, p_high=8000, t_high=None, name='Rankine Cycle'):
        """
        Initializes a Rankine cycle with specified pressure conditions and optional turbine inlet temperature.

        :param p_low: Low-pressure side of the cycle in kPa (default: 8 kPa)
        :param p_high: High-pressure side of the cycle in kPa (default: 8000 kPa)
        :param t_high: Optional temperature for turbine inlet in °C. If None, assumes saturated vapor.
        :param name: A string name for identifying the cycle.
        """
        self.p_low = p_low
        self.p_high = p_high
        self.t_high = t_high
        self.name = name

        # Properties initialized later in calc_efficiency()
        self.efficiency = None
        self.turbine_work = 0
        self.pump_work = 0
        self.heat_added = 0

        # Thermodynamic states (initialized later)
        self.state1 = None
        self.state2 = None
        self.state3 = None
        self.state4 = None

    def calc_efficiency(self):
        """
        Calculates the efficiency of the Rankine cycle using thermodynamic principles.
        Computes enthalpies at key states and determines net work and heat added.

        :return: Efficiency of the cycle as a percentage.
        """
        # State 1: Turbine Inlet
        if self.t_high is None:
            self.state1 = steam(self.p_high, x=1.0, name='Turbine Inlet')  # Saturated steam
        else:
            self.state1 = steam(self.p_high, T=self.t_high, name='Turbine Inlet')  # Superheated steam

        # State 2: Turbine Exit (isentropic expansion to p_low)
        self.state2 = steam(self.p_low, s=self.state1.s, name='Turbine Exit')

        # State 3: Pump Inlet (saturated liquid at p_low)
        self.state3 = steam(self.p_low, x=0.0, name='Pump Inlet')

        # State 4: Pump Exit (compressed liquid at p_high)
        self.state4 = steam(self.p_high, s=self.state3.s, name='Pump Exit')
        self.state4.h = self.state3.h + self.state3.v * (self.p_high - self.p_low)  # Approximate enthalpy

        # Work and heat calculations
        self.turbine_work = self.state1.h - self.state2.h
        self.pump_work = self.state4.h - self.state3.h
        self.heat_added = self.state1.h - self.state4.h

        # Efficiency calculation
        self.efficiency = 100.0 * (self.turbine_work - self.pump_work) / self.heat_added
        return self.efficiency

    def print_summary(self):
        """
        Prints a summary of the Rankine cycle, including efficiency, work, and state properties.
        """
        if self.efficiency is None:
            self.calc_efficiency()

        print(f'Cycle Summary for: {self.name}')
        print(f'\tEfficiency: {self.efficiency:.3f}%')
        print(f'\tTurbine Work: {self.turbine_work:.3f} kJ/kg')
        print(f'\tPump Work: {self.pump_work:.3f} kJ/kg')
        print(f'\tHeat Added: {self.heat_added:.3f} kJ/kg')

        self.state1.print()
        self.state2.print()
        self.state3.print()
        self.state4.print()


def main():
    """
    Runs a test case of the Rankine cycle and prints results.
    """
    print("Testing Rankine Cycle Calculation")
    rankine1 = Rankine(p_low=8, p_high=8000, t_high=501.5, name='Test Rankine Cycle')
    eff = rankine1.calc_efficiency()
    print(f"Efficiency: {eff:.2f}%\n")
    rankine1.print_summary()


if __name__ == "__main__":
    main()
