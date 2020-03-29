import numpy as np
from math import *

class Sound():
    def __init__(self, samples):
        self._len = samples.shape[0]
        self._samples = samples.copy()

    def add_extend(self, module, coef, position):
        '''
        Adds the samples from module, starting at "position" (in the original tab), with multiplicative factor "coef".
        Pads the original array is necessary 
        '''
        needed_len = position + module._len
        if needed_len > self._len:
            self._samples = np.pad(self._samples, (0,needed_len-self._len), mode='constant', constant_values=0)
            self._len += needed_len - self._len
        self._samples[position:position+module._len] += (coef * module._samples)

    def add_inplace(self, module, coef, position):
        '''
        Adds the samples from module, starting at "position" (in the original tab), with multiplicative factor "coef".
        Does not pad the original array, update outside the original shape will be discarded 
        '''
        needed_len = position + module._len
    
        if needed_len > self._len:
            self._samples[position:] += (coef * module._samples[:-(needed_len-self._len)])
        else:
            self._samples[position:position+module._len] += (coef * module._samples)

    def scalar_prod(self, module, position):
        '''
        Computes the scalar product with "module" translated by "position"
        Does not permanently pad array.
        '''
        needed_len = position + module._len
        samples_cop = self._samples.copy()
        if needed_len > self._len:
            samples_cop = np.pad(samples_cop, (0,needed_len-self._len), mode='constant', constant_values=0)
        res = np.dot(samples_cop[position:position+module._len], module._samples)
        return res

    def norm(self):
        '''
        Computes the L2 norm of the sound sample
        '''
        return sqrt(self.scalar_prod(self, 0))

    def normalise(self):
        '''
        Scales the samples so that its L2 norm is 1
        '''
        norm = self.norm()
        self._samples = self._samples / norm
