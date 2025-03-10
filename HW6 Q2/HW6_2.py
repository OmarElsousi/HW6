from Fluid import Fluid
from Pipe import Pipe
from Loop import Loop
from PipeNetwork import PipeNetwork


def main():
    """
    This program analyzes fluid flow through a pipe network based on the following principles:
    1. Pipe segments are named by their endpoint node names (e.g., 'a-b', 'b-e').
    2. Flow direction from a lower to a higher letter is considered positive.
    3. Pressure (head) decreases in the direction of flow.
    4. At each node, mass is conserved (net flow equals external flow).
    5. Around each loop, the net head loss is zero.
    """

    # Create a fluid object for water with default properties (mu=0.00089, rho=1000)
    water = Fluid()
    roughness = 0.00025  # Pipe roughness in meters

    # Create a new pipe network
    PN = PipeNetwork()

    # Define pipes and add them to the network
    PN.pipes.append(Pipe('a', 'b', 250, 300, roughness, water))
    PN.pipes.append(Pipe('a', 'c', 100, 200, roughness, water))
    PN.pipes.append(Pipe('b', 'e', 100, 200, roughness, water))
    PN.pipes.append(Pipe('c', 'd', 125, 200, roughness, water))
    PN.pipes.append(Pipe('c', 'f', 100, 150, roughness, water))
    PN.pipes.append(Pipe('d', 'e', 125, 200, roughness, water))
    PN.pipes.append(Pipe('d', 'g', 100, 150, roughness, water))
    PN.pipes.append(Pipe('e', 'h', 100, 150, roughness, water))
    PN.pipes.append(Pipe('f', 'g', 125, 250, roughness, water))
    PN.pipes.append(Pipe('g', 'h', 125, 250, roughness, water))

    # Automatically build nodes from pipe connections
    PN.buildNodes()

    # Specify external flow at nodes (L/s, positive for inflow, negative for outflow)
    PN.getNode('a').extFlow = 60
    PN.getNode('d').extFlow = -30
    PN.getNode('f').extFlow = -15
    PN.getNode('h').extFlow = -15

    # Define loops and their respective pipes (order matters)
    PN.loops.append(Loop('A', [
        PN.getPipe('a-b'),
        PN.getPipe('b-e'),
        PN.getPipe('d-e'),
        PN.getPipe('c-d'),
        PN.getPipe('a-c')
    ]))
#Loop B
    PN.loops.append(Loop('B', [
        PN.getPipe('c-d'),
        PN.getPipe('d-g'),
        PN.getPipe('f-g'),
        PN.getPipe('c-f')
    ]))
#Loop C
    PN.loops.append(Loop('C', [
        PN.getPipe('d-e'),
        PN.getPipe('e-h'),
        PN.getPipe('g-h'),
        PN.getPipe('d-g')
    ]))

    # Solve for flow rates in pipes
    PN.findFlowRates()

    # Print results
    PN.printPipeFlowRates()
    print('\nCheck node flows:')
    PN.printNetNodeFlows()
    print('\nCheck loop head loss:')
    PN.printLoopHeadLoss()
 # PN.printPipeHeadLosses() # if you want to see individual pipe head losses
# endregion

# Run the main function when the script is executed directly
if __name__ == "__main__":
    main()
# endregion