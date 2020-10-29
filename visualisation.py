import numpy as np
import matplotlib.pyplot as plt

from sound import *


def plot_sound(sound, title=None, save=None):
    '''
    Plots the samples of a Sound object
    '''
    fig = plt.figure()
    plt.plot(range(sound._len), sound._samples)
    if title:
        plt.title(title)
    plt.show()


def draw_spikes(spike_list, title=None, save=None):
    fig = plt.figure()
    max_coeff = abs(max(spike_list, key=lambda x: abs(x[1]))[1])
    for i, (spike_idx, coeff, position) in enumerate(spike_list):
        if coeff > 0:
            color = 'r'
        else:
            color = 'b'
        if title:
            plt.title = title
        intensity = abs(coeff)/max_coeff
        plt.scatter(position, spike_idx, color=color, alpha=intensity)
    return fig


def plot_spikes(spike_list, title=None, save=None):
    '''
    Graphical representation of a set of spikes (to check that original spikes were found)
    '''
    fig = draw_spikes(spike_list, title)
    plt.show()


def plot_sounds(sounds, labels, title=None, save=None):
    fig = plt.figure()
    assert len(sounds) == len(labels)

    for i, sound in enumerate(sounds):
        plt.plot(range(sound._len), sound._samples, label=labels[i])

    if title:
        plt.title(title)
    plt.legend()
    plt.show()


def compare_spikes(target, pred, save=None):
    y_max = max(max(target, key=lambda x: abs(x[0]))[0], max(pred, key=lambda x: abs(x[0]))[0])
    x_max = max(max(target, key=lambda x: abs(x[2]))[2], max(pred, key=lambda x: abs(x[2]))[2])

    plt.subplot(2, 1, 1)
    axes = plt.gca()
    axes.set_xlim([-0.5, x_max+1])
    axes.set_ylim([-0.5, y_max+1])
    plt.title('True Spikes')

    max_coeff = abs(max(target, key=lambda x: abs(x[1]))[1])
    for i, (spike_idx, coeff, position) in enumerate(target):
        if coeff > 0:
            color = 'r'
        else:
            color = 'b'
        intensity = abs(coeff)/max_coeff
        plt.scatter(position, spike_idx, color=color, alpha=intensity)

    plt.subplot(2, 1, 2)
    axes = plt.gca()
    axes.set_xlim([-0.5, x_max+1])
    axes.set_ylim([-0.5, y_max+1])
    plt.title('Encoded spikes')

    max_coeff = abs(max(pred, key=lambda x: abs(x[1]))[1])
    for i, (spike_idx, coeff, position) in enumerate(pred):
        if coeff > 0:
            color = 'r'
        else:
            color = 'b'
        intensity = abs(coeff)/max_coeff
        plt.scatter(position, spike_idx, color=color, alpha=intensity)

    plt.tight_layout()
    if save:
        plt.savefig(save)
    plt.show()


def plot_dic_match(dic1, dic2, matches, dic_names=['first dictionary', 'second dictionary'],
                   save=None):
    '''
    Visualy compares the correspondances between two matched dictionnaries
    '''
    nb_matches = len(matches)
    fig = plt.figure(figsize=(6, 2*nb_matches))
    for i, (id1, id2) in enumerate(matches):
        plt.subplot(nb_matches, 1, i+1)
        plt.title('Kernel {}'.format(i+1))
        plt.plot(dic1[id1]._samples, label=dic_names[0])
        plt.plot(dic2[id2]._samples, label=dic_names[1])
        plt.legend()

    plt.tight_layout()

    if save:
        plt.savefig(save)

    plt.show()
