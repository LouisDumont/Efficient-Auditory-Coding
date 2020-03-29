import numpy as np
import matplotlib.pyplot as plt

from sound import *

def plot_sound(sound, title=None):
    '''
    Plots the samples of a Sound object
    '''
    fig = plt.figure()
    plt.plot(range(sound._len), sound._samples)
    if title: plt.title(title)
    plt.show()

def draw_spikes(spike_list, title=None):
    fig = plt.figure()
    max_coeff = abs(max(spike_list, key=lambda x: abs(x[1]))[1])
    for i, (spike_idx, coeff, position) in enumerate(spike_list):
        if coeff > 0: color='r'
        else: color='b'
        if title: plt.title = title
        intensity = abs(coeff)/max_coeff
        plt.scatter(position, spike_idx, color=color, alpha=intensity)
    return fig

def plot_spikes(spike_list, title=None):
    '''
    Graphical representation of a set of spikes (to check that original spikes were found)
    '''
    fig = draw_spikes(spike_list, title)
    plt.show()

def plot_sounds(sounds, labels, title=None):
    fig = plt.figure()
    assert len(sounds)==len(labels)

    for i, sound in enumerate(sounds):
        plt.plot(range(sound._len), sound._samples, label=labels[i])
    
    if title: plt.title(title)
    plt.legend()
    plt.show()

def compare_spikes(target, pred):
    y_max = max(max(target, key=lambda x: abs(x[0]))[0], max(pred, key=lambda x: abs(x[0]))[0])
    x_max = max(max(target, key=lambda x: abs(x[2]))[2], max(pred, key=lambda x: abs(x[2]))[2])

    plt.subplot(2,1,1)
    axes = plt.gca()
    axes.set_xlim([-0.5,x_max+1])
    axes.set_ylim([-0.5,y_max+1])
    
    max_coeff = abs(max(target, key=lambda x: abs(x[1]))[1])
    for i, (spike_idx, coeff, position) in enumerate(target):
        if coeff > 0: color='r'
        else: color='b'
        intensity = abs(coeff)/max_coeff
        plt.scatter(position, spike_idx, color=color, alpha=intensity)

    plt.subplot(2,1,2)
    axes = plt.gca()
    axes.set_xlim([-0.5,x_max+1])
    axes.set_ylim([-0.5,y_max+1])
    
    max_coeff = abs(max(pred, key=lambda x: abs(x[1]))[1])
    for i, (spike_idx, coeff, position) in enumerate(pred):
        if coeff > 0: color='r'
        else: color='b'
        intensity = abs(coeff)/max_coeff
        plt.scatter(position, spike_idx, color=color, alpha=intensity)

    plt.show()


