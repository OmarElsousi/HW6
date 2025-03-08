# region imports
import numpy as np
from scipy.interpolate import griddata
# endregion

# region class definitions
class steam():
    """
    The steam class is used to find thermodynamic properties of steam along an isobar.
    The constructor requires pressure in kPa and one more property (T, x, v, h, or s).
    """

    def __init__(self, pressure, T=None, x=None, v=None, h=None, s=None, name=None):
        '''
        :param pressure: pressure in kPa
        :param T: Temperature in degrees C
        :param x: quality of steam x=1 is saturated vapor, x=0 is saturated liquid
        :param v: specific volume in m^3/kg
        :param h: specific enthalpy in kJ/kg
        :param s: specific entropy in kJ/(kg*K)
        :param name: a convenient identifier
        '''
        self.p = pressure  # kPa
        self.T = T
        self.x = x
        self.v = v
        self.h = h
        self.s = s
        self.name = name

        # Will get set to 'Saturated' or 'Superheated' (or possibly subcooled)
        self.region = None

        # If no second property is given, there's nothing to solve for
        if (T is None and x is None and v is None and h is None and s is None):
            return
        else:
            self.calc()

    def calc(self):
        '''
        1) Load steam tables for saturation & superheat.
        2) Identify which second property is known.
        3) Decide if the state is saturated (two-phase) or superheated.
        4) Interpolate needed properties.
        '''
        # -------------------------------------------------------
        # 1) Read in the thermodynamic data from text files
        # -------------------------------------------------------
        # A) Saturated table: columns (T [°C], P [bar], hf, hg, sf, sg, vf, vg)
        #    We'll convert bar -> bar, or just keep as bar since we do Pbar = p/100
        #    and we’ll pass that to griddata.
        data_sat = np.loadtxt('sat_water_table.txt', skiprows=1)
        # Adjust 'delimiter=' if needed based on how your file is formatted
        ts_all = data_sat[:, 0]
        ps_all = data_sat[:, 1]
        hfs_all = data_sat[:, 2]
        hgs_all = data_sat[:, 3]
        sfs_all = data_sat[:, 4]
        sgs_all = data_sat[:, 5]
        vfs_all = data_sat[:, 6]
        vgs_all = data_sat[:, 7]

        # B) Superheated table: columns [temp, h, s, p kpa]
        #    We’ll read them all into arrays.
        data_sh = np.loadtxt('superheated_water_table.txt', skiprows=1)
        tsh_all = data_sh[:, 0]
        hsh_all = data_sh[:, 1]
        ssh_all = data_sh[:, 2]
        psh_all = data_sh[:, 3]

        # Prepare for interpolation with griddata. We'll interpret (p, T) => h or s, etc.
        # Or (p, h) => T or s, etc., depending on the usage below.

        # For the saturated portion, we only need 1D interpolation by p in bar.
        # We’ll convert p (kPa) to bar:
        Pbar = self.p / 100.0

        # Interpolate the saturated properties at this pressure
        # griddata wants points, values, and the new point.
        # But since we’re just using 1D, we can do:
        Tsat = float(griddata((ps_all,), ts_all, (Pbar,)))
        hf = float(griddata((ps_all,), hfs_all, (Pbar,)))
        hg = float(griddata((ps_all,), hgs_all, (Pbar,)))
        sf = float(griddata((ps_all,), sfs_all, (Pbar,)))
        sg = float(griddata((ps_all,), sgs_all, (Pbar,)))
        vf = float(griddata((ps_all,), vfs_all, (Pbar,)))
        vg = float(griddata((ps_all,), vgs_all, (Pbar,)))

        # Store a few of these for reference (optional):
        self.hf = hf
        self.hg = hg
        self.sf = sf
        self.sg = sg
        self.vf = vf
        self.vg = vg
        # -------------------------------------------------------

        # Ideal gas constant for water vapor (approx):
        R = 8.314 / (18/1000)  # J/(mol*K) / (kg/mol) => ~461.9 J/(kg*K)
        # We'll use it if we guess v in superheat region: v = R*T / (p * 1000)...

        # 2) Identify which second property is known:
        #    T, x, h, s, or v
        # 3) Decide saturated vs. superheated
        # 4) Interpolate as needed

        if self.T is not None:
            # Temperature-based
            if self.T > Tsat:
                # => Superheated region
                self.region = 'Superheated'
                # We can interpolate h, s from (T, p) = (temp, psh_all)
                # “points” in 2D: (tsh_all, psh_all)
                # Then "values" could be hsh_all or ssh_all
                self.h = float(griddata((tsh_all, psh_all), hsh_all, (self.T, self.p)))
                self.s = float(griddata((tsh_all, psh_all), ssh_all, (self.T, self.p)))
                self.x = 1.0  # indicates vapor
                # Approximate v from ideal gas if needed:
                TK = self.T + 273.15
                self.v = R * TK / (self.p * 1000.0)  # p in kPa => multiply by 1000 => Pa
            else:
                # => Saturated or two-phase
                self.region = 'Saturated'
                self.x = 1.0 if abs(self.T - Tsat) < 0.01 else (self.T - Tsat)*0  # or assume x=1 if T==Tsat
                self.T = Tsat
                self.h = hf + self.x * (hg - hf)
                self.s = sf + self.x * (sg - sf)
                self.v = vf + self.x * (vg - vf)

        elif self.x is not None:
            # Quality-based => saturated region
            self.region = 'Saturated'
            self.T = Tsat
            self.h = hf + self.x * (hg - hf)
            self.s = sf + self.x * (sg - sf)
            self.v = vf + self.x * (vg - vf)

        elif self.h is not None:
            # Enthalpy-based
            # First try to see if h is <= hg => saturated region
            self.x = (self.h - hf) / (hg - hf)
            if self.x <= 1.0:
                # => saturated mixture
                self.region = 'Saturated'
                self.T = Tsat
                self.s = sf + self.x * (sg - sf)
                self.v = vf + self.x * (vg - vf)
            else:
                # => superheated
                self.region = 'Superheated'
                # We have (p, h) => find T, s from superheat data
                self.T = float(griddata((hsh_all, psh_all), tsh_all, (self.h, self.p)))
                self.s = float(griddata((hsh_all, psh_all), ssh_all, (self.h, self.p)))
                self.x = 1.0
                # approximate v with ideal gas
                TK = self.T + 273.15
                self.v = R * TK / (self.p * 1000.0)

        elif self.s is not None:
            # Entropy-based
            self.x = (self.s - sf) / (sg - sf)
            if self.x <= 1.0:
                # => saturated mixture
                self.region = 'Saturated'
                self.T = Tsat
                self.h = hf + self.x * (hg - hf)
                self.v = vf + self.x * (vg - vf)
            else:
                # => superheated
                self.region = 'Superheated'
                # We have (p, s) => find T, h from superheat data
                self.T = float(griddata((ssh_all, psh_all), tsh_all, (self.s, self.p)))
                self.h = float(griddata((ssh_all, psh_all), hsh_all, (self.s, self.p)))
                self.x = 1.0
                # approximate v with ideal gas
                TK = self.T + 273.15
                self.v = R * TK / (self.p * 1000.0)

    def print(self):
        """
        Prints a nicely formatted report of the steam properties.
        """
        print('Name: ', self.name)
        if self.x is not None and self.x < 0.0:
            print('Region: compressed liquid (x<0)')
        else:
            print('Region: ', self.region)

        print('p = {:0.2f} kPa'.format(self.p))
        if self.x is not None and self.x >= 0.0:
            print('T = {:0.1f} deg C'.format(self.T))
        if self.h is not None:
            print('h = {:0.2f} kJ/kg'.format(self.h))
        if self.x is not None and self.x >= 0.0:
            print('s = {:0.4f} kJ/(kg·K)'.format(self.s))
            if self.region == 'Saturated':
                print('v = {:0.6f} m^3/kg'.format(self.v))
                print('x = {:0.4f}'.format(self.x))
        print()

# endregion

# region function definitions
def main():
    # Simple test
    inlet = steam(7350, name='Turbine Inlet')  # not enough info
    inlet.x = 0.9
    inlet.calc()
    inlet.print()

    h1 = inlet.h
    s1 = inlet.s
    print("inlet h, s =", h1, s1, '\n')

    # Another test: isentropic expansion from p=7350 => p=100
    outlet = steam(100, s=inlet.s, name='Turbine Exit')
    outlet.print()

    # Another test: specify enthalpy at a certain pressure
    st3 = steam(8575, h=2050, name='State 3')
    st3.print()

    st4 = steam(8575, h=3125, name='State 4')
    st4.print()

if __name__ == "__main__":
    main()
# endregion
