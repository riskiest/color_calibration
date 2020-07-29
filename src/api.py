from .ccm import *
from .color import *

def color_calibration(src, dst, colorspace = sRGB,
        ccm_shape = '3x3', 
        distance = 'de00', 
        linear = 'gamma', gamma = 2.2, deg = 3, 
        saturated_threshold = (0, 0.98), weights_list = None, weights_coeff = 0, 
        initial_method = 'least_square', xtol = 1e-4, ftol = 1e-4):
        
    '''
    # ============ split line =====================
    src: 
        detected colors of ColorChecker patches;
        NOTICE: the color type is RGB not BGR, and the color values are in [0, 1];
        type: np.array(np.double)

    dst: 
        the reference colors;
        NOTICE: Built-in color card or custom color card are supported.
                Built-in:
                    Macbeth_D50_2: Macbeth ColorChecker with 2deg D50;
                    Macbeth_D65_2: Macbeth ColorChecker with 2deg D65;
                Custom:
                    You should use color.Color(color_value, color_space)
                    For the list of color spaces supported, see the notes below;
                    If the color type is some RGB, the format is RGB not BGR, and the color 
                    values are in [0, 1];
        type: color.Color;

    colorspace:
        the absolute color space that detected colors convert to;
        NOTICE: it should be some RGB color space;
                For the list of RGB color spaces supported, see the notes below;
        type: colorspace.ColorSpace;

    # ============ split line =====================
    ccm_shape:
        the shape of color correction matrix(CCM);
        Supported list:
            "3x3": 3x3 matrix;
            "4x3": 4x3 matrix;
        type: str

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
    saturated_threshold:
        the threshold to determine saturation;
        NOTICE: it is a tuple of [low, up]; 
                The colors in the closed interval [low, up] are reserved to participate 
                in the calculation of the loss function and initialization parameters.
        type: tuple of [low, up];
    
    # ============ split line =====================
    There are some ways to set weights:
        1. set weights_list only;
        2. set weights_coeff only;
    see CCM.pdf for details;

    weights_list:
        the list of weight of each color;
        type: np.array(np.double)
    
    weights_coeff:
        the exponent number of L* component of the reference color in CIE Lab color space;
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
    Supported Color Space:
        Supported list of RGB color spaces:
            sRGB;
            AdobeRGB;
            WideGamutRGB;
            ProPhotoRGB;
            DCI_P3_RGB;
            AppleRGB;
            REC_709_RGB;
            REC_2020_RGB;

        Supported list of linear RGB color spaces:
            sRGBL;
            AdobeRGBL;
            WideGamutRGBL;
            ProPhotoRGBL;
            DCI_P3_RGBL;
            AppleRGBL;
            REC_709_RGBL;
            REC_2020_RGBL;

        Supported list of non-RGB color spaces:
            Lab_D50_2;
            Lab_D65_2;
            XYZ_D50_2;
            XYZ_D65_2;
        
        Supported IO (You can use Lab(io) or XYZ(io) to create color space):
            A_2;
            A_10;
            D50_2;
            D50_10;
            D55_2;
            D55_10;
            D65_2;
            D65_10;
            D75_2;
            D75_10;
            E_2;
            E_10;         
            
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

    return globals()['CCM_'+ccm_shape](src, dst, colorspace,
        distance, 
        linear, gamma, deg, 
        saturated_threshold, weights_list, weights_coeff, 
        initial_method, xtol, ftol)
