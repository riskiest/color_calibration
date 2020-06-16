import numpy as np

def saturate(src, low, up):
    return np.all(np.logical_and(src>=low,src<=up), axis = 1)
