import os
import re

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate


def f(y, t, params):
    """System"""

    u1 = y[0]
    u2 = y[1]
    u3 = t
    return u2, -2 * params["gamma"] * u2 - np.sin(u1) + params["mu"] * np.sin(params["omega"] * u3)


def g(y, t, params):
    """System 2nd kind"""

    u1 = y[0]
    u2 = y[1]
    u3 = t
    return u2, -2 * params["gamma"] * u2 - (1 - params["mu"] * np.sin(params["omega"] * u3)) * np.sin(u1)


def periodic_boundary(y):
    """Pendelüberschlag korrigieren"""

    offset = 0.0

    for i in range(len(y)):

        while y[i] + offset <= -np.pi:
            offset += 2*np.pi

        while y[i] + offset > np.pi:
            offset -= 2*np.pi

        y[i] = y[i] + offset

    return y


def generate(f, t0, y0, dt, **opt):
    """Generate"""

    opt.setdefault("caption", "")
    opt.setdefault("params", {})
    opt.setdefault("spinup", 0)
    opt.setdefault("steps", 1000)

    f_ = lambda y, t: f(y, t, opt["params"])

    if opt["spinup"]:
        steps = opt["spinup"]
        t = np.linspace(t0, t0 + steps * dt, steps + 1)
        y = scipy.integrate.odeint(f_, y0, t)
        t0 = t[-1]
        y0 = y[-1]

    steps = opt["steps"]
    t = np.linspace(t0, t0 + steps * dt, steps + 1)
    y = scipy.integrate.odeint(f_, y0, t)

    return t, y


def plot(t, y, **opt):
    """Plot"""

    opt.setdefault("xlim", None)
    opt.setdefault("ylim", None)

    if os.path.isfile(filename(opt) + ".png"):
        return

    y.T[0] = periodic_boundary(y.T[0])
    if opt["xlim"] is not None:
        y.T[0][y.T[0] < opt["xlim"][0]] = np.nan
        y.T[0][y.T[0] > opt["xlim"][1]] = np.nan
    if opt["ylim"] is not None:
        y.T[1][y.T[1] < opt["ylim"][0]] = np.nan
        y.T[1][y.T[1] > opt["ylim"][1]] = np.nan

    plt.close()
    plt.plot(y.T[0][::opt["stroboscope"]], y.T[1][::opt["stroboscope"]], linestyle="", marker=".", markersize=0.2)
    plt.legend()
    plt.savefig(filename(opt) + ".png", dpi=300)


def filename(opt):
    """Dateiname"""

    return "sheet4_" + re.sub(r"[^a-zA-Z0-9.]", "_", str(opt))


def data(f, dt, **opt):
    """Daten"""

    if not os.path.isfile(filename(opt) + ".npz"):
        t, y = generate(f, 0, [0, 0], dt, **opt)
        np.savez_compressed(filename(opt), t=t, y=y)
    else:
        data = np.load(filename(opt) + ".npz")
        t, y = data["t"], data["y"]
    return t, y


if __name__ == "__main__":

    # Exercise 3a
    stroboscope = 1000
    steps = int(1e7)
    omega = 0.8
    dt = 2 * np.pi / omega / stroboscope
    opt = {
        "caption": "ex3a",
        "params": {
            "gamma": 0.1,
            "mu": 1.15,
            "omega": omega,
        },
        "spinup": 400,
        "steps": steps,
        "stroboscope": stroboscope,
    }
    t, y = data(f, dt, **opt)
    plot(t, y, **opt)
    plot(t, y, **opt, xlim=[1.5, 2.5], ylim=[0.5, 1.0])
    plot(t, y, **opt, xlim=[1.9, 2.0], ylim=[0.72, 0.75])

    # Exercise 3b
    stroboscope = 1000
    steps = int(1e7)
    omega = 0.8
    dt = 2 * np.pi / omega / stroboscope
    opt = {
        "caption": "ex3b",
        "params": {
            "gamma": 0.1,
            "mu": 1.15,
            "omega": omega,
        },
        "spinup": 400,
        "steps": steps,
        "stroboscope": stroboscope,
    }
    t, y = data(g, dt, **opt)
    plot(t, y, **opt)

    # Exercise 4
    stroboscope = 1000
    steps = int(1e7)
    omega = 0.8
    dt = 2 * np.pi / omega / stroboscope
    opt = {
        "caption": "ex4",
        "params": {
            "gamma": 0.1,
            "mu": 0.915,
            "omega": omega,
        },
        "spinup": 400,
        "steps": steps,
        "stroboscope": stroboscope,
    }
    t, y = data(f, dt, **opt)
    plot(t, y, **opt)
