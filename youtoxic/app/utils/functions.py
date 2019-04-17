"""Contains implementation of functions used for normalization of values returned by the models."""

import numpy as np


def sigmoid(x):
    """Sigmoid function used to normalize output of the models."""
    return 1 / (1 + np.exp(-x))


def softmax(x):
    """Softmax function used to normalize output of the models."""
    if x.ndim == 1:
        x = x.reshape((1, -1))
    max_x = np.max(x, axis=1).reshape((-1, 1))
    exp_x = np.exp(x - max_x)
    return exp_x / np.sum(exp_x, axis=1).reshape((-1, 1))
