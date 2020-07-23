from .ccm import *
def color_calibration(src,
        dst,
        # dst = None, dst_colorspace = 'sRGB', 
        #     dst_illuminant  = None, dst_observer = None, dst_whites = None, 
        # colorchecker = 'Macbeth_D65_2', 
        ccm_shape = '3x3', 
        colorspace = 'sRGB',
        distance = 'de00', 
        saturated_threshold = (0, 0.98), 
        linear = 'gamma', gamma = 2.2, deg = 3, 
        # dist_illuminant = 'D65', dist_observer = '2',
        weights_list = None, weights_coeff = 0, 
        # weights_color = False,
        initial_method = 'least_square', xtol = 1e-4, ftol = 1e-4):
        
    '''
    src: 
        detected colors of ColorChecker patches;
        NOTICE: the color type is RGB not BGR, and the color values are in [0, 1];
        type: np.array(np.double)

    # ============ split line =====================
    You can set reference colors either by dst dst_colorspace dst_illuminant dst_observer
        or by colorchecker;

    dst: 
        the reference colors;
        NOTICE: the color type is some RGB color space or CIE Lab color space;
                If the color type is RGB, the format is RGB not BGR, and the color 
                values are in [0, 1];
        type: np.array(np.double);

    dst_colorspace: 
        the color space of the reference colors;
        NOTICE: it could be some RGB color space or CIE Lab color space;
                For the list of RGB color spaces supported, see the notes below;
        type: str;
    
    dst_illuminant:
        the illuminant of the reference color space;
        NOTICE: the option is for CIE Lab color space;
                if dst_colorspace is some RGB color space, the option would be ignored;
                For the list of the illumiant supported, see the notes below;
        type: str;
    
    dst_observer:
        the observer of the reference color space;
        NOTICE: the option is for CIE Lab color space;
                if dst_colorspace is some RGB color space, the option would be ignored;
                For the list of the observer supported, see the notes below;
        type: str;
    
    dst_whites:
        the indice list of gray colors of the reference colors;
        NOTICE: If it is set to None, some linearize method would not work;
        type: np.array(np.int);

    colorchecker:
        the name of the ColorChecker;
        Supported list:
            "Macbeth": Macbeth ColorChecker with 2deg D50;
            "Macbeth_D65_2": Macbeth ColorChecker with 2deg D65;
        NOTICE: you can either set the reference by variables starting with dst or this;
                The option works only if dst is set to None.
        type: str;
    
    # ============ split line =====================
    ccm_shape:
        the shape of color correction matrix(CCM);
        Supported list:
            "3x3": 3x3 matrix;
            "4x3": 4x3 matrix;
        type: str
    
    saturated_threshold:
        the threshold to determine saturation;
        NOTICE: it is a tuple of [low, up]; 
                The colors in the closed interval [low, up] are reserved to participate 
                in the calculation of the loss function and initialization parameters.
        type: tuple of [low, up];
    
    colorspace:
        the absolute color space that detected colors convert to;
        NOTICE: it could be some RGB color space;
                For the list of RGB color spaces supported, see the notes below;
        type: str;
    
    # ============ split line =====================
    linear:
        the method of linearization;
        NOTICE: see Linearization.pdf for details;
        Supported list:
            "identity": no change is made;
            "gamma": gamma correction;
                     Need assign a value to gamma simultaneously;
            "color_polyfit": polynomial fitting channels respectively;
                             Need assign a value to deg simultaneously;
            "gray_polyfit": grayscale polynomial fitting;
                            Need assign a value to deg and dst_whites simultaneously;
            "color_logpolyfit": logarithmic polynomial fitting channels respectively;
                             Need assign a value to deg simultaneously;
            "gray_logpolyfit": grayscale Logarithmic polynomial fitting;
                            Need assign a value to deg and dst_whites simultaneously;
        type: str;
    
    gamma:
        the gamma value of gamma correction;
        NOTICE: only valid when linear is set to "gamma";
        type: float;
    
    deg:
        the degree of linearization polynomial;
        NOTICE: only valid when linear is set to "color_polyfit", "gray_polyfit", 
                "color_logpolyfit" and "gray_logpolyfit";
        type: int;

    # ============ split line =====================
    distance:
        the type of color distance;
        Supported list:
            'de00': ciede2000 
            'de94': cie94
            'de76': cie76
            'cmc': CMC l:c (1984)
            'rgb': Euclidean distance of rgb color space;
            'rgbl': Euclidean distance of rgbl color space;
        type: str;
    
    dist_illuminant:
        the illuminant of CIE lab color space associated with distance function;
        NOTICE: only valid when distance is set to 'de00', 'de94', 'de76' and 'cmc'; 
                For the list of the illumiant supported, see the notes below;
        type: str;    

    dist_observer:
        the observer of CIE lab color space associated with distance function;
        NOTICE: only valid when distance is set to 'de00', 'de94', 'de76' and 'cmc'; 
                For the list of the observer supported, see the notes below;
        type: str;   

    # ============ split line =====================
    There are some ways to set weights:
        1. set weights_list only;
        2. set weights_coeff only;
        3. set weights_color only;
        4. set weights_coeff and weights_color;
    see CCM.pdf for details;

    weights_list:
        the list of weight of each color;
        type: np.array(np.double)
    
    weights_coeff:
        the exponent number of L* component of the reference color in CIE Lab color space;
        type: float
    
    weights_color:
        if it is set to True, only non-gray color participate in the calculation 
        of the loss function.
        NOTICE: only valid when dst_whites is assigned.
        type: float

    # ============ split line =====================
    initial_method:
        the method of calculating CCM initial value;
        see CCM.pdf for details;
        Supported list:
            'least_square': least-squre method;
            'white_balance': white balance method;
        type: str;
    
    xtol, ftol:
        absolute error in independent variables or function values 
        between iterations that is acceptable for convergence;
        type: float;
    
    # ============ split line =====================
    Supported list of illuminants:
        'A';
        'D50';
        'D55';
        'D65';
        'D75';
        'E';
    
    Supported list of observers:
        '2';
        '10';
    
    Supported list of RGB color spaces:
        'sRGB';
        'AdobeRGB';
        'WideGamutRGB';
        'ProPhotoRGB';
        'DCI_P3_RGB';
        'AppleRGB';
        'REC_709_RGB';
        'REC_2020_RGB';
    
    # ============ split line =====================
    Abbr.

        src, s: source;
        dst, d: destination;
        io: illuminant & observer;
        sio, dio: source of io; destination of io;
        rgbl: linear RGB
        cs: color space;
        cc: Colorchecker;
        M: matrix
        ccm: color correction matrix;
        cam: chromatic adaption matrix;
    '''
    return globals()['CCM_'+ccm_shape](src,
        dst,
        ccm_shape, 
        colorspace,
        distance, 
        saturated_threshold, 
        linear, gamma, deg, 
        weights_list, weights_coeff, 
        # weights_color,
        initial_method, xtol, ftol)
