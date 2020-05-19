import random
from os import urandom

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
plt.rcParams['animation.ffmpeg_path'] = r'A:\\Software\\ffmpeg'

def logistic_map(u_i, mu):
    '''Define logistic map, note that mu can range from 0 to 4'''
    return mu*u_i*(1-u_i)

def osrandom():
    return ord(urandom(1)) / 256

def randoms(n):
    rnd = [random.random()]
    ornd = [osrandom()]
    lmap = [random.random()]
    for _ in range(n):
        rnd.append(random.random())
        ornd.append(osrandom())
        lmap.append(logistic_map(lmap[-1], 4))
    rnd.sort()
    ornd.sort()
    lmap.sort()
    return rnd, ornd, lmap

for n in [1000, 10000]:
    rnd, ornd, lmap = randoms(n)
    plt.close()
    plt.plot(rnd, color="orange", label="Random Function")
    plt.plot(ornd, color="blue", label="OS Random")
    plt.plot(lmap, color="green", label="Logistic Map")
    plt.savefig("Plot_n={}".format(n))

fig = plt.figure(figsize=(11.69, 8.27), dpi=200)
artists = []
plt.close()
plt.plot(0, color="orange", label="Random Function")
plt.plot(0, color="blue", label="OS Random")
plt.plot(0, color="green", label="Logistic Map")
plt.legend(loc="best")

count = 10
for i in range(100):
    if count < int(np.exp(i/10)):
        count =  int(np.exp(i/10))
        rnd, ornd, lmap = randoms(count)
        artists.append(plt.plot(np.linspace(0, 1, len(rnd)), rnd, color="orange"))
        artists.append(plt.plot(np.linspace(0, 1, len(ornd)), ornd, color="blue"))
        artists.append(plt.plot(np.linspace(0, 1, len(lmap)), lmap, color="green"))

ani = animation.ArtistAnimation(fig, artists, interval=100, blit=True)
ani.save("sheet2_animation.mp4")
