"""CCEES sheet 01

Plots for exercises 1, 4 and 5
"""

import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import numpy as np


def f1(u, params):
    """System for exercise 1"""

    return (u[1] - (1.8 * u[0]) ** 2 * np.exp(-u[0]), (0.7 + 0.5 * u[0]) ** (-2) - u[1])


def f4(u, params):
    """System for exercise 4"""

    return params["mu"] - u[0]**2


def f5(u, params):
    """System for exercise 5"""

    return -u[0] * ((u[0] ** 2 - 1) ** 2 - params["mu"] - 1)


def explicitEuler(f, u, deltaT):
    """Euler method, numerical procedure for solving ordinary differential equations"""

    return np.array(u) + deltaT * np.array(f(u))


def generate(u0, t0, deltaT, method, f, **cfg):
    """Generate plot data via iteration"""

    # Set default values for arguments
    cfg.setdefault("params", None)
    cfg.setdefault("steps", 1000)
    cfg.setdefault("xmin", -10)
    cfg.setdefault("xmax", 10)
    cfg.setdefault("ymin", -10)
    cfg.setdefault("ymax", 10)
    cfg.setdefault("min", -10)
    cfg.setdefault("max", 10)

    t = np.empty((cfg["steps"],))
    t[0] = t0
    u = np.empty((cfg["steps"], len(u0)))
    u[0] = u0
    GraphT = [t0]
    GraphU1 = [u0[0]]
    GraphU2 = list()
    if len(u0) == 2:
        GraphU2.append(u0[1])
    for i in range(1, cfg["steps"]):
        t[i] = t[i - 1] + deltaT
        GraphT.append(GraphT[-1] + deltaT)
        if len(GraphU2) > 0:
            us = np.array([GraphU1[-1], GraphU2[-1]])
        else:
            us = np.array([GraphU1[-1]])
        un = method(lambda u: f(u, cfg["params"]), us, deltaT)
        u[i] = method(lambda u: f(u, cfg["params"]), u[i - 1], deltaT)
        GraphU1.append(un[0])
        if len(un) > 1:
            GraphU2.append(un[1])

        if any(u[i] < cfg["min"]) or any(u[i] > cfg["max"]):
            break
        # TODO Kommentar
        #if len(GraphU2) == 0 and (GraphU1[-1] > cfg["ymax"] or GraphU1[-1] < cfg["ymin"]):
        #    break
        ## TODO Kommentar
        #if len(GraphU2) > 0 and (GraphU1[-1] > cfg["xmax"] or GraphU1[-1] < cfg["xmin"] or GraphU2[-1] > cfg["ymax"] or GraphU2[-1] < cfg["ymin"]):
        #    break

    t = t[:i + 1]
    u = u[:i + 1]
    return (t, *[u[:, i] for i in range(len(u0))])
    return GraphT, GraphU1, GraphU2


if __name__ == "__main__":

    # Exercise 1
    # a)
    plt.close()
    for deltaT in np.geomspace(0.0001, 1, 5):
        steps = int(100 / deltaT)
        _, GraphU1, GraphU2 = generate([0, 0], 0, deltaT, explicitEuler, f1, steps=steps)
        plt.plot(GraphU1, GraphU2, label=r"$\Delta\tau=$" + str(deltaT), linewidth=0.3)
    plt.legend(loc="best")
    plt.savefig("ex1a.png", dpi=300)

    # b) Square
    plt.close()
    for u1 in np.linspace(0, 2, 10):
        for u2 in np.linspace(0, 2, 10):
            if u1 not in [0, 2] and u2 not in [0, 2]:
                continue
            _, GraphU1, GraphU2 = generate([u1, u2], 0, 0.01, explicitEuler, f1)
            plt.plot(GraphU1, GraphU2, linewidth=0.3)
    plt.savefig("ex1bsquare.png", dpi=300)

    # b) Circle
    plt.close()
    for phi in np.linspace(0, 2*np.pi, 16):
        u1 = 1 + np.cos(phi)
        u2 = 1 + np.sin(phi)
        _, GraphU1, GraphU2 = generate([u1, u2], 0, 0.01, explicitEuler, f1)
        plt.plot(GraphU1, GraphU2, linewidth=0.3)
    plt.savefig("ex1bcircle.png", dpi=300)

    # Exercise 4
    for mu in [-1, 0, 1]:
        plt.close()
        #for u in np.linspace(-4, 4, 40):
        for u in np.arange(-4, 4, 0.2):
            GraphT, GraphU = generate([u], 0, 0.001, explicitEuler, f4, params={"mu": mu}, steps=2000, ymin=-50, ymax=50, min=-50, max=50)
            plt.plot(GraphT, GraphU, linewidth=0.3)
        plt.savefig("ex4_mu={}.png".format(mu), dpi=300)

    # Exercise 5
    for mu in [-1, 0, 1]:
        plt.close()
        for u in np.linspace(-4, 4, 40):
            GraphT, GraphU = generate([u], 0, 0.001, explicitEuler, f5, params={"mu": mu}, steps=2000, ymin=-50, ymax=50, min=-50, max=50)
            plt.plot(GraphT, GraphU, linewidth=0.3)
        plt.savefig("ex5_mu={}.png".format(mu), dpi=300)
