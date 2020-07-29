import numpy as np
from skimage import color
import inspect
from .io_ import *
from .utils import *

class SingletonArgs(type):
    """ 
    Singleton with arguments;
    Only supports hashable arguments.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        key = (cls, frozenset(inspect.getcallargs(cls.__init__, None, *args, **kwargs).items()))

        if key not in cls._instances:
            cls._instances[key] = super(SingletonArgs, cls).__call__(*args, **kwargs)
        return cls._instances[key]

class ColorSpace(metaclass=SingletonArgs):
    '''color space interface'''
    def __init__(self):
        self.io = None
    
    def relate(self, other):
        '''
        relate with other color space;
        if they are the same, return copy function;
        else return None;
        '''
        return (lambda x:x) if type(self)==type(other) and self.io==other.io else None

class RGB_Base_(ColorSpace):
    '''
    base of RGB color space;
    the argument values are from AdobeRGB;

    Data from https://en.wikipedia.org/wiki/Adobe_RGB_color_space
    '''
    def __init__(self, linear = False):
        self._set_primaries()
        self._cal_M()

        self._set_gamma()
        self._cal_para()

        self.linear = linear
        self.operations()

    def _set_primaries(self):
        # IO
        self.io = D65_2        

        # primaries
        self.xr, self.yr = 0.64, 0.33
        self.xg, self.yg = 0.21, 0.71
        self.xb, self.yb = 0.15, 0.06

    def _set_gamma(self):
        # linearization
        self.gamma = 2.2  
    
    def _cal_para(self):
        pass

    def operations(self):
        '''operations to or from XYZ'''
        if self.linear:
            self.to = [self.M.T]
            self.from_ = [self.Mi.T]
        else:
            self.to = [self.toL, self.M.T]
            self.from_ = [self.Mi.T, self.fromL]

    def _cal_M(self):
        '''
        calculation of M_RGBL2XYZ_base;
        see ColorSpace.pdf for details;
        '''
        XYZr = xyY2XYZ(self.xr, self.yr)
        XYZg = xyY2XYZ(self.xg, self.yg)
        XYZb = xyY2XYZ(self.xb, self.yb)
        XYZw = illuminants[self.io]
        XYZ_rgbl = np.stack([XYZr, XYZg, XYZb], axis= 1)
        Sr, Sg, Sb = np.linalg.solve(XYZ_rgbl, XYZw)
        self.M = np.stack([Sr*XYZr, Sg*XYZg, Sb*XYZb], axis= 1) 
        self.Mi = np.linalg.inv(self.M)

    def toL(self, rgb):
        '''rgb -> rgbl'''
        return gamma_correction(rgb, self.gamma)
    
    def fromL(self, rgbl):
        '''rgbl -> rgb'''
        return gamma_correction(rgbl, 1/self.gamma)

    def relate(self, other):
        '''
        There are 3 kinds of relationships for RGB:
         1. Different types;    - no operation
         1. Same type, same linear; - copy
         2. Same type, different linear, self is nonlinear; - 2 toL
         3. Same type, different linear, self is linear - 3 fromL
        '''
        if type(self)!=type(other):
            return None
        if self.linear==other.linear:
            return (lambda x:x)
        if self.linear==False:
            return self.toL
        return self.fromL    

class sRGB_Base_(RGB_Base_):
    '''
    base of sRGB-like color space;
    the argument values are from sRGB;
    data from https://en.wikipedia.org/wiki/SRGB
    '''
    def _set_primaries(self):
        # IO
        self.io = D65_2        
        # primaries
        self.xr, self.yr = 0.64, 0.33	
        self.xg, self.yg = 0.30, 0.60
        self.xb, self.yb = 0.15, 0.06

    def _set_gamma(self):
        # linearization
        self.a = 0.055
        self.gamma = 2.4

    def _cal_para(self):
        '''
        linearization parameters
        see ColorSpace.pdf for details;        
        '''
        self.alpha = self.a+1
        self.K0 = self.a/(self.gamma-1)
        self.phi = (self.alpha**self.gamma*(self.gamma-1)**(self.gamma-1))/(self.a**(self.gamma-1)*self.gamma**self.gamma)
        self.beta = self.K0/self.phi

    def toL(self, rgb):
        '''
        linearization
        see ColorSpace.pdf for details; 
        '''
        def _rgb2rgbl_ele(x):
            if x>self.K0:
                return ((x+self.alpha-1)/self.alpha)**self.gamma
            elif x>=-self.K0:
                return x/self.phi
            else:
                return -(((-x+self.alpha-1)/self.alpha)**self.gamma)
        return np.vectorize(_rgb2rgbl_ele)(rgb)  
    
    def fromL(self, rgbl):
        '''
        delinearization
        see ColorSpace.pdf for details; 
        '''
        def _rgbl2rgb_ele(x):
            if x>self.beta:
                return self.alpha*(x**(1/self.gamma))-(self.alpha-1)
            elif x>=-self.beta:
                return x*self.phi
            else:
                return -(self.alpha*((-x)**(1/self.gamma))-(self.alpha-1))
        return np.vectorize(_rgbl2rgb_ele)(rgbl)    

class sRGB_(sRGB_Base_):
    '''data from https://en.wikipedia.org/wiki/SRGB'''
    pass

class AdobeRGB_(RGB_Base_):
    pass

class WideGamutRGB_(RGB_Base_):
    '''data from https://en.wikipedia.org/wiki/Wide-gamut_RGB_color_space'''

    def _set_primaries(self):
        self.xr, self.yr = 0.7347, 0.2653	
        self.xg, self.yg = 0.1152, 0.8264
        self.xb, self.yb = 0.1566, 0.0177
        self.io = D50_2

class ProPhotoRGB_(RGB_Base_):
    '''data from https://en.wikipedia.org/wiki/ProPhoto_RGB_color_space'''

    def _set_primaries(self):
        self.xr, self.yr = 0.734699, 0.265301	
        self.xg, self.yg = 0.159597, 0.840403
        self.xb, self.yb = 0.036598, 0.000105
        self.io = D50_2    

    def _set_gamma(self):
        self.gamma = 1.8

class DCI_P3_RGB_(RGB_Base_):
    '''data from https://en.wikipedia.org/wiki/DCI-P3'''

    def _set_primaries(self):
        self.xr, self.yr = 0.680, 0.32	
        self.xg, self.yg = 0.265, 0.69
        self.xb, self.yb = 0.15, 0.06
        self.io = D65_2        

class AppleRGB_(RGB_Base_):
    '''data from http://www.brucelindbloom.com/index.html?WorkingSpaceInfo.html'''

    def _set_primaries(self):   	
        self.xr, self.yr = 0.625, 0.34	
        self.xg, self.yg = 0.28, 0.595
        self.xb, self.yb = 0.155, 0.07
        self.io = D65_2        
    
    def _set_gamma(self):
        self.gamma = 1.8

class REC_709_RGB_(sRGB_Base_):
    '''data from https://en.wikipedia.org/wiki/Rec._709'''

    def _set_primaries(self):   	
        self.xr, self.yr = 0.64, 0.33	
        self.xg, self.yg = 0.3, 0.6
        self.xb, self.yb = 0.15, 0.06
        self.io = D65_2        
    
    def _set_gamma(self):
        self.a, self.gamma = 0.099, 1/0.45
 
class REC_2020_RGB_(sRGB_Base_):
    '''data from https://en.wikipedia.org/wiki/Rec._2020'''

    def _set_primaries(self):   	
        self.xr, self.yr = 0.708, 0.292	
        self.xg, self.yg = 0.17, 0.797
        self.xb, self.yb = 0.131, 0.046
        self.io = D65_2  

    def _set_gamma(self):
        self.a, self.gamma = 0.09929682680944, 1/0.45    

def bind(CS):
    '''produce color space instance with linear and non-linear versions'''
    cs, csl = CS(), CS(True)
    cs.l = csl.l = csl
    csl.nl = cs.nl = cs
    return cs, csl

sRGB, sRGBL = bind(sRGB_)
AdobeRGB, AdobeRGBL = bind(AdobeRGB_)
WideGamutRGB, WideGamutRGBL = bind(WideGamutRGB_)
ProPhotoRGB, ProPhotoRGBL = bind(ProPhotoRGB_)
DCI_P3_RGB, DCI_P3_RGBL = bind(DCI_P3_RGB_)
AppleRGB, AppleRGBL = bind(AppleRGB_)
REC_709_RGB, REC_709_RGBL = bind(REC_709_RGB_)
REC_2020_RGB, REC_2020_RGBL = bind(REC_2020_RGB_)

class XYZ(ColorSpace):
    '''chromatic adaption matrices'''
    CAMs = {}

    Von_Kries = np.array([[ 0.40024,  0.7076 , -0.08081],
                    [-0.2263 ,  1.16532,  0.0457 ],
                    [ 0.     ,  0.     ,  0.91822]])

    Bradford = np.array([[0.8951, 0.2664, -0.1614],
            [-0.7502, 1.7135, 0.0367],
            [0.0389, -0.0685, 1.0296]])

    MAs = {'Identity':(np.eye(3), np.eye(3)), 
        'Von_Kries':(Von_Kries, np.linalg.inv(Von_Kries)),
        'Bradford':(Bradford, np.linalg.inv(Bradford))}

    @classmethod
    def _cam(cls, sio, dio, method = 'Bradford'):
        '''get cam'''
        if sio==dio:
            return np.eye(3)
        if (sio, dio, method) in cls.CAMs:
            return cls.CAMs[(sio, dio, method)]
        if (dio, sio, method) in cls.CAMs:
            cls.CAMs[(sio, dio, method)] = np.linalg.inv(cls.CAMs[(dio, sio, method)])
            return cls.CAMs[(sio, dio, method)]
        # function from http://www.brucelindbloom.com/index.html?ColorCheckerRGB.html
        XYZws = illuminants[sio]
        XYZWd = illuminants[dio]
        MA, MA_inv = cls.MAs[method]
        M = MA_inv@np.diag((MA@XYZWd)/(MA@XYZws))@MA
        cls.CAMs[(sio, dio, method)] = M
        return M

    def __init__(self, io = D65_2):
        self.io = io
        self.to = []
        self.from_ = []

    def cam(self, io, method = 'Bradford'):
        return [] if self.io == io else [self._cam(self.io, io, method).T]
        
XYZ_D65_2 = XYZ()
XYZ_D50_2 = XYZ(D50_2)

from functools import partial
class Lab(ColorSpace):
    def __init__(self, io = D65_2):
        self.io = io
        
        self.to = [partial(color.colorconv.lab2xyz, illuminant = self.io.illuminant, 
            observer = self.io.observer)]
        
        self.from_ = [partial(color.colorconv.xyz2lab, illuminant = self.io.illuminant, 
            observer = self.io.observer)]

# from copy import copy
Lab_D65_2 = Lab()
Lab_D50_2 = Lab(D50_2)

if __name__ == "__main__":
    pass
