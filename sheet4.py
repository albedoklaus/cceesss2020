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


def f(u, params):
    """System for exercise 1"""

    u1 = u[0]
    u2 = u[1]
    u3 = u[2]
    return u2, -2 * params["gamma"] * u2 - np.sin(u1) + params["mu"] * np.sin(params["omega"] * u3), 1


def explicitEuler(f, u, deltaT):
    """Euler method, numerical procedure for solving ordinary differential equations"""

    return np.array(u) + deltaT * np.array(f(u))


def generate(u0, t0, deltaT, method, f, **cfg):
    """Generate plot data via iteration"""

    # Set default values for arguments
    cfg.setdefault("params", None)
    cfg.setdefault("steps", 1000)
    cfg.setdefault("min", -np.inf)
    cfg.setdefault("max", np.inf)

    # Initialize arrays
    t = np.empty((cfg["steps"],))
    t[0] = t0
    u = np.empty((cfg["steps"], len(u0)))
    u[0] = u0

    # Iterate
    for i in range(1, cfg["steps"]):
        if not i % 1000:
            print("{:.2f}%".format(i/cfg["steps"]*100), end="\r")
        u[i] = method(lambda u: f(u, cfg["params"]), u[i - 1], deltaT)
        if any(u[i] < cfg["min"]) or any(u[i] > cfg["max"]):
            break

    # Crop array if necessary and return
    u = u[:i + 1]
    return [u[:, i] for i in range(len(u0))]


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
    stroboscope, deltaT = data["array3"]
    stroboscope = int(stroboscope)
    plt.close()
    if x is not None:
        GraphU1[GraphU1 < x[0]] = np.nan
        GraphU1[GraphU1 > x[1]] = np.nan
    if y is not None:
        GraphU2[GraphU2 < y[0]] = np.nan
        GraphU2[GraphU2 > y[1]] = np.nan
    plt.plot(GraphU1[::stroboscope], GraphU2[::stroboscope], label=r"$\Delta\tau=$" + str(deltaT/np.pi) + r"$\pi$", linestyle="", linewidth=0.3, marker=".", markersize=0.25)
    plt.legend()
    plt.savefig(filename + f"x={x}_y={y}.png", dpi=300)


if __name__ == "__main__":

    omega = 0.8
    stroboscope = 1000
    steps = int(1e7)
    deltaT = 2*np.pi / omega / stroboscope
    params={"gamma" : 0.1, "mu" : 1.15, "omega" : omega}
    filename = "data{}.npz".format(steps)
    SpinUp = generate([0, 0, 0], 0, deltaT, explicitEuler, f, steps=400, params=params)
    #with Timer("generate"):
    #    GraphU1, GraphU2, GraphT = generate(np.array(SpinUp).T[-1], 0, deltaT, explicitEuler, f, steps=steps, params=params)
    #np.savez_compressed(filename, array1=GraphU1, array2=GraphU2, array3=np.array([stroboscope, deltaT]))
    #plot(filename)


    # Faster ODE solver scipy.integrate.odeint

    def f(y, t):
        """System for exercise 1"""

        u1 = y[0]
        u2 = y[1]
        u3 = t
        return u2, -2 * params["gamma"] * u2 - np.sin(u1) + params["mu"] * np.sin(params["omega"] * u3)

    #y0 = np.array(SpinUp).T[-1][0:2]
    #t0 = np.array(SpinUp).T[-1][2]
    #t = np.linspace(t0, t0 + steps * deltaT, steps)
    #with Timer("odeint"):
    #    y = scipy.integrate.odeint(f, y0, t)
    filename = "data_new{}.npz".format(steps)
    #np.savez_compressed(filename, array1=y.T[0], array2=y.T[1], array3=np.array([stroboscope, deltaT]))
    #plot(filename)
    #plot(filename, x=[0, 0.2], y=[1.7, 1.9])
    #plot(filename, x=[1.8, 2.0], y=[0.5, 0.7])
    plot(filename, x=[1.5, 2.5], y=[0.5, 1.0])
    plot(filename, x=[1.9, 2.0], y=[0.72, 0.75])

