import numpy as np
from statistics import mean

from sound import *
from matching_pursuit import *
from visualisation import *

def update_kernels(kernels_dic, decomposition, residual, learning_rate=1, verbose=False):
    for (kernel_idx, coeff, position) in decomposition:
        if verbose: print('Updating kernel {} with coeff {} from postiion {}'.format(kernel_idx, coeff, position))
        kernel = kernels_dic[kernel_idx]
        local_residual = Sound(residual._samples[position:position+kernel._len])
        kernel.add_extend(local_residual, coeff, 0)
    return

def train(kernels_dic, sounds, n_epochs, learning_rate=1, threshold=0.1, verbose=False):

    n_sounds = len(sounds)

    if verbose: plot_sound(kernels_dic[0])

    epoch_scores = []
    for epoch in range(n_epochs):
        residual_scores = []
        for i in range(n_sounds):
            sound = sounds[i%n_sounds]
            if verbose: plot_sound(sound, 'original sound')
            decomp, residual = mp_decomposition(sound, kernels_dic, threshold)
            if verbose: plot_sounds([sound, residual], ['original sound', 'residual'])
            if verbose:
                print('decomp:',decomp)
            update_kernels(kernels_dic, decomp, residual, learning_rate, verbose)
            if verbose:
                plot_sound(kernels_dic[0])
            residual_scores.append(residual.scalar_prod(residual, 0))
        epoch_score = mean(residual_scores)
        print('Mean residual norm at epoch {}: {}'.format(epoch, epoch_score))
        epoch_scores.append(epoch_score)

    return epoch_scores