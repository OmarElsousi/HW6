class Loop:
    """
    A class representing a loop in an electrical circuit.

    Loops are formed by connecting nodes in a closed path.
    This class stores the node names that make up the loop.
    """

    def __init__(self):
        """
        Initializes an empty loop.

        Attributes:
        - self.Nodes (list): A list to store node names forming the loop.
        """
        self.Nodes = []  # List to store node names that form a loop
