from scipy.optimize import fsolve
import numpy as np
from Fluid import Fluid
from Node import Node


class PipeNetwork:
    """
    Represents a network of interconnected pipes, nodes, and loops, solving for flow rates
    based on mass conservation at nodes and energy conservation around loops.
    """

    def __init__(self, Pipes=[], Loops=[], Nodes=[], fluid=Fluid()):
        """
        Initializes a PipeNetwork with lists of pipes, loops, and nodes.

        :param Pipes: List of Pipe objects in the network.
        :param Loops: List of Loop objects in the network.
        :param Nodes: List of Node objects in the network.
        :param fluid: Fluid object representing the working fluid in the pipes.
        """
        self.loops = Loops  # Store list of loops
        self.nodes = Nodes  # Store list of nodes
        self.Fluid = fluid  # Store fluid properties
        self.pipes = Pipes  # Store list of pipes

    def findFlowRates(self):
        """
        Solves for flow rates in the pipes using mass continuity and head loss equations.
        """
        N = len(self.nodes) + len(self.loops)  # Number of equations (nodes + loops)
        Q0 = np.full(N, 10.0)  # Initial guess for flow rates (L/s)

        def fn(q):
            """
            Function to be solved by fsolve, enforcing conservation of mass at nodes
            and conservation of energy around loops.

            :param q: Array of flow rates in pipes.
            :return: Array of residuals for node mass balance and loop head losses.
            """
            for i in range(len(self.pipes)):
                self.pipes[i].Q = q[i]  # Assign flow rates to pipes

            L = self.getNodeFlowRates()  # Compute net flow rates at nodes
            L += self.getLoopHeadLosses()  # Compute net head loss around loops

            return L

        FR = fsolve(fn, Q0)  # Solve system of equations
        return FR

    def getNodeFlowRates(self):
        """
        Computes the net flow rate at each node.

        :return: List of net flow rates at all nodes.
        """
        return [n.getNetFlowRate() for n in self.nodes]

    def getLoopHeadLosses(self):
        """
        Computes the net head loss around each loop.

        :return: List of net head losses for each loop.
        """
        return [l.getLoopHeadLoss() for l in self.loops]

    def getPipe(self, name):
        """
        Retrieves a Pipe object by its name.

        :param name: Name of the pipe (format: 'a-b').
        :return: Corresponding Pipe object.
        """
        for p in self.pipes:
            if name == p.Name():
                return p

    def getNodePipes(self, node):
        """
        Finds all pipes connected to a given node.

        :param node: Name of the node.
        :return: List of Pipe objects connected to the node.
        """
        return [p for p in self.pipes if p.oContainsNode(node)]

    def nodeBuilt(self, node):
        """
        Checks if a node already exists in the network.

        :param node: Name of the node.
        :return: True if node exists, False otherwise.
        """
        return any(n.name == node for n in self.nodes)

    def getNode(self, name):
        """
        Retrieves a Node object by name.

        :param name: Name of the node.
        :return: Corresponding Node object.
        """
        for n in self.nodes:
            if n.name == name:
                return n

    def buildNodes(self):
        """
        Automatically creates Node objects by scanning pipe connections.
        """
        for p in self.pipes:
            if not self.nodeBuilt(p.startNode):
                self.nodes.append(Node(p.startNode, self.getNodePipes(p.startNode)))
            if not self.nodeBuilt(p.endNode):
                self.nodes.append(Node(p.endNode, self.getNodePipes(p.endNode)))

    def printPipeFlowRates(self):
        """
        Prints flow rates for all pipes in the network.
        """
        for p in self.pipes:
            p.printPipeFlowRate()

    def printNetNodeFlows(self):
        """
        Prints the net flow at each node to verify mass conservation.
        """
        for n in self.nodes:
            print(f'Net flow into node {n.name} is {n.getNetFlowRate():.2f} L/s')

    def printLoopHeadLoss(self):
        """
        Prints head loss values for each loop to verify energy conservation.
        """
        for l in self.loops:
            print(f'Head loss for loop {l.name} is {l.getLoopHeadLoss():.2f} m')