"""
Author: Miguel Tamayo

integrator.py
Defines an RK4 integrator that is used for various states in the simulation
"""

import numpy as np

def integrateRk4(derivative: callable, state: np.array, t: float, dt: float, *args) -> np.array:
    """
    integrateRk4(derivative: callable, state: np.array, t: float, dt: float, *args)

    Integrates a statte using Runge-Kutta "RK4" method

    :param derivative: callable function that calculates the state derivative
    :param state: current state in vector form at current time step k.
    :param t: initial time
    :param dt: time step to iterate over
    :param *args: any additional parameters that the derivative function takes
    """

    k1 = derivative(t, state, *args)
    k2 = derivative(t + (dt / 2.0), state + dt * (k1 / 2.0), *args)
    k3 = derivative(t + (dt / 2.0), state + dt * (k2 / 2.0), *args)
    k4 = derivative(t + dt, state + (dt * k3))

    return state + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)