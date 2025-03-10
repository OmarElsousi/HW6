import math
import numpy as np
import random as rnd
from scipy.optimize import fsolve
from Fluid import Fluid


class Pipe:
    """
    Represents a pipe in a network with properties such as length, diameter, roughness,
    and flow characteristics.
    """

    def __init__(self, Start='A', End='B', L=100, D=200, r=0.00025, fluid=Fluid()):
        """
        Initializes a Pipe object with given parameters.

        :param Start: Name of the starting node (string).
        :param End: Name of the ending node (string).
        :param L: Pipe length in meters (float).
        :param D: Pipe diameter in millimeters (float).
        :param r: Pipe roughness in meters (float).
        :param fluid: A Fluid object representing the fluid inside the pipe.
        """
        self.startNode = min(Start, End)  # Ensure startNode is alphabetically lower
        self.endNode = max(Start, End)  # Ensure endNode is alphabetically higher
        self.length = L  # Store pipe length
        self.r = r  # Store pipe roughness
        self.fluid = fluid  # Store fluid properties

        # Compute derived properties
        self.d = D / 1000.0  # Convert diameter to meters
        self.relrough = self.r / self.d  # Compute relative roughness
        self.A = math.pi / 4.0 * self.d ** 2  # Compute cross-sectional area (m²)
        self.Q = 10  # Initial guess for flow rate (L/s)
        self.vel = self.V()  # Compute velocity (m/s)
        self.reynolds = self.Re()  # Compute Reynolds number

    def V(self):
        """
        Calculates the average velocity in the pipe based on the volumetric flow rate.

        :return: The average velocity in m/s.
        """
        self.vel = (self.Q * 0.001) / self.A  # Convert L/s to m³/s and compute velocity
        return self.vel

    def Re(self):
        """
        Computes the Reynolds number based on the pipe's current conditions.

        :return: The Reynolds number (dimensionless).
        """
        self.reynolds = (self.fluid.rho * self.V() * self.d) / self.fluid.mu
        return self.reynolds

    def FrictionFactor(self):
        """
        Computes the Darcy-Weisbach friction factor depending on the flow regime.
        Uses the Colebrook equation for turbulent flow and an approximation for laminar flow.

        :return: The friction factor (dimensionless).
        """
        Re = self.Re()
        rr = self.relrough

        def CB():
            cb = lambda f: 1 / (f ** 0.5) + 2.0 * np.log10(rr / 3.7 + 2.51 / (Re * f ** 0.5))
            result = fsolve(cb, 0.01)
            return result[0]

        def lam():
            return 64 / Re

        if Re >= 4000:
            return CB()  # Turbulent flow
        elif Re <= 2000:
            return lam()  # Laminar flow
        else:
            # Transitional flow: Interpolate between laminar and turbulent
            CBff = CB()
            Lamff = lam()
            mean = Lamff + ((Re - 2000) / (4000 - 2000)) * (CBff - Lamff)
            sig = 0.2 * mean
            return rnd.normalvariate(mean, sig)

    def frictionHeadLoss(self):
        """
        Calculates head loss in meters using the Darcy-Weisbach equation.

        :return: Head loss in meters of fluid.
        """
        g = 9.81  # Acceleration due to gravity (m/s²)
        ff = self.FrictionFactor()
        hl = ff * (self.length / self.d) * (self.vel ** 2) / (2 * g)
        return hl

    def getFlowHeadLoss(self, s):
        """
        Calculates the signed head loss in the pipe when traversing a loop.

        :param s: Starting node for traversal.
        :return: Signed head loss in meters.
        """
        nTraverse = 1 if s == self.startNode else -1
        nFlow = 1 if self.Q >= 0 else -1
        return nTraverse * nFlow * self.frictionHeadLoss()

    def Name(self):
        """
        Returns the pipe name in the format 'startNode-endNode'.

        :return: Pipe name as a string.
        """
        return f"{self.startNode}-{self.endNode}"

    def oContainsNode(self, node):
        """
        Checks if the pipe is connected to a given node.

        :param node: Node name (string).
        :return: True if the node is part of the pipe, False otherwise.
        """
        return self.startNode == node or self.endNode == node

    def printPipeFlowRate(self):
        """
        Prints the flow rate in the pipe.
        """
        print(f"The flow in segment {self.Name()} is {self.Q:.2f} L/s")

    def getFlowIntoNode(self, n):
        """
        Determines the flow rate into a specific node.

        :param n: The node name.
        :return: Positive flow if into the node, negative if out of the node.
        """
        if n == self.startNode:
            return -self.Q  # Flow is leaving the node
        else:
            return self.Q  # Flow is entering the node
