import numpy as np
from skimage import color
from .io_ import *

def saturate(src, low, up):
    '''return the mask of unsaturated colors'''
    return np.all(np.logical_and(src>=low,src<=up), axis = -1)               


# =======some convection functions=========
def xyz2grayl(xyz):
    '''xyz->linear grayscale'''
    return xyz[..., 1]

def xyz2lab(xyz, io = D65_2):
    '''xyz->lab with io unchanged'''
    return color.colorconv.xyz2lab(xyz, io.illuminant, io.observer)

def lab2xyz(lab, io = D65_2):
    '''lab->xyz with io unchanged'''
    return color.colorconv.lab2xyz(lab, io.illuminant, io.observer)

def xyz2xyz(xyz, sio, dio):
    '''xyz->xyz with io changed'''
    if sio==dio:
        return xyz
    return xyz@cam(sio, dio).T

def lab2lab(lab, sio, dio):
    '''lab->lab with io changed'''
    if sio==dio:
        return lab    
    return xyz2lab(xyz2xyz(lab2xyz(lab, sio), sio, dio), dio) 

# ==== others ==============
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
