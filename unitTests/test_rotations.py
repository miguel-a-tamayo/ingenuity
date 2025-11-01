"""
Author: Miguel Tamayo

test_rotations.py
Tests the rotations utilities
"""

from utilities.rotations import (euler2Quat, quatMult, quatConjugate,
                                   quatNormalize, ned2enu)

import numpy as np
import pytest

tolerance = 1e-8

def test_quatNormUnitLength():
    # Normalization of a unit quaternion should not change it
    q = np.array([0.7071, 0.7071, 0, 0])
    qn = quatNormalize(q)

    expected = q / np.linalg.norm(q)
    assert np.allclose(qn, expected, atol = tolerance)

def test_quatNorm():
    # Normalization should remove magnitude scaling
    q = np.array([2, 0, 0, 0])
    qn = quatNormalize(q)

    expected = np.array([1, 0, 0, 0])
    assert np.allclose(qn, expected, atol = tolerance)

def test_quatNormZero():
    # Zero quaternion should raise ValueError
    q = np.array([0, 0, 0, 0])
    with pytest.raises(ValueError):
        quatNormalize(q)

def test_identityMultiplication():
    # q * 1 = q
    q = np.array([0.7071, 0.7071, 0, 0])  # 90° rotation around X
    identity = np.array([1, 0, 0, 0])
    result = quatMult(q, identity)

    assert np.allclose(result, q, atol = tolerance)

def test_commutativityFail():
    # Quaternion multiplication is NOT commutative
    q1 = np.array([0.7071, 0.7071, 0, 0])  # rot X 90°
    q2 = np.array([0.7071, 0, 0.7071, 0])  # rot Y 90°
    q12 = quatMult(q1, q2)
    q21 = quatMult(q2, q1)

    assert not np.allclose(q12, q21, atol = tolerance)

def test_90degComposition():
    # Two 90 deg X rotations = 180 deg X rotation
    qx_90 = np.array([np.cos(np.pi/4), np.sin(np.pi/4), 0, 0])
    qx_180_expected = np.array([np.cos(np.pi/2), np.sin(np.pi/2), 0, 0])
    qx_180 = quatMult(qx_90, qx_90)

    assert np.allclose(qx_180, qx_180_expected, atol = tolerance)

def test_quatConjugate():
    # flips all the axes expect for the scalar
    q = quatConjugate(np.array([0.5, -1, 0.542, -0.701]))
    expected = np.array([0.5, 1, -0.542, 0.701])
    
    assert np.allclose(q, expected, atol = tolerance)

def test_euler2QuatIdentity():
    # No rotation results in identiy quaternion
    q = euler2Quat(0, 0, 0)
    expected = np.array([1, 0, 0, 0])

    assert np.allclose(q, expected, atol = tolerance)

def test_euler2Quat():
    # 90 degree rotation along yaw 
    deg = np.deg2rad(90)

    q = euler2Quat(deg, 0, 0)
    expected = np.array([0.7071, 0, 0, 0.7071])
    assert np.allclose(q, expected, atol = tolerance)

    # 90 degree yaw pitch roll
    q = euler2Quat(deg, deg, deg)
    expected = np.array([ 0.7071068, 0, 0.7071068, 0])
    assert np.allclose(q, expected, atol = tolerance)

def test_ned2enu():
    # north east down = north east -up
    ned = np.array([[34, 23, 56]])
    enu = ned2enu(ned)

    expected = np.array([[23, 34, -56]])
    assert np.allclose(enu, expected, atol = tolerance)

