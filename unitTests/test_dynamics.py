"""
Author: Miguel Tamayo

test_dynamics.py
Tests vehicle dynamics
"""

from constants.ingenuityConstants import mass
from model.dynamics import VehicleDynamics
from model.inputs import Force
from model.states import VehicleState

import numpy as np

def test_getState():
    # set the state and get it back
    inputState = VehicleState(1, 2, 3, 0, 0.5, 1.2)
    testVehicle = VehicleDynamics()

    testVehicle.setVehicleState(state=inputState)
    assert testVehicle.getVehicleState() == inputState

def test_getDerivativeState():
    # set the derivative state and get it back
    inputState = VehicleState(2, 4, 1, 6, 4, 1)
    testVehicle = VehicleDynamics()

    testVehicle.setVehicleDerivative(inputState)
    assert testVehicle.getVehicleDerivative() == inputState

def test_derivative():
    # calculate the derivative of a vehicle
    vehicle = VehicleDynamics()
    force = Force(x=10.0, y=15.0)
    state = VehicleState(u=10.0)

    dot = vehicle.calculateDerivative(state, force)

    expected = np.array([10.0, 0.0, 0.0])
    assert np.allclose(dot[0:3], expected, atol=1e-8)

    expected = np.array([10.0, 15.0, 0.0]) / mass
    assert np.allclose(dot[3:6], expected, atol=1e-8)