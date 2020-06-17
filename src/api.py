from .ccm import *
def color_calibration(src, 
        dst = None, dst_colorspace = 'sRGB', 
            dst_illuminant  = None, dst_observer = None, dst_whites = None, 
        colorchecker = 'Macbeth_D65_2 ', 
        ccm_shape = '3x3', saturated_threshold = (0.02, 0.98), colorspace = 'sRGB',
        linear = 'gamma', gamma = None, deg = None, 
        distance = 'de00', dist_illuminant = 'D65', dist_observer = '2',
        weights_list = None, weights_coeff = 0, weight_color = False,
        initial_method = 'least_square', xtol = 1e-4, ftol = 1e-4):
        
    '''
    src: input colorchecker patches colors; values are inside [0, 1];
        now numpy matrix is the only supported;
    dst: the true value 
    colorchecker: the kind of colorchecker patches; str; 
        now only 'Macbeth' is supported.
    ccm_shape: shape of color correction matrix (ccm); str; 
        '3x3' now is the only supported;
    saturated_threshold: upper and lower limit to determine if the patch is saturated; tuple;
    pre_linear: the method of (de)linearizaton of src or input images; str; 
        now support:
            'gamma': (de)linearize src with gamma correction; and you should assign value to pre_gamma;
            'srgb': (de)linearize src with srgb way; 
            'color_polyfit': use three polyfit functions to fit from src-rgb to dst-rgbl; 
                        and you should assign value to pre_deg;
            'color_log_polyfit': log_polyfit version of color_polyfit;
            'gray_polyfit': use one polyfit function to fit from scr gray patches to dst gray patches;
                        and you should assign value to pre_deg;
            'gray_log_polyfit': log_polyfit version of gray_polyfit;
            'identity': do nothing; perfect for RAW file.
    pre-gamma: pre_linear gamma value; float; 2.2 is recommended.
    pre-deg: pre_linear polyfit degree; int; 3 is recommended.
    post_linear: the method of (de)linearizaton of dst or output images; str; 
        now support:
            'gamma': (de)linearize src with gamma correction; and you should assign value to post_gamma;
            'srgb': (de)linearize src with srgb way; 
            'identity': do nothing; perfect for RAW file.
    post-gamma: post_linear gamma value; float; 2.2 is recommended.
    post-deg: pre_linear polyfit degree; int; now it is useless in fact.
    weights_list: One can define weights color by color; numpy;
    weights_coeff: 

    distance: the way to calculate color difference; str;
        now support:
            'de00': ciede2000 
            'de94': cie94
            'de76': cie76
            'rgb': difference square between src-srgb with dst-srgb
    initial_value: the way to get initial value for nonlinear optimization;
        now support:
            'white_balance': diag{src-rgbl[0]/dst-rgbl[0], src-rgbl[1]/dst-rgbl[1], src-rgbl[1]/dst-rgbl[1]}
            'least_square': general-inverse(src-rgbl)*dst-rgbl
    xtol: ccm element tolent for nonlinear optimization;
    tolent: function-value tolent for nonlinear optimization;

    变量对照表：
    src, s: source;
    dst, d: destination;
    io: illuminant & observer; instance of class IO;
        sio, dio: source of io; destination of io;
    rgbl: linearization of rgb
    cs: colorspace;
    cc: colorchecker;
    M: matrix
    ccm: color correction matrix;
    cam: chromatic adaption matrix;
    '''
    return globals()['CCM_'+ccm_shape](src, dst, dst_colorspace, dst_illuminant, dst_observer, 
        dst_whites, colorchecker, saturated_threshold, colorspace, linear, gamma, deg, 
        distance, dist_illuminant, dist_observer, weights_list, weights_coeff, weight_color,
        initial_method, xtol, ftol)
