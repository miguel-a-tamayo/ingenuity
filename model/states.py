"""
Author: Miguel Tamayo

states.py
Defines the vehicle states for position and orientation. Defined in NED frame
"""

class VehicleStates:
    """
    Class defining vehicle states

    :param pn: initial north position [m]
    :param pe: initial east position [m]
    :param pd: initial down position [m]

    :param yaw: initial yaw rotation [rad]
    :param pitch: initial pitch rotation [rad]
    :param roll: initial roll rotation [rad]
    """
    def __init__(self,
                 pn: float = 0.0,
                 pe: float = 0.0,
                 pd: float = 0.0,
                 yaw: float = 0.0,
                 pitch: float = 0.0,
                 roll: float = 0.0):

        # position 
        self.pn = pn
        self.pe = pe
        self.pd = pd

        # Euler angles
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll