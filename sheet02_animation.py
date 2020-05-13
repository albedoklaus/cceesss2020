#import python libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pylab as py 
from functools import partial
from matplotlib import cm
import matplotlib.colors as mcolors
def logistic_map(u_i, mu):
    '''Define logistic map, note that mu can range from 0 to 4'''
    return mu*u_i*(1-u_i)

#Sweeping range for mu
#mu_0 = 0
#mu_1 = 4
#N_mu = 1000

#Initial value for u
#u_0  = 0.5

#Number of iterations for spinup
#N_Spinup = 4000

#Number of data points collected after spinup for each value of mu
#N_sample = 10

#Total number of data points collected
#N_hits



def compute_bifurcation(mu_0 = 0, mu_1 = 4, N_mu = 1000, N_sample = 10, N_spinup = 0, u_0 = 0.5):
    '''Compute values of u with parameter sweeps over mu and u_0
       Return a tuple of array with computed values of mu and u'''
    #Arrays for storing results of computation
    N_hits = N_mu*N_sample
    mu_array = np.zeros(N_hits)
    u_array = np.zeros(N_hits)

    #Loop over possible values for mu
    for n in range(0, N_mu):
        mu = mu_0 + n*(mu_1 - mu_0)/N_mu
        #Spinup
        u = u_0
        for i in range(0, N_spinup):
            u = logistic_map(u, mu)

        #Compute a further N_u iterations of logistic map and store results
        for j in range(0, N_sample):
            u = logistic_map(u, mu)
            mu_array[n*N_sample + j] = mu
            u_array[n*N_sample + j]  = u

    return [mu_array, u_array]


def plot_simple_bifurcation_diagram(mu, u):
    plt.figure(figsize=(11.69, 8.27), dpi=200)
    plt.xlabel(r"$\mu$")
    plt.ylabel(r"$u$")
    plt.ylim(0, 1)
    plt.xlim(0,4)
    plt.title(r'Bifurcation diagram for logistic map')
    plt.scatter(mu, u, s=0.1, lw=0.2, marker='.', color='grey')

    plt.fill_between([3, 0], [1, 1],
                         alpha=0.1, label='stationary')
    plt.fill_between([3.56995, 3], [1, 1],
                         alpha=0.1, label='periodic')
    plt.fill_between([4, 3.56995], [1, 1],
                         alpha=0.1, label='chaotic')
    plt.legend()
    plt.savefig("sheet02_mu0.3.png", dpi=600)

mu_result, u_result = compute_bifurcation(N_sample = 10)
plot_simple_bifurcation_diagram(mu_result, u_result)

# Animation

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure(figsize=(11.69, 8.27), dpi=200)
plt.xlabel(r"$\mu$")
plt.ylabel(r"$u$")
plt.ylim(0, 1)
plt.xlim(0,4)
plt.title(r'Bifurcation diagram for logistic map')
plt.fill_between([3, 0], [1, 1],
                     alpha=0.1, label='stationary')
plt.fill_between([3.56995, 3], [1, 1],
                     alpha=0.1, label='periodic')
plt.fill_between([4, 3.56995], [1, 1],
                     alpha=0.1, label='chaotic')
plt.legend()

artists = []
for u_0 in np.linspace(0.1, 0.9, 50):
    mu_result, u_result = compute_bifurcation(N_sample=10, u_0=u_0)
    artists.append(plt.plot(mu_result, u_result, linestyle="", marker=".", color="red"))

ani = animation.ArtistAnimation(fig, artists, interval=100, blit=True)
ani.save("animation.mp4")

