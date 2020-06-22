'''
    Same as ADALINE, except has different activation, loss, and predict functions

    Camille Ross & Marius Orehovschi
    Prof. Oliver Layton
    Colby College
    CS343: Neural Networks
    Project 1: Single Layer Networks
    ADALINE (ADaptive LInear NEuron) neural network for classification and regression
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from adaline import Adaline

class AdalineLogistic(Adaline):
    
    def __init__(self, n_epochs=1000, lr=0.001):
        super().__init__(n_epochs, lr)
    
    def activation(self, net_in):
        '''
        Applies the activation function to the net input and returns the output neuron's activation.
        Activation function is f(NetIn) = 1 / (1 + e^(-NetIn))

        Parameters:
        ----------
        net_in: ndarray. Shape = [Num samples,]

        Returns:
        ----------
        net_act. ndarray. Shape = [Num samples,]
        '''

        return 1 / (1 + np.exp(-net_in))
    
    def compute_loss(self, y, net_act):
        ''' Computes the Cross Entropy loss (over a single training epoch)

        Parameters:
        ----------
        y: ndarray. Shape = [Num samples,]
            True classes corresponding to each input sample in a training epoch (coded as 0 or 1).
        net_act: ndarray. Shape = [Num samples,]
            Output neuron's activation value (after activation function is applied)

        Returns:
        ----------
        float. The Cross Entropy loss (across a single training epoch).
        '''
        
        loss = 0
        
        for i in range(len(y)):
            if y[i] == 0:
                loss += -np.log(1-net_act[i])
            else:
                loss += -np.log(net_act[i])

        return loss
    
    def predict(self, features):
        '''Predicts the class of each test input sample

        Parameters:
        ----------
        features: ndarray. Shape = [Num samples, Num features]
            Collection of input vectors.

        Returns:
        ----------
        The predicted classes (-1 or +1) for each input feature vector. Shape = [Num samples,]
        '''

        net_act = self.activation(self.net_input(features))

        return np.where(net_act >= 0.5, 1, 0)

def main():
    pass

if __name__ == "__main__":
    main()

