# region imports
from ResistorNetwork import ResistorNetwork, ResistorNetwork_2


# endregion

# region Function Definitions
def main():
    """
    This script analyzes two electrical resistor networks by solving for unknown currents.

    The program does the following:
    1. Reads and analyzes the first circuit from "ResistorNetwork.txt".
    2. Reads and analyzes the second (modified) circuit from "ResistorNetwork_2.txt".

    It uses the `ResistorNetwork` and `ResistorNetwork_2` classes to build and analyze the networks.
    """

    print("Network 1:")
    # Create an instance of the ResistorNetwork class to handle the first circuit
    Net = ResistorNetwork()
    # Load the resistor network from a text file
    Net.BuildNetworkFromFile("ResistorNetwork.txt")
    # Analyze the circuit to compute the unknown currents
    IVals = Net.AnalyzeCircuit()

    print("\nNetwork 2:")
    # Create an instance of the modified ResistorNetwork_2 class for the second circuit
    Net_2 = ResistorNetwork_2()
    # Load the second circuit from another file
    Net_2.BuildNetworkFromFile("ResistorNetwork_2.txt")
    # Analyze the second circuit to compute the unknown currents
    IVals_2 = Net_2.AnalyzeCircuit()


# Ensure the script runs only when executed directly (not when imported)
if __name__ == "__main__":
    main()
