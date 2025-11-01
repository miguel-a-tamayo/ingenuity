"""
Author: Miguel Tamayo

test_inputs.py
Tests various input classes
"""
from model.inputs import Force, Moment

import numpy as np

tolerance = 1e-8

def test_createForce():
    # creates a unit vector force
    F = Force(1, 0, 0)
    expected = np.array([1, 0, 0])

    assert np.allclose(F.vector(), expected, atol=tolerance)

def test_addForce():
    # adding 2 forces together
    F1 = Force(1, 0, -0.6)
    F2 = Force(0.25, 0.5, 0)
    F = F1 + F2

    expected = np.array([1.25, 0.5, -0.6])
    assert np.allclose(F.vector(), expected, atol=tolerance)