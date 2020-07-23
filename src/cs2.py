# 解决问题：
# 1. 定义尽量在一起；
# 2. combine L with not L
# 3. to XYZ 的问题

# 一起定义的好处在于
# 1. 不会引起代码的混乱
# 2. 容易连接L和非L
# 3. to XYZ可以在RGB和RGBL上同时实现
# 4. io可以一致
#
# 坏处：
# 1. 数据会重复2份；

import numpy as np
from skimage import color
from .utils import *

class ColorSpace:
    type = ''
    def __init__(self):
        self.io = None
    
    def relate(self, other):
        return 1 if type(self)==type(other) and self.io==other.io else 0

class RGB_Base_(ColorSpace):
    type = 'RGB'
    '''
    base of RGB color space;
    the argument values are from AdobeRGB;

    Data from https://en.wikipedia.org/wiki/Adobe_RGB_color_space
    '''
    def __init__(self, linear = False):
        # self._set_io()
        self._set_primaries()
        self._cal_M()

        self._set_gamma()
        self._cal_para()

        self.linear = linear
        self.operations()
    
    # def _set_io(self):
    #     # IO
    #     self.io = D65_2        

    def _set_primaries(self):
        # IO
        self.io = D65_2        

        # primaries
        self.xr, self.yr = 0.6400, 0.3300	
        self.xg, self.yg = 0.21, 0.71
        self.xb, self.yb = 0.1500, 0.0600

    def _set_gamma(self):
        # linearization
        self.gamma = 2.2  
    
    def _cal_para(self):
        pass

    def operations(self):
        # to or from XYZ
        if self.linear:
            self.to = [self.toL, self.M]
            self.from_ = [self.Mi, self.fromL]
        else:
            self.to = [self.M]
            self.from_ = [self.Mi]

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
        return gamma_correction(rgb, self.gamma)
    
    def fromL(self, rgbl):
        return gamma_correction(rgbl, 1/self.gamma)

    def relate(self, other):
        '''
        RGB relate有3种关系：
        1. type不同
        1. type相同，linear相同；-- 1
        2. type相同, linear不同，self是非线性；-- 2
        3. type相同, linear不同，self是线性 -- 3
        '''
        if type(self)!=type(other):
            return 0
        if self.linear==other.linear:
            return 1
        if self.linear==False:
            return 2
        return 3
        # return type(self)==type(other) and self.linear==other.linear
    

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
        self.xr, self.yr = 0.6400, 0.3300	
        self.xg, self.yg = 0.3000, 0.6000
        self.xb, self.yb = 0.1500, 0.0600

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

    def _set_gamma(self):
        self.a, self.gamma = 0.09929682680944, 1/0.45    

# def get_colorspace(colorspace):
#     '''get colorspace by str'''
#     if isinstance(colorspace, str):
#         return globals()[colorspace]()
#     return colorspace

# def colorconvert(color, src, dst):
#     '''convert between RGB color space'''
#     return get_colorspace(dst).xyz2rgb(get_colorspace(src).rgb2xyz(color, D65_2), D65_2)

def bind(CS):
    cs, csl = CS(), CS(True)
    cs.l = csl
    csl.l = cs
    return cs, csl

sRGB, sRGBL = bind(sRGB_)
AdobeRGB, AdobeRGBL = bind(AdobeRGB_)
WideGamutRGB, WideGamutRGBL = bind(WideGamutRGB_)
ProPhotoRGB, ProPhotoRGBL = bind(ProPhotoRGB_)
DCI_P3_RGB, DCI_P3_RGBL = bind(DCI_P3_RGB_)
AppleRGB, AppleRGBL = bind(AppleRGB_)
REC_709_RGB, REC_709_RGBL = bind(REC_709_RGB_)
REC_2020_RGB, REC_2020_RGBL = bind(REC_2020_RGB_)

# class CAM:
#     '''chromatic adaption matrices'''
#     CAMs = {}

#     Von_Kries = np.array([[ 0.40024,  0.7076 , -0.08081],
#                     [-0.2263 ,  1.16532,  0.0457 ],
#                     [ 0.     ,  0.     ,  0.91822]])

#     Bradford = np.array([[0.8951, 0.2664, -0.1614],
#             [-0.7502, 1.7135, 0.0367],
#             [0.0389, -0.0685, 1.0296]])

#     MAs = {'Identity':(np.eye(3), np.eye(3)), 
#         'Von_Kries':(Von_Kries, np.linalg.inv(Von_Kries)),
#         'Bradford':(Bradford, np.linalg.inv(Bradford))}

#     @classmethod
#     def cam(cls, sio, dio, method = 'Bradford'):
#         '''get cam'''
#         if (sio, dio, method) in cls.CAMs:
#             return cls.CAMs[(sio, dio, method)]
#         # function from http://www.brucelindbloom.com/index.html?ColorCheckerRGB.html
#         XYZws = illuminants[sio]
#         XYZWd = illuminants[dio]
#         MA, MA_inv = cls.MAs[method]
#         M = MA_inv@np.diag((MA@XYZWd)/(MA@XYZws))
#         cls.CAMs[(sio, dio, method)] = M
#         return M

class CAM:
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
    def cam(cls, sio, dio, method = 'Bradford'):
        '''get cam'''
        if (sio, dio, method) in cls.CAMs:
            return cls.CAMs[(sio, dio, method)]
        # function from http://www.brucelindbloom.com/index.html?ColorCheckerRGB.html
        XYZws = illuminants[sio]
        XYZWd = illuminants[dio]
        MA, MA_inv = cls.MAs[method]
        M = MA_inv@np.diag((MA@XYZWd)/(MA@XYZws))
        cls.CAMs[(sio, dio, method)] = M
        return M

'''function to get cam'''
cam = CAM.cam

class XYZ(ColorSpace):
    type = 'XYZ'    
    def __init__(self, io = D65_2):
        self.io = io

    def to(self, io):
        return [] if self.io == io else [cam(self.io, io).T]
    
    def __eq__(self, other):
        return type(other)==type(self) and self.io==other.io
    
XYZ_D65_2 = XYZ()
XYZ_D50_2 = XYZ(D50_2)

from functools import partial
class Lab(ColorSpace):
    type = 'Lab'    
    def __init__(self, io = D65_2):
        self.io = io

    def to(self):
        return [partial(color.colorconv.lab2xyz, illuminant = self.io.illuminant, 
            observer = self.io.observer)]
    
    def from_(self):
        return [partial(color.colorconv.xyz2lab, illuminant = self.io.illuminant, 
            observer = self.io.observer)]

    def __eq__(self, other):
        return type(other)==type(self) and self.io==other.io

# from copy import copy
Lab_D65_2 = Lab()
Lab_D50_2 = Lab(D50_2)

# gray color space


class Color:
    def __init__(self, colors, cs):
        self.colors = colors
        self.cs = cs
    
    def copy(self, cs=None):
        return Color(self.colors.copy(), cs if cs is not None else self.cs)
    
    def to(self, cs):
        relation = self.cs.relate(cs)
        if relation == 1:
            return self.copy()
        if relation == 2:
            return Color(self.cs.toL(self.colors), cs)
        if relation == 3:
            return Color(self.cs.fromL(self.colors), cs)
        
        operations = [*self.cs.to, *(XYZ(self.cs.io).to(XYZ(cs.io))), *cs.from_]
        colors = self.colors
        M = None
        for op in operations:
            if isinstance(op, np.ndarray):
                if M is None:
                    M = op
                else:
                    M = M@op
            else:
                if M is not None:
                    colors = colors@M
                    M = None
                colors = op(colors)
        if M is not None:
            colors = colors@M
        return Color(colors, cs)

    # 支持以下运算
    # 1. 取下标，为下标赋值等等
    # 2. @ccm    
    # 3. distance
    # 4. 取黑白
    



if __name__ == "__main__":
    pass
