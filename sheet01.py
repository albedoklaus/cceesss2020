import matplotlib.pyplot as plt
import numpy as np

def system1(u, params):
    """System for exercise 1"""
    return [u[1] - (1.8 * u[0])**2 * np.exp(-u[0]), (0.7 + 0.5 * u[0])**(-2) - u[1]]

def system4(u, params):
    """System for exercise 4"""
    return params["mu"] - u[0]**2

def system5(u, params):
    """System for exercise 5"""
    return -u[0] * ((u[0]**2 - 1)**2 - params["mu"] - 1)

def explicitEuler(f, u, deltaT):
    return u + deltaT * np.array(f(u))

def graph(u0, t0, deltaT, integration, f, bounds={"steps" : 1000, "xmin" : -10, "xmax" : 10, "ymin" : -10, "ymax" : 10}, params=None):
    GraphT = [t0]
    GraphU1 = [u0[0]]
    GraphU2 = list()
    if len(u0) == 2:
        GraphU2.append(u0[1])
    while True:
        GraphT.append(GraphT[-1] + deltaT)
        if len(GraphU2) > 0:
            us = np.array([GraphU1[-1], GraphU2[-1]])
        else:
            us = np.array([GraphU1[-1]])
        un = integration(lambda u: f(u, params), us, deltaT)
        GraphU1.append(un[0])
        if len(un) > 1:
            GraphU2.append(un[1])

        if len(GraphT) > bounds["steps"]:
            break
        if len(GraphU2) == 0 and (GraphU1[-1] > bounds["ymax"] or GraphU1[-1] < bounds["ymin"]):
            break
        if len(GraphU2) > 0 and (GraphU1[-1] > bounds["xmax"] or GraphU1[-1] < bounds["xmin"] or GraphU2[-1] > bounds["ymax"] or GraphU2[-1] < bounds["ymin"]):
            break

    return GraphT, GraphU1, GraphU2

#Ex1
#a
plt.close()
for deltaT in np.geomspace(0.0001, 1, 5):
    _, GraphU1, GraphU2 = graph([0, 0], 0, deltaT, explicitEuler, ex1, bounds={"steps" : 100/deltaT, "xmin" : -10, "xmax" : 10, "ymin" : -10, "ymax" : 10})
    plt.plot(GraphU1, GraphU2, label=r'$\Delta\tau=$' + str(deltaT), linewidth=0.3)
plt.legend(loc="best")
plt.savefig("ex1a.png", dpi=300)

#b
plt.close()
for u1 in np.linspace(0, 2, 10):
    for u2 in np.linspace(0, 2, 10):
        if u1 not in [0, 2] and u2 not in [0, 2]:
            continue
        _, GraphU1, GraphU2 = graph([u1, u2], 0, 0.01, explicitEuler, ex1)
        plt.plot(GraphU1, GraphU2, linewidth=0.3)
plt.savefig("ex1bsquare.png", dpi=300)

plt.close()
for phi in np.linspace(0, 2*np.pi, 16):
    u1 = 1 + np.cos(phi)
    u2 = 1 + np.sin(phi)
    _, GraphU1, GraphU2 = graph([u1, u2], 0, 0.01, explicitEuler, ex1)
    plt.plot(GraphU1, GraphU2, linewidth=0.3)
plt.savefig("ex1bcircle.png", dpi=300)

#Ex4
for mu in [-1, 0, 1]:
    plt.close()
    #for u in np.linspace(-4, 4, 40):
    for u in np.arange(-4, 4, 0.2):
        GraphT, GraphU, _ = graph([u], 0, 0.001, explicitEuler, ex4, params={"mu" : mu}, bounds={"steps" : 2000, "xmin" : -10, "xmax" : 10, "ymin" : -50, "ymax" : 50})
        plt.plot(GraphT, GraphU, linewidth=0.3)
    plt.savefig("ex4_mu={}.png".format(mu), dpi=300)

#Ex5
for mu in [-1, 0, 1]:
    plt.close()
    for u in np.linspace(-4, 4, 40):
        GraphT, GraphU, _ = graph([u], 0, 0.001, explicitEuler, ex5, params={"mu" : mu}, bounds={"steps" : 2000, "xmin" : -10, "xmax" : 10, "ymin" : -50, "ymax" : 50})
        plt.plot(GraphT, GraphU, linewidth=0.3)
    plt.savefig("ex5_mu={}.png".format(mu), dpi=300)
