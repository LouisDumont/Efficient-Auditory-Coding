import numpy as np
import random
from math import *

from sound import *
from utils import *

class Kernels_generator():
    '''
    Ancestor for all kernel dics generators
    '''
    def __init__(self, avg_length=100, mean=0, std=1):
        self._avg_length = avg_length
        self._mean = mean
        self._std = std

    def generate_kernels(self, n_kernels):
        '''
        Generates a dictionnary of kernels (as a list)
        '''
        raise NotImplementedError

class Gaussian_noise_generator(Kernels_generator):
    '''
    Generates Gaussian noise with predetermined statistics
    '''
    def __init__(self, avg_length=100, mean=0, std=1):
        super().__init__(avg_length, mean, std)

    def generate_kernels(self, n_kernels):
        '''
        Generates a dictionnary of kernels (as a list) initialised with gaussian noise
        '''
        dic = {}
        for i in range(n_kernels):
            kernel_length = max(int(random.gauss(self._avg_length, self._avg_length/4)), 1)
            kernel_samples = np.random.normal(self._mean, self._std, kernel_length)
            samples_norm = np.dot(kernel_samples, kernel_samples)
            kernel_samples = kernel_samples / sqrt(samples_norm)
            dic[i] = Sound(kernel_samples)
        return dic

class Gaussian_distrib_generator(Kernels_generator):
    '''
    Generates kernels that ressemble a Gaussian distribution
    '''
    def __init__(self, avg_length=100, mean=10, std=5):
        super().__init__(avg_length, mean, std)

    def generate_kernels(self, n_kernels):
        '''
        Generates a dictionnary of kernels (as a list) initialised with gaussian distribution
        '''  
        dic = {}
        for i in range(n_kernels):
            kernel_mean = max(random.gauss(self._mean, self._std), 1)
            kernel_std = max(random.gauss(self._std, self._std/2), 1)
            kernel_length = 2*int(kernel_mean)+1
            kernel_samples = np.arange(0, kernel_length, 1)
            kernel_samples = gaussian(kernel_samples, kernel_mean, kernel_std)
            samples_norm = np.dot(kernel_samples, kernel_samples)
            kernel_samples = kernel_samples / sqrt(samples_norm)
            dic[i] = Sound(kernel_samples)
        return dic     


class Sound_generator():
    '''
    Generates sounds based on the combinations of elements in a dictionnary
    '''
    def __init__(self, kernel_dic, avg_length, avg_density=0.15, noise=None):
        self._kernels = kernel_dic
        self._avg_length = avg_length
        self._noise = noise # Noise is always assumed to be Gaussian, with std self._noise
        self._avg_density = avg_density

    def generate_sound(self, length=None, density=0.15):
        # density of kernels is estimated from the article
        # TODO: add noise
        if length is None:
            length = max(int(random.gauss(self._avg_length, self._avg_length/4)), 1+self._avg_length//10)
        print('Length of generated sound:', length)
        sound = Sound(np.zeros(length))
        basis = [] # Stores the original (idx, coeff, position) tuples from which the sound was generated
        nb_kernels = max(int(random.gauss(density*length, density*length/4)), 0)
        for i in range(nb_kernels):
            #try:
            kernel_idx = random.choice(list(self._kernels.keys()))
            position = random.randint(0,length)
            coeff = random.gauss(0,1)
            kernel = self._kernels[kernel_idx]
            sound.add_extend(kernel, coeff, position)
            basis.append((kernel_idx, coeff, position))
            '''except:
                print('Could not add kernel to generated sample. Details:')
                print('kernel length:', kernel._len)
                print('kernel:', kernel._samples)
                print('positions:', position)
                print('coeff:', coeff)
                print('sound length:', sound._len)'''
        if self._noise:
            noise = Sound(np.random.normal(0, self._noise, sound._len))
            sound.add_inplace(noise, 1, 0)
        return sound, basis

    def generate_sounds(self, n_sounds, avg_length=None, avg_density=None):
        if not avg_length: avg_length = self._avg_length
        if not avg_density: avg_density = self._avg_density
        sounds = []
        bases = []
        lengths = np.maximum(np.random.normal(self._avg_length, self._avg_length/4, n_sounds), 1+self._avg_length//10)
        densities = np.maximum(np.random.normal(self._avg_density, self._avg_density/4, n_sounds), 0)
        for i in range(n_sounds):
            generation = self.generate_sound(int(lengths[i]), densities[i])
            sounds.append(generation[0])
            bases.append(generation[1])
        return sounds, bases



        
        
