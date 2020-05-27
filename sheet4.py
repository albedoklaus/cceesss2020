"""CCEES sheet 01

Plots for exercises 1, 4 and 5
"""

import matplotlib.pyplot as plt
import numpy as np


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

def periodicBoundary2(y):
    for i in range(len(y)):
        if y[i] <= -np.pi:
            y[i:]+= 2*np.pi
        elif y[i] > np.pi:
            y[i:]-= 2*np.pi
    return y

def plot(file):
    data = np.load(file)
    print(data)
    GraphU1 = data["array1"]
    GraphU2 = data["array2"]
    stroboscope, deltaT = data["array3"]
    stroboscope = int(stroboscope)
    plt.close()
    plt.plot(periodicBoundary(GraphU1)[::stroboscope], GraphU2[::stroboscope], label=r"$\Delta\tau=$" + str(deltaT/np.pi) + r"$\pi$", linestyle="", linewidth=0.3, marker=".", markersize=0.25)
    plt.legend()
    plt.savefig("sheet04_ex4.png", dpi=300)

if __name__ == "__main__":
    # Exercise 4

    omega = 0.8
    stroboscope = 1000
    steps = 5e8
    deltaT = 2*np.pi / omega / stroboscope
    SpinUp = generate([0, 0, 0], 0, deltaT, explicitEuler, f, steps=400, params={"gamma" : 0.1, "mu" : 1.15, "omega" : omega})
    GraphU1, GraphU2, GraphT = generate(np.array(SpinUp).T[-1], 0, deltaT, explicitEuler, f, steps=int(steps), params={"gamma" : 0.1, "mu" : 1.15, "omega" : omega})
    np.savez_compressed("data{}.npz".format(steps), array1=GraphU1, array2=GraphU2, array3=np.array([stroboscope, deltaT]))
