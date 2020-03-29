import numpy as np
import time
import matplotlib.pyplot as plt

from sound import *
from visualisation import *

def mp_decomposition(signal, kernels, threshold, mode='bruteforce', verbose=False):
    assert threshold>1e-10

    if mode=='bruteforce': matching_function = bf_matching
    residual = Sound(signal._samples) # Will work until Sound copy is implemented
    last_coeff = threshold + 1
    decomposition = []

    start = time.time()
    while abs(last_coeff) > threshold:
        if verbose: plot_sound(residual, 'residual')
        start_search = time.time()
        kernel_id, coeff, position = matching_function(residual, kernels, verbose=verbose)
        if abs(coeff)>threshold:
            decomposition.append((kernel_id, coeff, position))
            residual.add_inplace(kernels[kernel_id], -coeff, position)
        last_coeff = coeff
        if verbose: print('Extracted component {} in:'.format((kernel_id, coeff, position)), time.time()-start)
        if verbose:
            residual_norm = residual.scalar_prod(residual, 0)
            print('Residual norm after step:', residual_norm)
    if verbose: print('Decomposed signal in:', time.time()-start)
    
    return decomposition, residual

def bf_matching(signal, kernels, verbose=False):
    '''
    Returns the principal kernel in the signal by testing all positions
    '''
    last_best = (0,0,0)
    best_score_abs = 0
    n = signal._len

    for kernel_id in kernels.keys():
        kernel = kernels[kernel_id]
        if verbose: ps_values = []
        for position in range(n):
            ps_score = signal.scalar_prod(kernel, position)
            if verbose: ps_values.append(ps_score)
            if abs(ps_score) > best_score_abs:
                last_best = (kernel_id, ps_score, position)
                best_score_abs = abs(ps_score)
        '''if verbose:
            fig = plt.figure()
            plt.plot(ps_values)
            plt.title(kernel_id)
            plt.show()'''

    return last_best