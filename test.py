from src.api import color_calibration
from src.colorchecker import ColorChecker2005_LAB_D50_2, ColorChecker2005_LAB_D65_2
from cv2 import cv2
import numpy as np
import os

fileDict = {'imgs/input1.png': np.array([[214.11,  98.67,  37.97],
       [231.94, 153.1 ,  85.27],
       [204.08, 143.71,  78.46],
       [190.58, 122.99,  30.84],
       [230.93, 148.46, 100.84],
       [228.64, 206.97,  97.5 ],
       [229.09, 137.07,  55.29],
       [189.21, 111.22,  92.66],
       [223.5 ,  96.42,  75.45],
       [201.82,  69.71,  50.9 ],
       [240.52, 196.47,  59.3 ],
       [235.73, 172.13,  54.  ],
       [131.6 ,  75.04,  68.86],
       [189.04, 170.43,  42.05],
       [222.23,  74.  ,  71.95],
       [241.01, 199.1 ,  61.15],
       [224.99, 101.4 , 100.24],
       [174.58, 152.63,  91.52],
       [248.06, 227.69, 140.5 ],
       [241.15, 201.38, 115.58],
       [236.49, 175.87,  88.86],
       [212.19, 133.49,  54.79],
       [181.17, 102.94,  36.18],
       [115.1 ,  53.77,  15.23]]),
       'imgs/input2.png': np.array([[ 50.9 ,  49.07,  20.62],
       [144.35, 142.37,  68.76],
       [ 58.45,  98.21,  76.68],
       [ 47.21,  64.9 ,  19.75],
       [ 75.94, 107.21,  88.47],
       [110.73, 193.01, 103.59],
       [169.94, 110.82,  22.24],
       [ 38.24,  74.13,  89.  ],
       [105.75,  63.45,  33.  ],
       [ 27.06,  33.33,  28.2 ],
       [156.78, 197.28,  44.47],
       [188.47, 155.32,  24.02],
       [ 19.35,  42.9 ,  63.2 ],
       [ 78.25, 131.45,  44.16],
       [ 74.04,  36.51,  14.55],
       [254.54, 251.8 ,  42.45],
       [ 98.13,  75.17,  67.1 ],
       [ 44.48, 114.7 ,  97.86],
       [255.  , 255.  , 255.  ],
       [254.96, 255.  , 201.62],
       [177.42, 222.95, 122.64],
       [ 95.35, 121.51,  66.48],
       [ 45.4 ,  59.18,  32.  ],
       [ 17.68,  23.99,  12.22]]),
       'imgs/input3.png': np.array([[ 46.91,  52.44,  42.82],
       [ 79.55,  91.72,  79.28],
       [ 51.57,  78.57,  82.  ],
       [ 45.05,  59.76,  42.57],
       [ 53.83,  75.32,  80.8 ],
       [ 62.35,  94.57,  83.76],
       [ 87.4 ,  77.66,  46.56],
       [ 43.46,  73.97,  90.7 ],
       [ 70.15,  63.79,  58.75],
       [ 35.12,  45.89,  51.37],
       [ 78.05,  98.41,  60.95],
       [ 81.89,  80.2 ,  42.7 ],
       [ 31.05,  61.54,  82.08],
       [ 64.01,  94.28,  68.84],
       [ 63.8 ,  51.19,  42.29],
       [105.98, 114.55,  62.56],
       [ 66.15,  68.64,  77.28],
       [ 42.77,  82.59,  86.94],
       [130.47, 169.14, 154.25],
       [107.98, 141.87, 130.75],
       [ 84.54, 111.66, 103.55],
       [ 61.9 ,  82.87,  76.68],
       [ 42.23,  56.92,  52.76],
       [ 21.6 ,  31.25,  27.78]])}

def test(filename, savetag, series_tag, L=False, **kwargs):
    print(f"======={savetag}===========")
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)/255.
    src = fileDict[filename]
    ccm = color_calibration(src/255, **kwargs)
    ccm.value(100000)
    img = ccm.infer_image(filename, L)
    head, end = os.path.splitext(filename)
    cv2.imwrite(head + '_' + str(series_tag) + str(savetag) + end, img)    

def test_1(series_tag='A'):
    test('imgs/input1.png', 1, series_tag)
    test('imgs/input1.png', 2, series_tag, ccm_shape = '4x3')
    # test('imgs/input1.png', 2, series_tag, linear='gray_polyfit', ccm_shape = '4x3')
    # test('imgs/input1.png', 3, series_tag, distance = 'rgbl', linear='gray_logpolyfit', deg = 3)
    # test('imgs/input1.png', 4, series_tag, L=True, linear='identity', distance = 'rgb')
    # test('imgs/input1.png', 5, series_tag, weights_coeff = 1, linear='color_polyfit', deg = 2)
    # test('imgs/input1.png', 6, series_tag, distance = 'de94', linear='color_logpolyfit', deg = 3)

def test_2(series_tag='A'):
    test('imgs/input2.png', 1, series_tag, distance = 'rgb', pre_linear='identity')
    test('imgs/input2.png', 2, series_tag, distance = 'de00', pre_linear='identity', post_linear='gamma', post_gamma=2.2)

def test_3(series_tag='A'):
    test('imgs/input3.png', 1, series_tag, distance = 'de00', pre_linear='gamma', pre_gamma=2.2,initial_value='least_square')
    test('imgs/input3.png', 2, series_tag, distance = 'de00', pre_linear='gamma', pre_gamma=2.2)
    test('imgs/input3.png', 3, series_tag, distance = 'de00', initial_value='least_square')
    test('imgs/input3.png', 4, series_tag, distance = 'de00', initial_value='least_square', pre_linear='color_polyfit', pre_deg = 3)
    test('imgs/input3.png', 5, series_tag, distance = 'de00', initial_value='least_square', pre_linear='gray_polyfit', pre_deg = 3)

if __name__ == "__main__":
    test_1()
    # test_2()
    # test_3()
