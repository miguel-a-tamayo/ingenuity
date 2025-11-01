"""
Author: Miguel Tamayo

states.py
Defines the vehicle states for position and orientation. Defined in NED frame
"""

import numpy as np

class VehicleState:
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
                 u: float = 0.0,
                 v: float = 0.0,
                 w: float = 0.0):

        # position 
        self.pn = pn
        self.pe = pe
        self.pd = pd

        # Velocities
        self.u = u
        self.v = v
        self.w = w
    
    def __eq__(self, other):
        if isinstance(other, type(self)):
            if not all([np.allclose(getattr(self, attribute), getattr(other, attribute), atol=1e-8)
                        for attribute in ['pn', 'pe', 'pd', 'u', 'v', 'w']]):
                return False
            
            return True
        
        else:
            raise ValueError(f"Other is not type {type(self)}")


