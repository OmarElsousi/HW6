from Rankine_stem import Rankine

def main():
    """
    Main function to analyze two different Rankine power cycles:
    1. Saturated vapor entering the turbine.
    2. Superheated steam entering the turbine.

    The script instantiates two `rankine` objects, calculates the cycle efficiencies,
    and outputs a detailed report for each cycle.
    """

    # Rankine Cycle i: Saturated vapor entering the turbine
    print("Rankine Cycle i: Saturated vapor entering the turbine")
    # Instantiate the first Rankine object with p_low=8 kPa, p_high=8000 kPa, and t_high=None.
    # Setting t_high=None indicates that the turbine inlet is saturated vapor (x = 1).
    Rankine_i = Rankine(p_low=8, p_high=8000, t_high=None, name='Rankine Cycle i')
    # Calculate the efficiency of the cycle using the calc_efficiency() method.
    efficiency_i = Rankine_i.calc_efficiency()
    # Print a detailed report of the cycle's properties using the print_summary() method.
    Rankine_i.print_summary()
    print(f"Efficiency of Rankine Cycle i: {efficiency_i:.2f}%\n")

    # Rankine Cycle ii: Superheated steam entering the turbine
    print("Rankine Cycle ii: Superheated steam entering the turbine")
    # Calculate the superheated temperature as 1.7 * T_sat, where T_sat is the saturation temperature at p_high.
    # For p_high = 8000 kPa, the saturation temperature (T_sat) is approximately 295°C.
    T_sat = 295  # Approximate saturation temperature at 8000 kPa (from steam tables)
    T_high = 1.7 * T_sat  # Superheated temperature
    # Instantiate the second Rankine object with p_low=8 kPa, p_high=8000 kPa, and t_high=T_high.
    # Setting t_high=T_high indicates that the turbine inlet is superheated steam.
    Rankine_ii = Rankine(p_low=8, p_high=8000, t_high=T_high, name='Rankine Cycle ii')
    # Calculate the efficiency of the cycle using the calc_efficiency() method.
    efficiency_ii = Rankine_ii.calc_efficiency()
    # Print a detailed report of the cycle's properties using the print_summary() method.
    Rankine_ii.print_summary()
    print(f"Efficiency of Rankine Cycle ii: {efficiency_ii:.2f}%\n")

if __name__ == "__main__":
    # Run the main function when the script is executed.
    main()