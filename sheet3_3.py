import itertools
import os
import random

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def logistic_map(u_0=None, mu=4):
    """Logistic map random data
    
    Use the logistic map to generate random numbers. If `u_0` is
    `None`, an arbitrary initial value is being used. Note that
    `mu` can range from 0 to 4.
    """

    if u_0 is None:
        u_0 = random.random()

    u_i = u_0
    while True:
        u_i = mu * u_i * (1 - u_i)
        yield u_i


def generate_random_data(n):
    """Generate random data"""

    data = {
        "reference": np.linspace(0, 1, n),
        "os.urandom": [ord(os.urandom(1)) / 255 for _ in range(n)],
        "random.random": [random.random() for _ in range(n)],
        "np.random.rand": np.random.rand(n),
        "logistic_map": list(itertools.islice(logistic_map(), n)),
    }
    return data


if __name__ == "__main__":

    for n in [10, 100, 1000, 10000]:

        data = generate_random_data(n)
        plt.close()
        for method, numbers in data.items():
            plt.plot(sorted(numbers), label=method)
        plt.title(f"{n} random numbers between 0 and 1")
        plt.legend()
        plt.savefig(f"sheet3_plot_n={n}.png")

        plt.close()
        for method, numbers in data.items():
            plt.plot(numbers[:-1], numbers[1:], label=method, linestyle="", marker=".", markersize=2)
        plt.title(f"{n} random numbers between 0 and 1")
        plt.legend()
        plt.savefig(f"sheet3_trans_n={n}.png")
