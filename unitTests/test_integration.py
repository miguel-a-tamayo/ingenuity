"""
Author: Miguel Tamayo

test_integration.py
Test the Runge-Kutta RK4 Integrator
"""

import numpy as np

def test_Rk4FirstOrder():
    # test a first order system like an RC cirtuit
    # system: dV = -(1/RC) * V
    # analytical solution: V = V0 * e^(-t/RC)
    pass