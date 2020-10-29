import numpy as np
from statistics import mean

from sound import *
from matching_pursuit import *
from visualisation import *


def update_kernels(kernels_dic, decomposition, residual, learning_rate=1, verbose=0):
    for (kernel_idx, coeff, position) in decomposition:
        if verbose == 2:
            print('Updating kernel {} with coeff {} from postiion {}'.format(kernel_idx, coeff,
                                                                             position))
        kernel = kernels_dic[kernel_idx]
        local_residual = Sound(residual._samples[position:position+kernel._len])
        kernel.add_extend(local_residual, coeff, 0)
    for kernel_id in kernels_dic.keys():
        kernels_dic[kernel_id].normalise()
    return


def train(kernels_dic, sounds, n_epochs, learning_rate=0.1, init_threshold=1, verbose=0):

    n_sounds = len(sounds)

    if verbose == 2:
        plot_sound(kernels_dic[0], title='kernel 0')

    epoch_scores = []
    for epoch in range(n_epochs):

        threshold = init_threshold / (epoch+1)

        residual_scores = []
        for i in range(n_sounds):
            sound = sounds[i % n_sounds]
            if verbose == 2:
                plot_sound(sound, title='original sound')
            decomp, residual = mp_decomposition(sound, kernels_dic, max(threshold, 0.1),
                                                verbose=verbose)
            if verbose == 2:
                plot_sounds([sound, residual], ['original sound', 'residual'])
            if verbose == 2:
                print('decomp:', decomp)
            update_kernels(kernels_dic, decomp, residual, learning_rate, verbose)
            if verbose == 2:
                plot_sound(kernels_dic[0], title='kernel O')
            residual_scores.append(residual.scalar_prod(residual, 0))
        epoch_score = mean(residual_scores)
        if verbose > 0:
            print('Mean residual norm at epoch {}: {}'.format(epoch, epoch_score))
        epoch_scores.append(epoch_score)

    return epoch_scores
