"""
Author: Miguel Tamayo

ingenuityDraw.py
Defines the different points of the vehicle in NED coordinates.
Handles moving and rotating the vehicle in the NED inertial frame
"""

from constants.ingenuityConstants import (width, depth, height, axis_len)
from utilities.rotations import (euler2Quat, quatConjugate, quatMult, ned2enu)

class IngenuityDraw():
    def __init__(self):

        red = [1.0, 0.6, 0.6, 1.0] #[1., 0., 0., 1.]
        green = [0.6, 1.0, 0.6, 1.0]
        blue = [0.6, 0.6, 1.0, 1.0]

        x = depth / 2.
        y = width / 2.
        z = height / 2.

        self.vertices = [
            [-x, -y, -z],   # 0
            [ x, -y, -z],   # 1
            [ x,  y, -z],   # 2
            [-x,  y, -z],   # 3
            [-x, -y,  z],   # 4
            [ x, -y,  z],   # 5
            [ x,  y,  z],   # 6
            [-x,  y,  z]    # 7
        ]

        self.faces = [
            [0, 1, 2], [0, 2, 3], # -z up face
            [4, 5, 6], [4, 6, 7], # +z down face
            [0, 3, 7], [0, 4, 7], # -x
            [0, 1, 4], [1, 4, 5], # -y
            [1, 2, 5], [2, 5, 6], # +x
            [2, 3, 6], [3, 6, 7], # +y
        ]

        self.colors = [
            green, green,
            red, red,
            blue, blue,
            blue, blue,
            blue, blue,
            blue, blue,
            blue, blue
        ]

        self.axes = [
            [axis_len, 0, 0],   # X+
            [0, axis_len, 0],   # Y+
            [0, 0, axis_len]    # Z+
        ]

        return

    def getNewPoints(self, x: float, y: float, z: float, yaw: float, pitch: float, roll: float) -> list:
        """
        rotates and displaces the points that make up the vehicle in the NED inertial space.
        calculates the points in ENU frame for display. Also performs the same computation for the axis
        at the origin of the vehicle

        :param x:   north displacement (Pn) [m]
        :param y:   east displacement (Pe) [m]
        :param z:   down displacement (Pn) [m]
        :param yaw:     rotation about the intertial down [rad]
        :param pitch:   rotation about the intermidiate y-axis [rad]
        :param roll:    rotation about the body x-axis [rad]

        :return newPoints: new group of vertices
        :return newAxes: new set of axes
        :return newOrigin: new vehicle origin
        """

        verticesNED = [] # vehicle points expressed in the NED frame
        axisNED = [] # vehicle axes expressed in the NED frame
        
        # express the body points in the inertial frame
        body2Inertial = euler2Quat(yaw = yaw,
                                   pitch = pitch,
                                   roll = roll)
        inertial2Body = quatConjugate(body2Inertial) # quaternion conjugate

        for point in self.vertices:
            pureQuat = [0, *point]
            pointNED = quatMult(quatMult(body2Inertial, pureQuat), inertial2Body)

            # apply the translational offset and append to the new points
            verticesNED.append([pointNED[1]+x, pointNED[2]+y, pointNED[3]+z])
        
        for ax in self.axes:
            pureQuat = [0, *ax]
            axNED = quatMult(quatMult(body2Inertial, pureQuat), inertial2Body)
            axisNED.append([axNED[1]+x, axNED[2]+y, axNED[3]+z])

        verticesENU = ned2enu(verticesNED)
        axesENU = ned2enu(axisNED)
        originENU = ned2enu([[x, y, z]]) # index by 0 to get the list [x, y, z]

        return (verticesENU, axesENU, originENU[0])