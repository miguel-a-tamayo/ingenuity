"""
Author: Miguel Tamayo

rotations.py
implements various matric rotations such as Euler->DCM
                                            DCM->Euler
                                            NED->ENU
"""

import numpy as np

def euler2Quat(yaw: float, pitch: float, roll: float) -> list:
    """
    Create quaternion from Euler angles. Angles correspond to the [3, 2, 1] Euler set.
    Euler angles describe the rotation of the vehicle relative to the inertial frame.
    
    quaternion will rotate vectors from the body frame [B] to the inertial frame [I]

    :param yaw:     rotation about inertial down [rad]
    :param pitch:   rotation about intermediate y-axis [rad]
    :param roll:    rotation about body x-axis [rad]

    :return quat: rotation quaternion
    """

    yaw_rotation = [np.cos(yaw / 2),
                    0,
                    0,
                    np.sin(yaw / 2)]
    
    pitch_rotation = [np.cos(pitch / 2),
                      0,
                      np.sin(pitch / 2),
                      0]

    roll_rotation = [np.cos(roll / 2),
                     np.sin(roll / 2),
                     0,
                     0]
    
    quat1 = quatMult(roll_rotation, pitch_rotation)
    quat = quatMult(quat1, yaw_rotation)
    
    return quat

def quatMult(q1: list, q2: list) -> list:
    """
    multiplies 2 quaternions

    :param q1: quaternion 1
    :param q2: quaternion 2

    :return quat: resulting quaternion
    """
    a1 = q1[0]; a2 = q2[0] 
    b1 = q1[1]; b2 = q2[1]
    c1 = q1[2]; c2 = q2[2]
    d1 = q1[3]; d2 = q2[3]

    w = a1*a2 - b1*b2 - c1*c2 - d1*d2
    x = a1*b2 + b1*a2 + c1*d2 - d1*c2
    y = a1*c2 - b1*d2 + c1*a2 + d1*b2
    z = a1*d2 + b1*c2 - c1*b2 + d1*a2

    quat = [w, x, y, z]

    return quat

def quatConjugate(q: list) -> list:
    """
    caluculates the conjugate of a quaternion

    :param q: input quaternion

    :return qc: quaternion conjugate
    """

    qc = [q[0], -q[1], -q[2], -q[3]]

    return qc

def ned2enu(points: list) -> list:
    """
    changes the coordinates from North-East-Down (NED) to East-North-Up (ENU)
    this is required because the graphics functions use ENU frame

    :param points: matrix of NED points [n x 3]
    
    :return enuPoints: matrix of ENU points [n x 3]
    """

    # flip the first and second, multiply third by -1
    enuPoints = [[point[1], point[0], -point[2]] for point in points] # matrix of ENU points

    return enuPoints