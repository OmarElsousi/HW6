#region imports
import math
import numpy as np
import random as rnd
from scipy.optimize import fsolve
from Fluid import Fluid
#endregion

# region class definitions
class Pipe():
    #region constructor
    def __init__(self, Start='A', End='B', L=100, D=200, r=0.00025, fluid=Fluid()):
        '''
        Defines a generic pipe with orientation from lowest letter to highest, alphabetically.
        :param Start: the start node (string)
        :param End: the end node (string)
        :param L: the pipe length in m (float)
        :param D: the pipe diameter in mm (float)
        :param r: the pipe roughness in m  (float)
        :param fluid: a Fluid object (typically water)
        '''
        #region attributes
        # from arguments given in constructor
        self.startNode = min(Start, End)   # use the lowest letter for startNode
        self.endNode = max(Start, End)     # use the highest letter for endNode
        self.length = L
        self.r = r
        self.fluid = fluid

        # other calculated properties
        self.d = D/1000.0               # diameter in m
        self.relrough = self.r/self.d   # relative roughness
        self.A = math.pi/4.0 * self.d**2  # cross-sectional area, m^2
        self.Q = 10                     # initial guess, in L/s
        self.vel = self.V()            # compute velocity
        self.reynolds = self.Re()      # compute Reynolds number
        #endregion
    #endregion

    #region methods
    def V(self):
        '''
        Calculate average velocity in the pipe for volumetric flow self.Q
        :return: the average velocity in m/s
        '''
        # FILLED IN MISSING CODE
        # Q is in L/s => convert to m^3/s by multiplying by 0.001
        self.vel = (self.Q * 0.001) / self.A
        return self.vel

    def Re(self):
        '''
        Calculate the Reynolds number under current conditions.
        :return: Reynolds number (dimensionless)
        '''
        # FILLED IN MISSING CODE
        self.reynolds = (self.fluid.rho * self.V() * self.d) / self.fluid.mu
        return self.reynolds

    def FrictionFactor(self):
        """
        Calculates the Darcy friction factor for a pipe, considering laminar vs turbulent flow,
        and a transitional region in between.
        """
        Re = self.Re()
        rr = self.relrough

        # For turbulent flow: use Colebrook eq with fsolve
        def CB():
            cb = lambda f: 1/(f**0.5) + 2.0 * np.log10(rr/3.7 + 2.51/(Re * f**0.5))
            result = fsolve(cb, 0.01)
            return result[0]

        # For laminar flow
        def lam():
            return 64 / Re

        # Classification
        if Re >= 4000:     # turbulent
            return CB()
        elif Re <= 2000:   # laminar
            return lam()
        else:
            # transitional => a blend (with random variation)
            CBff = CB()
            Lamff = lam()
            # linear interpolation
            mean = Lamff + ((Re - 2000)/(4000 - 2000)) * (CBff - Lamff)
            sig = 0.2 * mean
            return rnd.normalvariate(mean, sig)

    def frictionHeadLoss(self):
        '''
        Use the Darcy–Weisbach equation to find the head loss (in m of fluid).
         h_f = f * (L / D) * (v^2 / (2*g))
        '''
        g = 9.81  # m/s^2
        ff = self.FrictionFactor()
        # FILLED IN MISSING CODE
        hl = ff * (self.length / self.d) * (self.vel**2) / (2 * g)
        return hl

    def getFlowHeadLoss(self, s):
        '''
        Calculate the signed head loss for the pipe if we are "traversing" in a loop.
        If flow is with the loop traversal direction, it's positive. Opposite => negative.
        :param s: the node I'm starting with in a loop traversal
        :return: the signed headloss in m
        '''
        # if s == startNode, we are traversing from start->end, otherwise end->start
        nTraverse = 1 if s == self.startNode else -1
        # if Q is positive in the "start->end" sense, nFlow=1, else -1
        nFlow = 1 if self.Q >= 0 else -1
        return nTraverse * nFlow * self.frictionHeadLoss()

    def Name(self):
        '''
        Gets the pipe name as "a-b".
        :return: string
        '''
        return self.startNode + '-' + self.endNode

    def oContainsNode(self, node):
        '''
        Does the pipe connect to the specified node?
        '''
        return (self.startNode == node or self.endNode == node)

    def printPipeFlowRate(self):
        print('The flow in segment {} is {:0.2f} L/s'.format(self.Name(), self.Q))

    def getFlowIntoNode(self, n):
        '''
        determines the flow rate into node n
        :param n: node's name
        :return: +Q if flowing into the node, -Q if flowing out
        '''
        if n == self.startNode:
            # node is the start => if Q is positive start->end, flow is leaving 'start', so negative
            return -self.Q
        else:
            return self.Q
    #endregion
#endregion
