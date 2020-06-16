import numpy as np
from skimage import color

# some convection functions
def xyY2XYZ(x,y,Y=1):
    X = Y*x/y
    Z = Y/y*(1-x-y)
    return np.array([X,Y,Z])

def xyz2grayl(xyz):
    return xyz[..., 1]

def xyz2lab(xyz, illuminant='D65', observer='2'):
    return color.colorconv.xyz2lab(xyz, illuminant, observer)

def lab2xyz(lab, illuminant='D65', observer='2'):
    return color.colorconv.lab2xyz(lab, illuminant, observer)

def xyz2xyz(xyz, src_ill, src_obs, dst_ill, dst_obs):
    return cam(src_ill, src_obs, dst_ill, dst_obs)@xyz

def lab2lab(lab, src_ill, src_obs, dst_ill, dst_obs):
    return xyz2lab(xyz2xyz(lab2xyz(lab, src_ill, src_obs), src_ill, src_obs, dst_ill, dst_obs), dst_ill, dst_obs) 

# gamma correction ...
def gamma_correction(rgb, gamma):
    arr = rgb.copy()
    mask = rgb>=0
    arr[mask] = np.power(arr[mask], gamma)
    arr[~mask] = -np.power(-arr[~mask], gamma)
    return arr

# illuminant matrices....
def get_illuminant():
    # data from https://en.wikipedia.org/wiki/Standard_illuminant
    illuminants_xy = \
        {"A": {'2': (0.44757, 0.40745),
            '10': (0.45117, 0.40594)},
        "D50": {'2': (0.34567, 0.35850),
                '10': (0.34773, 0.35952)},
        "D55": {'2': (0.33242, 0.34743),
                '10': (0.33411, 0.34877)},
        "D65": {'2': (0.31271, 0.32902),  
                '10': (0.31382, 0.33100)},
        "D75": {'2': (0.29902, 0.31485),
                '10': (0.29968, 0.31740)},
        "E": {'2': (1/3, 1/3),
            '10': (1/3, 1/3)}}

    illuminants = illuminants_xy.copy()
    for illuminant, value in illuminants_xy.items():
        for observer, (x, y) in value.items():
            illuminants[illuminant][observer] = xyY2XYZ(x, y)

    # data from https://en.wikipedia.org/wiki/Illuminant_D65
    illuminants["D65"]['2']=np.array([0.95047, 1., 1.08883])
    illuminants["D65"]['10']=np.array([0.94811, 1., 1.07304])
    return illuminants_xy, illuminants

illuminants_xy, illuminants = get_illuminant()

# chromatic adaption matrices
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
def cam(src_ill='D50', src_obs='2', dst_ill='D65', dst_obs='2', method = 'Bradford'):
    if (src_ill, src_obs, dst_ill, dst_obs) in CAMs:
        return CAMs[(src_ill, src_obs, dst_ill, dst_obs)]
    # function from http://www.brucelindbloom.com/index.html?ColorCheckerRGB.html
    XYZws = illuminants[src_ill][src_obs]
    XYZWd = illuminants[dst_ill][dst_obs]
    MA, MA_inv = MAs[method]
    M = MA_inv@np.diag((MA@XYZWd)/(MA@XYZws))
    CAMs[(src_ill, src_obs, dst_ill, dst_obs)] = M
    return M

class RGB_Base:
    def __init__(self):
        self.xr, self.yr = 0.6400, 0.3300	
        self.xg, self.yg = 0.21, 0.71
        self.xb, self.yb = 0.1500, 0.0600
        self.ill_base = 'D65'
        self.obs_base = '2'
        self.gamma = 2.2  
        self._M_RGBL2XYZ_base = None
        self._M_RGBL2XYZ = {}
        self._default_ill = 'D65'
        self._default_obs = '2'
    
    def cal_M_RGBL2XYZ_base(self):
        XYZr = xyY2XYZ(self.xr, self.yr)
        XYZg = xyY2XYZ(self.xg, self.yg)
        XYZb = xyY2XYZ(self.xb, self.yb)
        XYZw = illuminants[self.ill_base][self.obs_base]
        XYZ_rgbl = np.stack([XYZr, XYZg, XYZb], axis= 1)
        Sr, Sg, Sb = np.linalg.solve(XYZ_rgbl, XYZw)
        self._M_RGBL2XYZ_base = np.stack([Sr*XYZr, Sg*XYZg, Sb*XYZb], axis= 1)  
        return self._M_RGBL2XYZ_base      

    @property
    def M_RGBL2XYZ_base(self):
        if self._M_RGBL2XYZ_base:
            return self._M_RGBL2XYZ_base
        return self.cal_M_RGBL2XYZ_base()

    def _default(self, ill, obs):
        if ill is None:
            ill = self._default_ill
        if obs is None:
            obs = self._default_obs
        return ill, obs
    
    def set_default(self, ill, obs):
        self._default_ill = ill
        self._default_obs = obs
        
    def M_RGBL2XYZ(self, ill = None, obs = None, rev = False):
        ill, obs = self._default(ill, obs)
        if (ill, obs) in self._M_RGBL2XYZ:
            return self._M_RGBL2XYZ[(ill, obs)][1 if rev else 0]
        if ill == self.ill_base and obs == self.obs_base:
            self._M_RGBL2XYZ[(ill, obs)] = (self.M_RGBL2XYZ_base, np.linalg.inv(self.M_RGBL2XYZ_base))
            return self._M_RGBL2XYZ[(ill, obs)][1 if rev else 0]
        M_RGBL2XYZ = cam(self.ill_base, self.obs_base, ill, obs)@self.M_RGBL2XYZ_base
        self._M_RGBL2XYZ[(ill, obs)] = (M_RGBL2XYZ, np.linalg.inv(M_RGBL2XYZ))
        return self._M_RGBL2XYZ[(ill, obs)][1 if rev else 0]

    def rgbl2xyz(self, rgbl, ill = None, obs = None):
        ill, obs = self._default(ill, obs)
        return rgbl@(self.M_RGBL2XYZ(ill, obs).T)
    
    def xyz2rgbl(self, xyz, ill = None, obs = None):
        ill, obs = self._default(ill, obs) 
        return xyz@(self.M_RGBL2XYZ(ill, obs, True).T)

    def rgb2rgbl(self, rgb):
        return gamma_correction(rgb, self.gamma)
    
    def rgbl2rgb(self, rgbl):
        return gamma_correction(rgbl, 1/self.gamma)

    def rgb2xyz(self, rgb, ill = None, obs = None):
        ill, obs = self._default(ill, obs)
        return self.rgbl2xyz(self.rgb2rgbl(rgb), ill, obs) 

    def xyz2rgb(self, xyz, ill = None, obs = None):
        ill, obs = self._default(ill, obs)
        return self.rgbl2rgb(self.xyz2rgbl(xyz, ill, obs)) 

    def rgbl2lab(self, rgbl, ill = None, obs = None):
        ill, obs = self._default(ill, obs)
        return xyz2lab(self.rgbl2xyz(rgbl, ill, obs), ill, obs)
    
    def rgb2lab(self, rgb, ill = None, obs = None):
        ill, obs = self._default(ill, obs)
        return self.rgbl2lab(self.rgb2rgbl(rgb), ill, obs)
        
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

if __name__ == "__main__":
    pass
