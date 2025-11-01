"""
Author: Miguel Tamayo

inputs.py
File that contains classes that define inputs to various parts of the simulation
"""

import numpy as np

class Force:
    """
    Class defines a force vector [N]. Force is defined in the body-frame and assumed to be
    located in the center of mass

    :param x: force in body-x direction [N]
    :param y: force in body-y direction [N]
    :param z: force in body-z direction [N]
    """
    def __init__(self,
                 x = 0.0,
                 y = 0.0,
                 z = 0.0):

        self.x = x 
        self.y = y
        self.z = z

    def __add__(self, other: Force) -> Force:
        if isinstance(other, type(self)):
            return Force(self.x + other.x, self.y + other.y, self.z + other.z)
        
        else:
            raise ValueError(f"Other is not type {type(self)}")
    
    def vector(self) -> np.array:
        """
        Returns the vector representation of this force

        :return force: numpy array with the force elements
        """

        return np.array([self.x, self.y, self.z])

class Moment:
    """
    Class defines a moment vector [N-m]. Moment is defined in the body-frame and assumed to be located
    in the center of mass

    :param Mx: moment about body-x direction [N-m]
    :param My: moment about body-y direction [N-m]
    :param Mz: moment about body-z direction [N-m]
    """
    def __init__(self,
                 Mx = 0.0,
                 My = 0.0,
                 Mz = 0.0):
        
        self.Mx = Mx
        self.My = My
        self.Mz = Mz

    def __add__(self, other: Moment) -> Moment:
        if isinstance(other, type(self)):
            return Moment(self.Mx + other.Mx, self.My + other.My, self.z + other.Mz)
        
        else:
            raise ValueError(f"Other is not type {type(self)}")

    def getVector(self) -> np.array:
        """
        Returns the vector representation of this moment

        :return moment: numpy array with the moment elements
        """

        return np.array([self.Mx, self.My, self.Mz])

