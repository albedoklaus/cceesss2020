import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from scipy.integrate import ode


class Timer:
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        self.time = time.time()
    def __exit__(self, exc_type, exc_value, exc_traceback):
        print(self.name, time.time() - self.time)

def f(u, params):
    """Logistic map"""

    u1 = u[0]
    r = 2
    return r * u * (1 - u)


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

steps = 1000000
deltaT = 0.05
y0 = 0.5
t0 = 0
t1 = t0 + steps * deltaT
with Timer("generate"):
    GraphU1 = generate([y0], t0, deltaT, explicitEuler, f, steps=int(steps))

def f_odeint(y, x):
    r = 2
    return r * y * (1 - y)

def f_ode(x, y):
    r = 2
    return r * y * (1 - y)

xs = np.linspace(t0, t1, steps)
with Timer("odeint"):
    ys = odeint(f_odeint, y0, xs)

#r = ode(f_ode).set_integrator('vode', method='bdf')
#r = ode(f_ode).set_integrator('dopri5')
r = ode(f_ode).set_integrator('lsoda')
r.set_initial_value(y0, t0)
yy = []
tt = []

i = 0
yy = np.empty(steps + 1)
tt = np.empty(steps + 1)
with Timer("ode"):
    while r.successful() and r.t < t1:
        tt[i] = r.t + deltaT
        yy[i] = r.integrate(r.t + deltaT)[0]
        i += 1

exit()
plt.plot(xs, ys, linestyle="--")
plt.plot(tt, yy, linestyle="--")
plt.plot(xs, *GraphU1, linestyle="--")
plt.show()
