import numpy as np
import matplotlib.pyplot as plt

from sound import *

def plot_sound(sound):
    fig = plt.figure()
    plt.plot(range(sound._len), sound._samples)
    plt.show()