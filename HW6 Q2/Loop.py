class Loop:
    """
    Represents a loop in a pipe network.
    The pipes within the loop must be listed in order to ensure correct traversal.
    """

    def __init__(self, Name='A', Pipes=[]):
        """
        Initializes the loop with a given name and a list of pipes.

        :param Name: A string representing the loop's identifier.
        :param Pipes: A list of Pipe objects forming a closed loop.
        """
        self.name = Name  # Store the loop name
        self.pipes = Pipes  # Store the pipes that make up the loop

    def getLoopHeadLoss(self):
        """
        Calculates the total head loss around the loop by summing up the head losses of individual pipes.
        The head loss is calculated based on the traversal direction around the loop.

        :return: Net head loss in meters of fluid.
        """
        deltaP = 0  # Initialize head loss to zero
        startNode = self.pipes[0].startNode  # Start from the first pipe's start node

        for p in self.pipes:
            # Determine head loss considering the direction of traversal in the loop
            phl = p.getFlowHeadLoss(startNode)
            deltaP += phl

            # Move to the next node in the loop traversal
            startNode = p.endNode if startNode != p.endNode else p.startNode

        return deltaP