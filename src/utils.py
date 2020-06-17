import numpy as np
from skimage import color
from .io_ import *

def saturate(src, low, up):
    return np.all(np.logical_and(src>=low,src<=up), axis = 1)               

# some convection functions
def xyz2grayl(xyz):
    return xyz[..., 1]

def xyz2lab(xyz, io = D65_2):
    return color.colorconv.xyz2lab(xyz, io.illuminant, io.observer)

def lab2xyz(lab, io = D65_2):
    return color.colorconv.lab2xyz(lab, io.illuminant, io.observer)

def xyz2xyz(xyz, sio, dio):
    if sio==dio:
        return xyz
    return cam(sio, dio)@xyz

def lab2lab(lab, sio, dio):
    if sio==dio:
        return lab    
    return xyz2lab(xyz2xyz(lab2xyz(lab, sio), sio, dio), dio) 

# gamma correction ...
def gamma_correction(rgb, gamma):
    arr = rgb.copy()
    mask = rgb>=0
    arr[mask] = np.power(arr[mask], gamma)
    arr[~mask] = -np.power(-arr[~mask], gamma)
    return arr

# some gray
def rgb2gray(rgb):
    '''
    In fact, every kind of rgb has a different function to gray.
    because we don't know the exact color space of the input, we use it as an approximation.
    '''
    return rgb@np.array([0.2126, 0.7152, 0.0722])
