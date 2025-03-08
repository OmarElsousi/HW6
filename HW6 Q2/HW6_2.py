# region imports
from Fluid import Fluid
from Pipe import Pipe
from Loop import Loop
from PipeNetwork import PipeNetwork
# endregion

# region function definitions
def main():
    '''
    This program analyzes flows in a given pipe network based on:
      1. The pipe segments are named by their endpoint node names (e.g. a-b, b-e, etc.).
      2. Flow from the lower letter to the higher letter is considered positive.
      3. Pressure (head) decreases in the direction of flow.
      4. At each node, mass is conserved (net flow = external flow).
      5. Around each loop, the net head loss is zero.
    '''
    # FILLED IN MISSING CODE: instantiate a Fluid object for water
    water = Fluid()  # default mu=0.00089, rho=1000 => water

    roughness = 0.00025  # in meters

    # FILLED IN MISSING CODE: instantiate a new PipeNetwork object
    PN = PipeNetwork()

    # add Pipe objects to the network
    PN.pipes.append(Pipe('a','b',250, 300, roughness, water))
    PN.pipes.append(Pipe('a','c',100, 200, roughness, water))
    PN.pipes.append(Pipe('b','e',100, 200, roughness, water))
    PN.pipes.append(Pipe('c','d',125, 200, roughness, water))
    PN.pipes.append(Pipe('c','f',100, 150, roughness, water))
    PN.pipes.append(Pipe('d','e',125, 200, roughness, water))
    PN.pipes.append(Pipe('d','g',100, 150, roughness, water))
    PN.pipes.append(Pipe('e','h',100, 150, roughness, water))
    PN.pipes.append(Pipe('f','g',125, 250, roughness, water))
    PN.pipes.append(Pipe('g','h',125, 250, roughness, water))

    # add Node objects by scanning the pipes
    PN.buildNodes()

    # specify external flows at certain nodes (in L/s: + for inflow, - for outflow)
    PN.getNode('a').extFlow = 60
    PN.getNode('d').extFlow = -30
    PN.getNode('f').extFlow = -15
    PN.getNode('h').extFlow = -15

    # build loops: the order of pipes matters for the loop
    # Loop A
    PN.loops.append(Loop('A', [
        PN.getPipe('a-b'),
        PN.getPipe('b-e'),
        PN.getPipe('d-e'),
        PN.getPipe('c-d'),
        PN.getPipe('a-c')
    ]))

    # Loop B
    PN.loops.append(Loop('B', [
        PN.getPipe('c-d'),
        PN.getPipe('d-g'),
        PN.getPipe('f-g'),
        PN.getPipe('c-f')
    ]))

    # Loop C
    PN.loops.append(Loop('C', [
        PN.getPipe('d-e'),
        PN.getPipe('e-h'),
        PN.getPipe('g-h'),
        PN.getPipe('d-g')
    ]))

    # Solve for flow rates
    PN.findFlowRates()

    # Print results
    PN.printPipeFlowRates()
    print()
    print('Check node flows:')
    PN.printNetNodeFlows()
    print()
    print('Check loop head loss:')
    PN.printLoopHeadLoss()
    # PN.printPipeHeadLosses() # if you want to see individual pipe head losses
# endregion

# region function calls
if __name__ == "__main__":
    main()
# endregion
