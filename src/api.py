from .ccm import CCM_3x3

def color_calibration(src, colorchecker = 'Macbeth', ccm_shape = '3x3', saturated_threshold = (0.02, 0.98), 
        pre_linear = 'srgb', pre_gamma = None, pre_deg = None, 
        post_linear = 'srgb', post_gamma = None, post_deg = None,  
        distance = 'de00', initial_value = 'white_balance', xtol = 1e-4, ftol = 1e-4):
    '''
    src: input colorchecker patches colors; values are inside [0, 1];
        now 24x3 numpy matrix is the only supported;
    dst: the kind of colorchecker patches; str; 
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
            'gray_polyfit': use one polyfit function to fit from scr gray patches to dst gray patches;
                        and you should assign value to pre_deg;
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
    '''
    return CCM_3x3(src, colorchecker, saturated_threshold, 
        pre_linear, pre_gamma, pre_deg, post_linear, post_gamma, post_deg, 
        distance, initial_value, xtol, ftol)