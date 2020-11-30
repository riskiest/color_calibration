import unittest
import sys
sys.path.append(r'./')
# print(sys.path)
from src.utils import *
# import src
import numpy as np

array = np.array
na = np.testing.assert_array_almost_equal
color = 0


class TestIO(unittest.TestCase):
    def test_saturate(self):
        x = array([[0. , 0.5, 0. ],
                [0. , 0.3, 0.4],
                [0.3, 0.8, 0.4],
                [0.7, 0.6, 0.2],
                [1. , 0.8, 0.5]])
        assert (saturate(x, 0.2, 0.8)==array([False, False, True, True, False])).all()

    def test_gamma_correction(self):
        x = array([[0.8, -0.5, 0.6],
                [0.2, 0.9, -0.9],
                [1. , -0.2 , 0.4],
                [-0.4, 0.1, 0.3]])
        y = array([[ 0.6120656 , -0.21763764,  0.32503696],
                [ 0.02899119,  0.79311017, -0.79311017],
                [ 1.        , -0.02899119,  0.13320851],
                [-0.13320851,  0.00630957,  0.07074028]])
        na(gamma_correction(x, 2.2), y, decimal=4)

    def test_rgb2gray(self):
        x = array([0.2, 0.3, 0.4])
        y = 0.28596
        na(rgb2gray(x),y,decimal=4)
    
if __name__ == '__main__':
    unittest.main()
    # str2np(None)
