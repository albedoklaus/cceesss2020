import time

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate


class Timer:
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        self.time = time.time()
    def __exit__(self, exc_type, exc_value, exc_traceback):
        print(self.name, time.time() - self.time)

def f1(y, t):
    """System with forcing of first kind"""

    u1 = y[0]
    u2 = y[1]
    u3 = t
    return u2, -2 * params["gamma"] * u2 - np.sin(u1) + params["mu"] * np.sin(params["omega"] * u3)

def f2(y, t):
    """System with forcing of second kind"""

    u1 = y[0]
    u2 = y[1]
    u3 = t
    return u2, -2 * params["gamma"] * u2 - (1 - params["mu"] * np.sin(params["omega"] * u3)) * np.sin(u1)

def periodicBoundary(y):
    offset = 0.0
    for i in range(len(y)):
        while y[i] + offset <= -np.pi:
            offset += 2*np.pi
        while y[i] + offset > np.pi:
            offset -= 2*np.pi
        y[i] = y[i] + offset
    return y


def plot(filename, x=None, y=None):
    data = np.load(filename)
    GraphU1 = np.array(data["array1"])
    GraphU1 = periodicBoundary(GraphU1)
    GraphU2 = np.array(data["array2"])
    deltaT = data["array3"][0]
    plt.close()
    if x is not None:
        GraphU1[GraphU1 < x[0]] = np.nan
        GraphU1[GraphU1 > x[1]] = np.nan
    if y is not None:
        GraphU2[GraphU2 < y[0]] = np.nan
        GraphU2[GraphU2 > y[1]] = np.nan
    plt.plot(GraphU1, GraphU2, label=r"$\Delta\tau=$" + str(deltaT/np.pi) + r"$\pi$", linestyle="", linewidth=0.3, marker=".", markersize=0.25)
    plt.legend()
    plt.savefig(filename + f"x={x}_y={y}.png", dpi=300)


if __name__ == "__main__":

    params={"gamma" : 0.1, "mu" : 0.915, "omega" : 0.8}
    pointCount = int(1e5)
    spinup = 40000
    func = f1

    deltaT = 2*np.pi / params["omega"] / 100
    tSpinup = np.linspace(0, spinup * deltaT, spinup)
    ySpinup = scipy.integrate.odeint(func, np.array([1e-9, 1e-9]), tSpinup)
    points = np.empty(shape=(pointCount, 2))
    with Timer("Test"):
        t = np.linspace(tSpinup[-1], tSpinup[-1] + pointCount * deltaT, pointCount)
        y = scipy.integrate.odeint(func, ySpinup[-1], t)
    
    plt.close()
    plt.plot(tSpinup[:800], ySpinup.T[0][:800], linestyle="", linewidth=0.3, marker=".", markersize=0.25)
    plt.title("Spinup phase; first 800 steps")
    plt.xlabel(r"$t$")
    plt.ylabel(r"$u_1$")
    plt.savefig("trajectory_begin.png", dpi=300)

    plt.close()
    plt.plot(tSpinup, ySpinup.T[0], linestyle="", linewidth=0.3, marker=".", markersize=0.25)
    plt.title("Spinup phase; all 40000 steps")
    plt.xlabel(r"$t$")
    plt.ylabel(r"$u_1$")
    plt.savefig("trajectory.png", dpi=300)
    
    plt.close()
    plt.plot(periodicBoundary(y.T[0]), y.T[1], linestyle="", linewidth=0.3, marker=".", markersize=0.25, label=r"$\mu=0.915$")

    params={"gamma" : 0.1, "mu" : 0.90, "omega" : 0.8}
    pointCount = int(1e5)
    spinup = 40000
    func = f1

    deltaT = 2*np.pi / params["omega"] / 100
    tSpinup = np.linspace(0, spinup * deltaT, spinup)
    ySpinup = scipy.integrate.odeint(func, np.array([1e-9, 1e-9]), tSpinup)
    points = np.empty(shape=(pointCount, 2))
    with Timer("Test"):
        t = np.linspace(tSpinup[-1], tSpinup[-1] + pointCount * deltaT, pointCount)
        y = scipy.integrate.odeint(func, ySpinup[-1], t)
    plt.plot(periodicBoundary(y.T[0]), y.T[1], linestyle="", linewidth=0.3, marker=".", markersize=0.25, label=r"$\mu=0.90$")

    params={"gamma" : 0.1, "mu" : 0.92, "omega" : 0.8}
    pointCount = int(1e5)
    spinup = 40000
    func = f1

    deltaT = 2*np.pi / params["omega"] / 100
    tSpinup = np.linspace(0, spinup * deltaT, spinup)
    ySpinup = scipy.integrate.odeint(func, np.array([1e-9, 1e-9]), tSpinup)
    points = np.empty(shape=(pointCount, 2))
    with Timer("Test"):
        t = np.linspace(tSpinup[-1], tSpinup[-1] + pointCount * deltaT, pointCount)
        y = scipy.integrate.odeint(func, ySpinup[-1], t)
    plt.plot(periodicBoundary(y.T[0]), y.T[1], linestyle="", linewidth=0.3, marker=".", markersize=0.25, label=r"$\mu=0.92$")
    plt.hlines(0, -np.pi, np.pi)
    plt.vlines(0, -np.pi, np.pi)
    plt.title("Phase diagramm")
    plt.xlabel(r"$u_1$")
    plt.ylabel(r"$u_2$")
    plt.legend()
    plt.savefig("phase.png", dpi=300)

"""
Looking at the first 800 steps of iteration suggests that the spinup phase is already sufficently long for the system to be converged.\\
Even looking at the first 40000 steps reveals no significant chances later on.
But by checking the phase diagramm after a 800 step spinup phase one can see that it has not fully converged yet whereas 40000 steps as a spinup phase are more than enough to fully converge.

The Periodicity has already been discovered in exercise 3, where the phase diagramm was plotted after applying a stroboscope. There, three distinct points can be observed (the trails again mean that is hasn't fully converged yet).

The phase diagramm shows that for \mu=0.90 the diagramm is roughly symmetric while with increasing \mu it shifts to the left. However, this trend violated by the splitting of lines e.g. the transition from a period 3 to a period 5 orbit seen at \mu=0.92.
"""
