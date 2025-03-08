#region class definitions
class Node():
    #region constructor
    def __init__(self, Name='a', Pipes=[], ExtFlow=0):
        '''
        A node in a pipe network.
        :param Name: name of the node
        :param Pipes: a list/array of pipes connected to this node
        :param ExtFlow: any external flow into (+) or out (-) of this node in L/s
        '''
        #region attributes
        self.name = Name
        self.pipes = Pipes
        self.extFlow = ExtFlow
        #endregion
    #endregion

    #region methods
    def getNetFlowRate(self):
        '''
        Calculates the net flow rate into this node in L/s
        :return: the net flow rate into this node
        '''
        # FILLED IN MISSING CODE
        Qtot = self.extFlow  # start with external flow
        for p in self.pipes:
            # For each pipe, add the flow into this node (negative if outflow).
            Qtot += p.getFlowIntoNode(self.name)
        return Qtot
    #endregion
#endregion
