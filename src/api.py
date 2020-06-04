from .ccm import CCM_3x3

def color_calibration(src, colorchecker = 'Macbeth', ccm_shape = '3x3', saturated_threshold = (0.02, 0.98), 
        pre_linear = 'srgb', pre_gamma = None, pre_deg = None, 
        post_linear = 'srgb', post_gamma = None, post_deg = None,  
        distance = 'de00', initial_value = 'white_balance', method = 'Nelder-Mead', tol = 1e-4):
    '''
    src: input colorchecker patches colors; 24x3 numpy matrix; values are inside [0, 1];
    dst: output colorchecker patches; str; 
    ccm_shape: shape of color correction matrix (ccm); str; '3x3' now is the only one supported;
    saturated_threshold: upper and lower limit to determine if the patch is saturated; tuple;
    linear: str; linear_method;
    gamma: gamma value; float
    deg: polyfit value; int
    distance: color_distance; str;
    initial_value: the way to get initial value;
    method: nonlinear method;
    tolent: nonlinear tolent;
    '''
    return CCM_3x3(src, colorchecker, saturated_threshold, 
        pre_linear, pre_gamma, pre_deg, post_linear, post_gamma, post_deg, 
        distance, initial_value, method, tol)