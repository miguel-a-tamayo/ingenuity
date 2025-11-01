"""
Name:   Miguel Tamayo
Date:   10/28/2025
"""

import numpy as np

from constants.ingenuityConstants import mass
from model.inputs import Force, Moment
from utilities.rotations import quatConjugate, quatMult, quatNormalize
from model.states import VehicleState


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
        Sets both current stae and derivative states to zero
        """
        self.state = self.setVehicleState(VehicleState())

    def calculateDerivative(self, state: VehicleState, forces: Force) -> np.array:
        """
        calcualteDerivative(state: VehicleState, forces: Force, moments: Moment)
        Calculates vehicle state derivative given the current state and input forces and moments

        :param state: current state
        :param forces: sum of all forces acting on the vehicle [N] in the body frame
        :param moments: sum of all moments acting on the vehicle [N-m] about the body

        :return stateDot: vehicle state derivative
        """

        # inertial velocity (pdot)
        vel_inertial = np.array([state.u, state.v, state.w])

        # acceleration (vdot)
        accel_body = (1.0 / mass) * forces.vector()
    
        return np.array([*vel_inertial, *accel_body])