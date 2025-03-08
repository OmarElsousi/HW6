#region imports
from scipy.optimize import fsolve
import numpy as np
from Fluid import Fluid
from Node import Node
#endregion

# region class definitions
class PipeNetwork():
    #region constructor
    def __init__(self, Pipes=[], Loops=[], Nodes=[], fluid=Fluid()):
        '''
        The pipe network is built from pipe, node, loop, and fluid objects.
        :param Pipes: a list of pipe objects
        :param Loops: a list of loop objects
        :param Nodes: a list of node objects
        :param fluid: a fluid object
        '''
        #region attributes
        self.loops = Loops
        self.nodes = Nodes
        self.Fluid = fluid
        self.pipes = Pipes
        #endregion
    #endregion

    #region methods
    def findFlowRates(self):
        '''
        Analyze the pipe network and find the flow rates in each pipe
        given the constraints:
           (1) net flow at each node = 0 (unless external flow is specified)
           (2) net head loss around each loop = 0
        '''
        # number of equations = number of nodes + number of loops
        N = len(self.nodes) + len(self.loops)

        # Build an initial guess for the flow rates. We have len(self.pipes) unknown flows,
        # plus possibly 1 more for a degenerate node. The code is set to N, so let's do that:
        Q0 = np.full(N, 10.0)

        def fn(q):
            """
            Callback for fsolve. The mass continuity (node) equations plus
            the loop head-loss equations are all set to zero.
            :param q: array of flow values for the pipes (and possibly one extra if needed).
            :return: array of results from node flows + loop head losses.
            """
            # FILLED IN MISSING CODE: Assign flows to each pipe
            for i in range(len(self.pipes)):
                self.pipes[i].Q = q[i]

            # FILLED IN MISSING CODE: Gather node net flows
            L = self.getNodeFlowRates()

            # FILLED IN MISSING CODE: Append loop head losses
            L += self.getLoopHeadLosses()

            return L

        # Use fsolve to solve the system
        FR = fsolve(fn, Q0)
        return FR

    def getNodeFlowRates(self):
        # each node calculates net flow => we want them all to be zero
        qNet = [n.getNetFlowRate() for n in self.nodes]
        return qNet

    def getLoopHeadLosses(self):
        # each loop calculates net head loss => we want them to be zero
        lhl = [l.getLoopHeadLoss() for l in self.loops]
        return lhl

    def getPipe(self, name):
        # returns a pipe object by name "a-b"
        for p in self.pipes:
            if name == p.Name():
                return p

    def getNodePipes(self, node):
        # returns a list of pipe objects that connect to a node
        l = []
        for p in self.pipes:
            if p.oContainsNode(node):
                l.append(p)
        return l

    def nodeBuilt(self, node):
        # checks if a node by this name was already built
        for n in self.nodes:
            if n.name == node:
                return True
        return False

    def getNode(self, name):
        # retrieves a node object by name
        for n in self.nodes:
            if n.name == name:
                return n

    def buildNodes(self):
        # automatically create node objects by looking at pipe endpoints
        for p in self.pipes:
            if not self.nodeBuilt(p.startNode):
                self.nodes.append(Node(p.startNode, self.getNodePipes(p.startNode)))
            if not self.nodeBuilt(p.endNode):
                self.nodes.append(Node(p.endNode, self.getNodePipes(p.endNode)))

    def printPipeFlowRates(self):
        for p in self.pipes:
            p.printPipeFlowRate()

    def printNetNodeFlows(self):
        for n in self.nodes:
            print('net flow into node {} is {:0.2f}'.format(n.name, n.getNetFlowRate()))

    def printLoopHeadLoss(self):
        for l in self.loops:
            print('head loss for loop {} is {:0.2f}'.format(l.name, l.getLoopHeadLoss()))
# endregion
