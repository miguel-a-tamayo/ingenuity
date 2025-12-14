"""
Name:   Miguel Tamayo
Date:   10/28/2025
"""

import numpy as np

from constants.ingenuityConstants import mass
from model.inputs import Force
from model.states import VehicleState
from utilities.integrator import integrateRk4
from utilities.rotations import quatConjugate, quatMult

class VehicleDynamics:
    """
    Class defining vehicle dynamics

    :param dt: time step for the simulation
    """
    def __init__(self,
                 dt = 0.01):

        # initialize current state of the vehicle to 0 
        self.state = VehicleState()

        # initialize a state for the derivative to 0
        self.stateDerivative = VehicleState()

        self.dt = dt # keeping a copy of dt to carry
    
    def getVehicleState(self) -> VehicleState:
        """
        getVehicleState()
        Return the instance of current vehicle state

        :return state: vehicle state
        """
        return self.state

    def setVehicleState(self, state: VehicleState) -> None:
        """
        setVehicleState(state: VehicleState)
        Sets the current vehicle state to the input state

        :param vehicleState: new vehicle state
        """
        self.state = state
    
    def getVehicleDerivative(self) -> VehicleState:
        """
        getVehicleDerivative()
        Return the instance of the current vehicle derivative state

        :return stateDerivative: vehicle derivative state
        """
        return self.stateDerivative
    
    def setVehicleDerivative(self, derivativeState: VehicleState) -> None:
        """
        setVehicleDerivative(derivativeState: VehicleState)

        Sets the current vehicle derivative state to the input state

        :param derivativeState: new vehicle derivative state
        """
        self.stateDerivative = derivativeState
    
    def reset(self) -> None:
        """
        reset()

        Sets both current state and derivative states to zero
        """
        self.setVehicleState(VehicleState())
        self.setVehicleDerivative(VehicleState())

    def update(self, forces: Force) -> None:
        """
        update()

        Function that implements the intergration such that the state is updated using the forces

        :param forces: sum of forces acting on the vehicle [N] in the body frame
        """

        self.state = integrateRk4(self.calculateDerivative, self.state, 0.0, self.dt, forces)


    def calculateDerivative(self, t: float, stateVector: np.array, force: Force) -> np.array:
        """
        calcualteDerivative(stateVector: np.array, force: Force)

        Calculates vehicle state derivative given the current state and input forces

        :param t: current tiem step t
        :param stateVector: current state in a vector form
        :param force: sum of all forces acting on the vehicle [N] in the body frame

        :return stateDot: vehicle state derivative
        """

        # inertial velocity (pdot)
        body2Inertial = stateVector[6:10]
        inertial2Body = quatConjugate(body2Inertial)
        pdotInertial = quatMult(quatMult(body2Inertial, stateVector[3:6]), inertial2Body)

        # acceleration (vdot)
        vdotBody = (1.0 / mass) * force.vector()

        # quaternion (qdot)
        # NOTE: because we don't have rotational dynamics at the moment, the quaternion doesn't
        # need to be integrated
        qDot = np.array([0, 0, 0, 0])

        newDerivative = np.array([*pdotInertial, *vdotBody, *qDot])

        return np.array([*pdotInertial, *vdotBody, *qDot])