from skimage import color
import numpy as np

def distance_de00(src_lab, dst_lab):
    return color.deltaE_ciede2000(src_lab, dst_lab)

def distance_de94(src_lab, dst_lab):
    return color.deltaE_ciede94(src_lab, dst_lab)

def distance_de76(src_lab, dst_lab):
    return color.deltaE_cie76(src_lab, dst_lab)

distance_rgbl = distance_rgb = distance_de76

