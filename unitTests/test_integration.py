"""
Author: Miguel Tamayo

test_integration.py
Test the Runge-Kutta RK4 Integrator
"""

from utilities.integrator import integrateRk4

import matplotlib.pyplot as plt
import numpy as np

def test_Rk4FirstOrder():
    # test a first order system like an RC cirtuit
    # system: dV = -(1.0/RC) * V
    # analytical solution: V = V0 * e^(-t/RC)
    v0 = 5.0
    rc = 10e-1

    t = np.arange(0.0, 5.0, 0.05)
    v_analytical = v0 * np.exp(-t / rc)

    # rk4 solution
    dV = lambda t, V, RC: - (1.0 / RC) * V
    v_rk4 = np.zeros(shape=len(t))
    v_rk4[0] = 5.0
    dt = 0.05
    
    for k in range(0, len(v_rk4)-1):
        state = integrateRk4(dV, v_rk4[k], t[k], dt, rc)
        v_rk4[k+1] = state

    plt.figure(1)
    plt.plot(t, v_analytical, label="Analytical Solution")
    plt.plot(t, v_rk4, linestyle='--')
    plt.grid()
    plt.title("First Order (RC Circuit) System Integration Test")
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.legend(["Analytical Solution", "RK4 Solution"])

def test_Rk4SecondOrder():
    # test a second order system like a mass spring damper
    # m*xdd + c*xd + k*x = 0
    # analytical solution: x = x0*e^(-zeta*wn*t)cos(wd*t) + (x0*zeta*wn/wd)*e^(-zeta*wn*t)sin(wd*t)
    # wn = sqrt(k/m), zeta = c / 2sqrt(m*k)

    def derivative(t, state, k, c, m) -> np.array:
        xd = state[1]
        xdd = -(c * state[1] + k * state[0]) / m

        return np.array([xd, xdd])

    x0 = 1.0 # [m]
    zeta = 0.07
    wn = 2.0 * np.pi * 1.0
    m = 1.0
    wd = wn * np.sqrt(1 - np.square(zeta))
    t = np.arange(0.0, 7.0, 0.01)

    # analytical solution
    x_analytical = x0 * np.exp(-zeta*wn*t)*np.cos(wd*t) + (x0*zeta*wn/wd)*np.exp(-zeta*wn*t)*np.sin(wd*t)
    xd1 = x0*np.exp(-zeta*wn*t)*(-zeta*wn*np.cos(wd*t) - wd*np.sin(wd*t))
    xd2 = (x0*zeta*wn/wd)*np.exp(-zeta*wn*t)*(-zeta*wn*np.sin(wd*t) + wd*np.cos(wd*t))
    xd_analytical = xd1 + xd2

    # rk4 solution
    k = m * np.square(wn)
    c = 2 * zeta * m * wn
    x_rk4 = np.zeros(len(t))
    x_rk4[0] = 1.0
    xd_rk4 = np.zeros(len(t))
    dt = 0.01

    for i in range(0, len(x_rk4)-1):
        state = integrateRk4(derivative, np.array([x_rk4[i], xd_rk4[i]]), t[i], dt, k, c, m)
        x_rk4[i+1] = state[0]
        xd_rk4[i+1] = state[1]

    plt.figure(2)
    plt.title("Second Order (Mass-Spring-Damper) System Integration Test")
    plt.subplot(2, 1, 1)
    plt.plot(t, x_analytical)
    plt.plot(t, x_rk4, linestyle='--')
    plt.grid()
    plt.ylabel("Position [m]")
    plt.legend(["Analytical Solution", "RK4 Solution"])

    plt.subplot(2, 1, 2)
    plt.plot(t, xd_analytical)
    plt.plot(t, xd_rk4, linestyle='--')
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [m/s]")
    plt.legend(["Analytical Solution", "RK4 Solution"])
    plt.show()