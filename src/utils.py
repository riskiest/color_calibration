import numpy as np

def saturate(src, low, up):
    '''return the mask of unsaturated colors'''
    return np.all(np.logical_and(src>=low,src<=up), axis = -1)               

def gamma_correction(rgb, gamma):
    '''
    gamma correction; 
    see ColorSpace.pdf for details;
    '''
    arr = rgb.copy()
    mask = rgb>=0
    arr[mask] = np.power(arr[mask], gamma)
    arr[~mask] = -np.power(-arr[~mask], gamma)
    return arr

def rgb2gray(rgb):
    '''
    it is an approximation grayscale function for relative RGB color space;
    see Miscellaneous.pdf for details;
    rgb->gray
    '''
    return rgb@np.array([0.2126, 0.7152, 0.0722])
