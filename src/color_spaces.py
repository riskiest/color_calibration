from skimage import color
import numpy as np

def saturate(src, low, up):
    return np.all(np.logical_and(src>=low,src<=up), axis = 1)

# =================color conversion functions =================
def rgb2rgbl(rgb):
    # 考虑到转换后可能是负数，这里使用matlab类似的方法
    def _rgb2rgbl_ele(x):
        if x>0.04045:
            return ((x+0.055)/1.055)**2.4
        elif x>=-0.04045:
            return x/12.92
        else:
            return -(((-x+0.055)/1.055)**2.4)
    return np.vectorize(_rgb2rgbl_ele)(rgb)
    # RGB变成线性 rgb->rgbl
    # because (x, y, z).T = xyz-from-rgb @ (rl, gl, bl).T
    # so (rl, gl, bl) = (x, y, z) @ (rgb-from-xyz).T = rgb2xyz(rgb) @ (rgb-from-xyz).T
    # return (color.colorconv.rgb2xyz(rgb/255)@(color.colorconv.rgb_from_xyz.T))*255

def rgbl2rgb(rgbl):
    def _rgbl2rgb_ele(x):
        if x>0.0031308:
            return 1.055*(x**(1/2.4))-0.055
        elif x>=-0.0031308:
            return x*12.92
        else:
            return -(1.055*((-x)**(1/2.4))-0.055)
    return np.vectorize(_rgbl2rgb_ele)(rgbl)


def gamma_correction(rgb, gamma):
    # 使用gamma进行线性化
    arr = rgb.copy()
    mask = rgb>=0
    arr[mask] = np.power(arr[mask], gamma)
    arr[~mask] = -np.power(-arr[~mask], gamma)
    return arr

def rgbl2xyz(rgbl):
    return rgbl@(color.colorconv.xyz_from_rgb.T)

def xyz2rgbl(xyz):
    return xyz@(color.colorconv.rgb_from_xyz.T)

def rgbl2lab(rgbl):
    '''rgbl->lab'''
    return color.colorconv.xyz2lab(rgbl2xyz(rgbl))

def lab2rgbl(lab):
    '''lab->rgbl'''
    return xyz2rgbl(color.colorconv.lab2xyz(lab))

def lab2xyz(lab):
    return color.colorconv.lab2xyz(lab)

def rgb2gray(rgb):
    return np.squeeze(color.colorconv.rgb2gray(rgb[np.newaxis,...]), axis=0)

# ========distance==================
def distance_de00(src_lab, dst_lab):
    return color.deltaE_ciede2000(src_lab, dst_lab)

def distance_de94(src_lab, dst_lab):
    return color.deltaE_ciede94(src_lab, dst_lab)

def distance_de76(src_lab, dst_lab):
    return color.deltaE_cie76(src_lab, dst_lab)

def distance_rgb(src_rgbl, dst_rgbl):
    return color.deltaE_cie76(src_rgbl, dst_rgbl)

