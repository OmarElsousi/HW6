#region imports
from ResistorNetwork import ResistorNetwork, ResistorNetwork_2
#endregion

# region Function Definitions
def main():
    """
    This program solves for the unknown currents in two circuits:
    1) The original "ResistorNetwork.txt"
    2) The updated "ResistorNetwork_2.txt" with extra resistor(s) and loop(s).
    """
    print("Network 1:")
    # Instantiate a ResistorNetwork object
    Net = ResistorNetwork()
    # Build the resistor network from a text file
    Net.BuildNetworkFromFile("ResistorNetwork.txt")
    # Analyze the first circuit
    IVals = Net.AnalyzeCircuit()

    print("\nNetwork 2:")
    # Instantiate a ResistorNetwork_2 object
    Net_2 = ResistorNetwork_2()
    # Build from the second text file
    Net_2.BuildNetworkFromFile("ResistorNetwork_2.txt")
    # Analyze the second circuit
    IVals_2 = Net_2.AnalyzeCircuit()

if __name__=="__main__":
    main()
