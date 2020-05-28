import time

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate

def f1(y, t):
    """System with forcing of first kind"""

    u1 = y[0]
    u2 = y[1]
    u3 = t
    return u2, -2 * params["gamma"] * u2 - np.sin(u1) + params["mu"] * np.sin(params["omega"] * u3)

def periodicBoundary(y):
    offset = 0.0
    for i in range(len(y)):
        while y[i] + offset <= -np.pi:
            offset += 2*np.pi
        while y[i] + offset > np.pi:
            offset -= 2*np.pi
        y[i] = y[i] + offset
    return y

if __name__ == "__main__":

    params={"gamma" : 0.1, "mu" : 0.915, "omega" : 0.8}
    pointCount = int(1e5)
    spinup = 800
    func = f1

    deltaT = 2*np.pi / params["omega"] / 100
    tSpinup = np.linspace(0, spinup * deltaT, spinup)
    ySpinup = scipy.integrate.odeint(func, np.array([1e-9, 1e-9]), tSpinup)
    points = np.empty(shape=(pointCount, 2))
    t = np.linspace(tSpinup[-1], tSpinup[-1] + pointCount * deltaT, pointCount)
    y = scipy.integrate.odeint(func, ySpinup[-1], t)
    
    plt.close()
    plt.plot(tSpinup, ySpinup.T[0], linestyle="", linewidth=0.3, marker=".", markersize=0.25)
    plt.title("Spinup phase; first 800 steps")
    plt.xlabel(r"$t$")
    plt.ylabel(r"$u_1$")
    plt.savefig("trajectory_begin.png", dpi=300)
    
    plt.close()
    plt.plot(periodicBoundary(y.T[0]), y.T[1], linestyle="", linewidth=0.3, marker=".", markersize=0.25, label=r"$\mu=0.915$")
    plt.hlines(0, -np.pi, np.pi)
    plt.vlines(0, -np.pi, np.pi)
    plt.title("Phase diagramm")
    plt.xlabel(r"$u_1$")
    plt.ylabel(r"$u_2$")
    plt.legend()
    plt.savefig("phase800.png", dpi=300)
