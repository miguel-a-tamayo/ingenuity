"""
Author: Miguel Tamayo

test_states.py
Tests various state types
"""

from model.states import VehicleState

import numpy as np

def test_stateAsVector():
    # create a state vector from the class
    state = VehicleState(1, 2, 3, 4, 5, 6)
    stateVector = state.asVector()

    expected = np.array([1, 2, 3, 4, 5, 6])
    assert np.allclose(stateVector, expected, atol=1e-8)

def test_stateFromVector():
    # create a vehicle state from a vector
    state = VehicleState()
    stateVector = np.array([1, 2, 3, 4, 5, 6])
    state.fromVector(stateVector)

    expected = VehicleState(*stateVector)
    assert state == expected