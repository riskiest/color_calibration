import numpy as np
from skimage import color
from .utils import *

class RGB_Base:
    '''
    base of RGB color space;
    the argument values are from AdobeRGB;

    Data from https://en.wikipedia.org/wiki/Adobe_RGB_color_space
    '''
    def __init__(self):
        # primaries
        self.xr, self.yr = 0.6400, 0.3300	
        self.xg, self.yg = 0.21, 0.71
        self.xb, self.yb = 0.1500, 0.0600

        # IO
        self.io_base = D65_2

        # linearization
        self.gamma = 2.2  

        # to XYZ
        # M_RGBL2XYZ_base is matrix without chromatic adaptation
        # M_RGBL2XYZ is the one with
        # the _ prefix is the storage of calculated results
        self._M_RGBL2XYZ_base = None
        self._M_RGBL2XYZ = {}
    
    def cal_M_RGBL2XYZ_base(self):
        '''
        calculation of M_RGBL2XYZ_base;
        see ColorSpace.pdf for details;
        '''
        XYZr = xyY2XYZ(self.xr, self.yr)
        XYZg = xyY2XYZ(self.xg, self.yg)
        XYZb = xyY2XYZ(self.xb, self.yb)
        XYZw = illuminants[self.io_base]
        XYZ_rgbl = np.stack([XYZr, XYZg, XYZb], axis= 1)
        Sr, Sg, Sb = np.linalg.solve(XYZ_rgbl, XYZw)
        self._M_RGBL2XYZ_base = np.stack([Sr*XYZr, Sg*XYZg, Sb*XYZb], axis= 1)  
        return self._M_RGBL2XYZ_base      

    @property
    def M_RGBL2XYZ_base(self):
        '''get M_RGBL2XYZ_base'''
        if self._M_RGBL2XYZ_base is not None:
            return self._M_RGBL2XYZ_base
        return self.cal_M_RGBL2XYZ_base()

    def choose_io(self, io = None):
        '''if io is unset, use io of this RGB color space'''
        return io or self.io_base
    
    # def set_default(self, io):
    #     self._default_io = io
            
    def M_RGBL2XYZ(self, io = None, rev = False):
        '''
        calculation of M_RGBL2XYZ;
        see ColorSpace.pdf for details;
        '''
        io = self.choose_io(io)
        if io in self._M_RGBL2XYZ:
            return self._M_RGBL2XYZ[io][1 if rev else 0]
        if io==self.io_base:
            self._M_RGBL2XYZ[io] = (self.M_RGBL2XYZ_base, np.linalg.inv(self.M_RGBL2XYZ_base))
            return self._M_RGBL2XYZ[io][1 if rev else 0]
        M_RGBL2XYZ = cam(self.io_base, io)@self.M_RGBL2XYZ_base
        self._M_RGBL2XYZ[io] = (M_RGBL2XYZ, np.linalg.inv(M_RGBL2XYZ))
        return self._M_RGBL2XYZ[io][1 if rev else 0]

    def rgbl2xyz(self, rgbl, io = None):
        io = self.choose_io(io)
        return rgbl@(self.M_RGBL2XYZ(io).T)
    
    def xyz2rgbl(self, xyz, io = None):
        io = self.choose_io(io)
        return xyz@(self.M_RGBL2XYZ(io, True).T)

    def rgb2rgbl(self, rgb):
        return gamma_correction(rgb, self.gamma)
    
    def rgbl2rgb(self, rgbl):
        return gamma_correction(rgbl, 1/self.gamma)

    def rgb2xyz(self, rgb, io = None):
        io = self.choose_io(io)
        return self.rgbl2xyz(self.rgb2rgbl(rgb), io) 

    def xyz2rgb(self, xyz, io = None):
        io = self.choose_io(io)
        return self.rgbl2rgb(self.xyz2rgbl(xyz, io)) 

    def rgbl2lab(self, rgbl, io = None):
        io = self.choose_io(io)
        return xyz2lab(self.rgbl2xyz(rgbl, io), io)
    
    def lab2rgbl(self, lab, io = None):
        io = self.choose_io(io)
        return self.xyz2rgbl(lab2xyz(lab, io), io)
    
    def rgb2lab(self, rgb, io = None):
        io = self.choose_io(io)
        return self.rgbl2lab(self.rgb2rgbl(rgb), io)
    
    def lab2rgb(self, lab, io = None):
        io = self.choose_io(io)
        return self.xyz2rgb(lab2xyz(lab, io), io)
        
class sRGB_Base(RGB_Base):
    '''
    base of sRGB-like color space;
    the argument values are from sRGB;
    data from https://en.wikipedia.org/wiki/SRGB
    '''
    def __init__(self):
        super().__init__()

        # primaries        
        self.xr, self.yr = 0.6400, 0.3300	
        self.xg, self.yg = 0.3000, 0.6000
        self.xb, self.yb = 0.1500, 0.0600

        # linearization
        self._set()
        self._linear()

    def _set(self):
        '''for adaptation'''
        self.a = 0.055
        self.gamma = 2.4

    def _linear(self):
        '''
        linearization parameters
        see ColorSpace.pdf for details;        
        '''
        self.alpha = self.a+1
        self.K0 = self.a/(self.gamma-1)
        self.phi = (self.alpha**self.gamma*(self.gamma-1)**(self.gamma-1))/(self.a**(self.gamma-1)*self.gamma**self.gamma)
        self.beta = self.K0/self.phi
        # # ============
        # # L: linear, N: non-linear, K0 = beta*phi
        # # N = L/beta L<=K0
        # #   = ((L+alpha-1)/alpha)^gamma L>K0
        # # L = N*beta N<=phi
        # #   = alpha*N^(1/gamma)-(alpha-1)
        # # ============        
        # self.alpha, self.beta, self.phi, self.gamma = 1.055, 0.0031308, 12.92, 2.4
        # self._K0 = None

    # @property
    # def K0(self):
    #     if self._K0:
    #         return self._K0
    #     return self.beta*self.phi

    def rgb2rgbl(self, rgb):
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
    
    def rgbl2rgb(self, rgbl):
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

class sRGB(sRGB_Base):
    '''data from https://en.wikipedia.org/wiki/SRGB'''

    def __init__(self):
        super().__init__()
        self._M_RGBL2XYZ_base = np.array([[0.41239080, 0.35758434, 0.18048079],
                [0.21263901 ,0.71516868 ,0.07219232],
                [0.01933082 ,0.11919478 ,0.95053215]])

class AdobeRGB(RGB_Base):
    pass

class WideGamutRGB(RGB_Base):
    '''data from https://en.wikipedia.org/wiki/Wide-gamut_RGB_color_space'''

    def __init__(self):
        super().__init__()    	
        self.xr, self.yr = 0.7347, 0.2653	
        self.xg, self.yg = 0.1152, 0.8264
        self.xb, self.yb = 0.1566, 0.0177
        self.io_base = D50_2

class ProPhotoRGB(RGB_Base):
    '''data from https://en.wikipedia.org/wiki/ProPhoto_RGB_color_space'''

    def __init__(self):
        super().__init__()    	
        self.xr, self.yr = 0.734699, 0.265301	
        self.xg, self.yg = 0.159597, 0.840403
        self.xb, self.yb = 0.036598, 0.000105
        self.io_base = D50_2    

class DCI_P3_RGB(RGB_Base):
    '''data from https://en.wikipedia.org/wiki/DCI-P3'''

    def __init__(self):
        super().__init__()    	
        self.xr, self.yr = 0.680, 0.32	
        self.xg, self.yg = 0.265, 0.69
        self.xb, self.yb = 0.15, 0.06

class AppleRGB(RGB_Base):
    '''data from http://www.brucelindbloom.com/index.html?WorkingSpaceInfo.html'''

    def __init__(self):
        super().__init__()    	
        self.xr, self.yr = 0.625, 0.34	
        self.xg, self.yg = 0.28, 0.595
        self.xb, self.yb = 0.155, 0.07
        self.gamma = 1.8

class REC_709_RGB(sRGB_Base):
    '''data from https://en.wikipedia.org/wiki/Rec._709'''

    def __init__(self):
        super().__init__()    	
        self.xr, self.yr = 0.64, 0.33	
        self.xg, self.yg = 0.3, 0.6
        self.xb, self.yb = 0.15, 0.06
    
    def _set(self):
        self.a, self.gamma = 0.099, 1/0.45
 
class REC_2020_RGB(sRGB_Base):
    '''data from https://en.wikipedia.org/wiki/Rec._2020'''

    def __init__(self):
        super().__init__()    	
        self.xr, self.yr = 0.708, 0.292	
        self.xg, self.yg = 0.17, 0.797
        self.xb, self.yb = 0.131, 0.046

    def _set(self):
        self.alpha, self.gamma = 0.09929682680944, 1/0.45    

def get_colorspace(colorspace):
    '''get colorspace by str'''
    if isinstance(colorspace, str):
        return globals()[colorspace]()
    return colorspace

def colorconvert(color, src, dst):
    '''convert between RGB color space'''
    return get_colorspace(dst).xyz2rgb(get_colorspace(src).rgb2xyz(color, D65_2), D65_2)

if __name__ == "__main__":
    pass
