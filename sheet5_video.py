import os

import matplotlib.pyplot as plt
import numpy as np


def generate_frames(folder):
    os.makedirs(folder, exist_ok=True)
    for i, phi in enumerate(np.linspace(0, 2 * np.pi, 100)):
        plt.close()
        plt.plot([0, np.cos(phi)], [0, np.sin(phi)])
        plt.xlim(-1, 1)
        plt.ylim(-1, 1)
        plt.savefig(os.path.join(folder, f"frame{i}.png"))


def generate_video(folder):
    os.system(" ".join([
        "ffmpeg",
        "-r 25",
        f'-i "{os.path.join(folder, "frame%d.png")}"',
        "-c:v libx264",
        "-pix_fmt yuv420p",
        "-an",
        f"{folder}.mp4",
    ]))


if __name__ == "__main__":

    #generate_frames("test")
    generate_video("test")