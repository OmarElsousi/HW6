class Node:
    """
    Represents a node (junction) in a pipe network where multiple pipes meet.
    """

    def __init__(self, Name='a', Pipes=[], ExtFlow=0):
        """
        Initializes a node with a name, a list of connected pipes, and an external flow rate.

        :param Name: A string representing the node's name.
        :param Pipes: A list of Pipe objects connected to this node.
        :param ExtFlow: External flow into (+) or out (-) of this node in L/s.
        """
        self.name = Name  # Store the node name
        self.pipes = Pipes  # Store the list of connected pipes
        self.extFlow = ExtFlow  # External flow rate at the node (L/s)

    def getNetFlowRate(self):
        """
        Calculates the net flow rate into this node by summing external flow and flows from connected pipes.

        :return: Net flow rate into this node (L/s).
        """
        Qtot = self.extFlow  # Start with the external flow at the node

        for p in self.pipes:
            # Add flow into the node (negative if it is flowing out of the node)
            Qtot += p.getFlowIntoNode(self.name)

        return Qtot