# region class definitions
class Loop():
    #region constructor
    def __init__(self, Name='A', Pipes=[]):
        '''
        Defines a loop in a pipe network.  The pipes must be listed in order.
        The traversal of a pipe loop will begin at the start node of Pipe[0].
        '''
        #region attributes
        self.name = Name
        self.pipes = Pipes
        #endregion
    #endregion

    #region methods
    def getLoopHeadLoss(self):
        '''
        Calculates the net head loss as we traverse around the loop, in m of fluid.
        '''
        deltaP = 0  # initialize to zero
        startNode = self.pipes[0].startNode  # begin at the start node of the first pipe
        for p in self.pipes:
            # calculates the head loss in the pipe considering loop traversal direction
            phl = p.getFlowHeadLoss(startNode)
            deltaP += phl
            # move to the next node in the loop
            startNode = p.endNode if startNode != p.endNode else p.startNode
        return deltaP
    #endregion
#endregion
