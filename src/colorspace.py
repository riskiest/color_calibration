import numpy as np
from skimage import color
from .utils import *

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

class RGB_Base:
    def __init__(self):
        self.xr, self.yr = 0.6400, 0.3300	
        self.xg, self.yg = 0.21, 0.71
        self.xb, self.yb = 0.1500, 0.0600
        self.io_base = D65_2
        # self.obs_base = '2'
        self.gamma = 2.2  
        self._M_RGBL2XYZ_base = None
        self._M_RGBL2XYZ = {}
        self._default_io = D65_2
    
    def cal_M_RGBL2XYZ_base(self):
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
        if self._M_RGBL2XYZ_base:
            return self._M_RGBL2XYZ_base
        return self.cal_M_RGBL2XYZ_base()

    def get_default(self, io = None):
        return io or self._default_io
    
    def set_default(self, io):
        self._default_io = io
    
    # def get_default(self):
    #     return self._default_io
        # self._default_obs = obs
        
    def M_RGBL2XYZ(self, io = None, rev = False):
        io = self.get_default(io)
        if io in self._M_RGBL2XYZ:
            return self._M_RGBL2XYZ[io][1 if rev else 0]
        if io==self.io_base:
            self._M_RGBL2XYZ[io] = (self.M_RGBL2XYZ_base, np.linalg.inv(self.M_RGBL2XYZ_base))
            return self._M_RGBL2XYZ[io][1 if rev else 0]
        M_RGBL2XYZ = cam(self.io_base, io)@self.M_RGBL2XYZ_base
        self._M_RGBL2XYZ[io] = (M_RGBL2XYZ, np.linalg.inv(M_RGBL2XYZ))
        return self._M_RGBL2XYZ[io][1 if rev else 0]

    def rgbl2xyz(self, rgbl, io = None):
        io = self.get_default(io)
        return rgbl@(self.M_RGBL2XYZ(io).T)
    
    def xyz2rgbl(self, xyz, io = None):
        io = self.get_default(io)
        return xyz@(self.M_RGBL2XYZ(io, True).T)

    def rgb2rgbl(self, rgb):
        return gamma_correction(rgb, self.gamma)
    
    def rgbl2rgb(self, rgbl):
        return gamma_correction(rgbl, 1/self.gamma)

    def rgb2xyz(self, rgb, io = None):
        io = self.get_default(io)
        return self.rgbl2xyz(self.rgb2rgbl(rgb), io) 

    def xyz2rgb(self, xyz, io = None):
        io = self.get_default(io)
        return self.rgbl2rgb(self.xyz2rgbl(xyz, io)) 

    def rgbl2lab(self, rgbl, io = None):
        io = self.get_default(io)
        return xyz2lab(self.rgbl2xyz(rgbl, io), io)
    
    def rgb2lab(self, rgb, io = None):
        io = self.get_default(io)
        return self.rgbl2lab(self.rgb2rgbl(rgb), io)
        
class sRGB_Base(RGB_Base):
    # Data from http://www.brucelindbloom.com/index.html?ColorCheckerRGB.html
    def __init__(self):
        super().__init__()
        self.xr, self.yr = 0.6400, 0.3300	
        self.xg, self.yg = 0.3000, 0.6000
        self.xb, self.yb = 0.1500, 0.0600
        # ============
        # L: linear, N: non-linear, K0 = beta*phi
        # N = L/beta L<=K0
        #   = ((L+alpha-1)/alpha)^gamma L>K0
        # L = N*beta N<=phi
        #   = alpha*N^(1/gamma)-(alpha-1)
        # ============        
        self.alpha, self.beta, self.phi, self.gamma = 1.055, 0.0031308, 12.92, 2.4
        self._K0 = None

    @property
    def K0(self):
        if self._K0:
            return self._K0
        return self.beta*self.phi

    def rgb2rgbl(self, rgb):
        def _rgb2rgbl_ele(x):
            if x>self.K0:
                return ((x+self.alpha-1)/self.alpha)**self.gamma
            elif x>=-self.K0:
                return x/self.phi
            else:
                return -(((-x+self.alpha-1)/self.alpha)**self.gamma)
        return np.vectorize(_rgb2rgbl_ele)(rgb)  
    
    def rgbl2rgb(self, rgbl):
        # rgbl->rgb
        def _rgbl2rgb_ele(x):
            if x>self.beta:
                return self.alpha*(x**(1/self.gamma))-(self.alpha-1)
            elif x>=-self.beta:
                return x*self.phi
            else:
                return -(self.alpha*((-x)**(1/self.gamma))-(self.alpha-1))
        return np.vectorize(_rgbl2rgb_ele)(rgbl)    


class sRGB(sRGB_Base):
    # Data from http://www.brucelindbloom.com/index.html?ColorCheckerRGB.html
    def __init__(self):
        super().__init__()
        self.M_RGBL2XYZ_base = np.array([[0.41239080, 0.35758434, 0.18048079],
                [0.21263901 ,0.71516868 ,0.07219232],
                [0.01933082 ,0.11919478 ,0.95053215]])

class AdobeRGB(RGB_Base):
    pass

class WideGamutRGB(RGB_Base):
    def __init__(self):
        super().__init__()    	
        # https://en.wikipedia.org/wiki/Wide-gamut_RGB_color_space
        self.xr, self.yr = 0.7347, 0.2653	
        self.xg, self.yg = 0.1152, 0.8264
        self.xb, self.yb = 0.1566, 0.0177
        self.ill_base = 'D50'

class ProPhotoRGB(RGB_Base):
    def __init__(self):
        super().__init__()    	
        # https://en.wikipedia.org/wiki/ProPhoto_RGB_color_space
        self.xr, self.yr = 0.734699, 0.265301	
        self.xg, self.yg = 0.159597, 0.840403
        self.xb, self.yb = 0.036598, 0.000105
        self.ill_base = 'D50'    

class DCI_P3_RGB(RGB_Base):
    def __init__(self):
        super().__init__()    	
        # https://en.wikipedia.org/wiki/ProPhoto_RGB_color_space
        self.xr, self.yr = 0.680, 0.32	
        self.xg, self.yg = 0.265, 0.69
        self.xb, self.yb = 0.15, 0.06

class AppleRGB(RGB_Base):
    def __init__(self):
        super().__init__()    	
        # https://en.wikipedia.org/wiki/ProPhoto_RGB_color_space
        self.xr, self.yr = 0.625, 0.34	
        self.xg, self.yg = 0.28, 0.595
        self.xb, self.yb = 0.155, 0.07
        self.gamma = 1.8

class REC_709_RGB(sRGB_Base):
    def __init__(self):
        super().__init__()    	
        # https://en.wikipedia.org/wiki/ProPhoto_RGB_color_space
        self.xr, self.yr = 0.64, 0.33	
        self.xg, self.yg = 0.3, 0.6
        self.xb, self.yb = 0.15, 0.06
        self.alpha, self.beta, self.phi, self.gamma = 1.099, 0.018, 4.5, 1/0.45
 
class REC_2020_RGB(sRGB_Base):
    def __init__(self):
        super().__init__()    	
        # https://en.wikipedia.org/wiki/ProPhoto_RGB_color_space
        self.xr, self.yr = 0.708, 0.292	
        self.xg, self.yg = 0.17, 0.797
        self.xb, self.yb = 0.131, 0.046
        self.alpha, self.beta, self.phi, self.gamma = 1.09929682680944, 0.018053968510807, 4.5, 1/0.45    

def get_colorspace(colorspace):
    if isinstance(colorspace, str):
        return globals()[colorspace]
    return colorspace

def colorconvert(color, src, dst):
    return get_colorspace(dst).xyz2rgb(get_colorspace(src).rgb2xyz(color, D65_2), D65_2)

if __name__ == "__main__":
    pass
