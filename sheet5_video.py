import os

import matplotlib.pyplot as plt
import numpy as np


def generate_frames(dest="temp"):
    os.makedirs(dest, exist_ok=True)
    for i, phi in enumerate(np.linspace(0, 2 * np.pi, 100)):
        plt.close()
        plt.plot([0, np.cos(phi)], [0, np.sin(phi)])
        plt.xlim(-1, 1)
        plt.ylim(-1, 1)
        plt.savefig(os.path.join(dest, f"frame{i}.png"))


def generate_video(dest="temp"):
    os.system(" ".join([
        "ffmpeg",
        "-r 20",
        f'-i "{os.path.join(dest, "frame%d.png")}"',
        "-c:v libx264",
        "-pix_fmt yuv420p",
        "-an",
        "-filter:v scale=620:-1",
        f"{dest}.mp4",
    ]))

def rename(src, regexfilename, dest="temp"):
    os.makedirs(dest, exist_ok=True)
    from os import listdir
    from os.path import isfile, join
    files = [f for f in listdir(src) if isfile(join(src, f))]
    import re
    numbers = {float(re.match(regexfilename, file).group(1)) : file for file in files if re.match(regexfilename, file) is not None}
    keys = sorted(numbers.keys())
    for i in range(len(numbers.keys())):
        from shutil import copyfile
        copyfile(os.path.join(src, numbers[keys[i]]), os.path.join(dest, "frame{}.png".format(i)))

if __name__ == "__main__":
    #generate_frames()
    rename("Data", r"bitmap_r([0-9]+\.[0-9]+).png")
    generate_video()