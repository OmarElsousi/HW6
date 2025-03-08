from Steam_stem import steam  # Make sure this matches your actual filename or import statement
# If your file is named "Steam_stem.py," then do:
# from Steam_stem import steam

class rankine():
    def __init__(self, p_low=8, p_high=8000, t_high=None, name='Rankine Cycle'):
        '''
        Constructor for rankine power cycle.  If t_high is not specified, State 1
        is assigned x=1 (saturated steam @ p_high).  Otherwise, we use t_high for superheat.
        :param p_low: the low pressure isobar for the cycle in kPa
        :param p_high: the high pressure isobar for the cycle in kPa
        :param t_high: optional temperature for State1 (turbine inlet) in degrees C
        :param name: a convenient name
        '''
        self.p_low = p_low
        self.p_high = p_high
        self.t_high = t_high
        self.name = name

        # These will be computed after calling calc_efficiency()
        self.efficiency = None
        self.turbine_work = 0
        self.pump_work = 0
        self.heat_added = 0

        # The four principal states of the Rankine cycle
        self.state1 = None
        self.state2 = None
        self.state3 = None
        self.state4 = None

    def calc_efficiency(self):
        # -------------------------------------------------
        # 1) State 1: Turbine Inlet
        # -------------------------------------------------
        if self.t_high is None:
            # FILLED IN MISSING CODE: saturated steam at p_high, x=1
            self.state1 = steam(self.p_high, x=1.0, name='Turbine Inlet')
        else:
            # FILLED IN MISSING CODE: superheated steam at p_high, T = t_high
            self.state1 = steam(self.p_high, T=self.t_high, name='Turbine Inlet')

        # -------------------------------------------------
        # 2) State 2: Turbine Exit (isentropic expansion to p_low)
        # -------------------------------------------------
        # FILLED IN MISSING CODE: same entropy as state1, pressure = p_low
        self.state2 = steam(self.p_low, s=self.state1.s, name='Turbine Exit')

        # -------------------------------------------------
        # 3) State 3: Pump Inlet (saturated liquid at p_low)
        # -------------------------------------------------
        # FILLED IN MISSING CODE: x=0, saturated liquid at p_low
        self.state3 = steam(self.p_low, x=0.0, name='Pump Inlet')

        # -------------------------------------------------
        # 4) State 4: Pump Exit (pumped up to p_high)
        # -------------------------------------------------
        # We approximate the final state as compressed liquid with same s as state3,
        # but do a slight correction to enthalpy: h4 = h3 + v3*(p_high - p_low)
        self.state4 = steam(self.p_high, s=self.state3.s, name='Pump Exit')
        self.state4.h = self.state3.h + self.state3.v * (self.p_high - self.p_low)

        # -------------------------------------------------
        # Work & Heat Transfers
        # -------------------------------------------------
        # FILLED IN MISSING CODE:
        # Turbine work (kJ/kg) = h1 - h2
        self.turbine_work = self.state1.h - self.state2.h

        # Pump work (kJ/kg) = h4 - h3
        self.pump_work = self.state4.h - self.state3.h

        # Heat added in the boiler (kJ/kg) = h1 - h4
        self.heat_added = self.state1.h - self.state4.h

        # Overall efficiency (in %) = (turbine_work - pump_work)/heat_added * 100
        self.efficiency = 100.0 * (self.turbine_work - self.pump_work) / self.heat_added

        return self.efficiency

    def print_summary(self):
        # If efficiency isn’t calculated yet, do it now:
        if self.efficiency is None:
            self.calc_efficiency()

        print('Cycle Summary for:', self.name)
        print('\tEfficiency: {:0.3f}%'.format(self.efficiency))
        print('\tTurbine Work: {:0.3f} kJ/kg'.format(self.turbine_work))
        print('\tPump Work: {:0.3f} kJ/kg'.format(self.pump_work))
        print('\tHeat Added: {:0.3f} kJ/kg'.format(self.heat_added))

        self.state1.print()
        self.state2.print()
        self.state3.print()
        self.state4.print()

def main():
    # FILLED IN MISSING CODE: Instantiate a Rankine object to test it
    # Example: 8 kPa (condenser), 8000 kPa (boiler), t_high=500°C
    rankine1 = rankine(p_low=8, p_high=8000, t_high=501.5, name='Test Rankine Cycle')

    eff = rankine1.calc_efficiency()
    print("Efficiency: {:0.2f}%".format(eff))
    print()
    rankine1.print_summary()

if __name__=="__main__":
    main()
