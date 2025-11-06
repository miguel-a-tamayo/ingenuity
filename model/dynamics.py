"""
Name:   Miguel Tamayo
Date:   10/28/2025
"""

import numpy as np

from constants.ingenuityConstants import mass
from model.inputs import Force
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

        tSpan = np.array([0, self.dt])


    def calculateDerivative(self, t: float, stateVector: np.array, force: Force) -> np.array:
        """
        calcualteDerivative(stateVector: np.array, force: Force, moments: Moment)

        Calculates vehicle state derivative given the current state and input force and moments

        :param t: current tiem step t
        :param stateVector: current state in a vector form
        :param force: sum of all forces acting on the vehicle [N] in the body frame

        :return stateDot: vehicle state derivative
        """

        # inertial velocity (pdot)
        pos_inertial = stateVector[3:6]

        # acceleration (vdot)
        vel_body = (1.0 / mass) * force.vector()
    
        return np.array([*pos_inertial, *vel_body])