import unittest
import sys
sys.path.append(r'./')
# print(sys.path)
from src.colorspace import *
from src.io_ import *
# import src
import numpy as np

array = np.array

def str2np(s):
    # s = '''0.4124564  0.3575761  0.1804375
    #     0.2126729  0.7151522  0.0721750
    #     0.0193339  0.1191920  0.9503041'''
    return  np.array([[float(x) for x in l.split()] for l in s.splitlines()])

class TestIO(unittest.TestCase):
    def test_singleton(self):
        # print(Singleton._instances)
        sRGB_t, sRGBL_t = bind(sRGB_)
        assert sRGB is sRGB_t
        assert sRGBL is sRGBL_t
        assert sRGB is not sRGBL_t
        assert sRGBL is not sRGB_t
        assert XYZ_D65_2 is XYZ()
        assert Lab_D65_2 is Lab(D65_2)

        assert AdobeRGB.l is AdobeRGBL
        assert WideGamutRGBL.nl is WideGamutRGB
        assert ProPhotoRGB.nl is ProPhotoRGB
        assert DCI_P3_RGBL.l is DCI_P3_RGBL
    
    def test_sRGB_M(self):
        # print('sRGB:', sRGB.M)
        np.testing.assert_array_almost_equal(sRGB.M, np.array(str2np('''0.4124564  0.3575761  0.1804375
                        0.2126729  0.7151522  0.0721750
                        0.0193339  0.1191920  0.9503041''')))

        np.testing.assert_array_almost_equal(sRGB.Mi, np.array(str2np('''3.2404542 -1.5371385 -0.4985314
                        -0.9692660  1.8760108  0.0415560
                        0.0556434 -0.2040259  1.0572252''')))

    def test_AdobeRGB_M(self):

        # print('AdobeRGB:', AdobeRGB.M)
        np.testing.assert_array_almost_equal(AdobeRGB.M, np.array(str2np('''0.5767309  0.1855540  0.1881852
                        0.2973769  0.6273491  0.0752741
                        0.0270343  0.0706872  0.9911085''')))

        np.testing.assert_array_almost_equal(AdobeRGB.Mi, np.array(str2np('''2.0413690 -0.5649464 -0.3446944
                        -0.9692660  1.8760108  0.0415560
                        0.0134474 -0.1183897  1.0154096''')))

    def test_WideGamutRGB_M(self):
        # print('WideGamutRGB:', WideGamutRGB.M)

        np.testing.assert_array_almost_equal(WideGamutRGB.M, np.array(str2np('''0.7161046  0.1009296  0.1471858
                        0.2581874  0.7249378  0.0168748
                        0.0000000  0.0517813  0.7734287''')), decimal=2)

        np.testing.assert_array_almost_equal(WideGamutRGB.Mi, np.array(str2np('''1.4628067 -0.1840623 -0.2743606
                        -0.5217933  1.4472381  0.0677227
                        0.0349342 -0.0968930  1.2884099''')), decimal=2)

    def test_ProPhotoRGB_M(self):
        # print('ProPhotoRGB:', ProPhotoRGB.M)
        np.testing.assert_array_almost_equal(ProPhotoRGB.M, np.array(str2np('''0.7976749  0.1351917  0.0313534
                        0.2880402  0.7118741  0.0000857
                        0.0000000  0.0000000  0.8252100''')), decimal=2)

        np.testing.assert_array_almost_equal(ProPhotoRGB.Mi, np.array(str2np('''1.3459433 -0.2556075 -0.0511118
                        -0.5445989  1.5081673  0.0205351
                        0.0000000  0.0000000  1.2118128''')), decimal=2)       

    def test_cam_1(self):
        np.testing.assert_array_almost_equal(XYZ._cam(D50_2, D65_2), np.array(str2np('''0.9555766 -0.0230393  0.0631636
                        -0.0282895  1.0099416  0.0210077
                        0.0122982 -0.0204830  1.3299098''')), decimal=4)        

    def test_cam_2(self):
        np.testing.assert_array_almost_equal(XYZ._cam(D55_2, D50_2, 'Von_Kries'), np.array(str2np('''1.0063032  0.0219819 -0.0223692
                        0.0024146  0.9981384 -0.0004869
                        0.0000000  0.0000000  0.8955170''')), decimal=4)                 

    def test_cam_3(self):  
        np.testing.assert_array_almost_equal(XYZ._cam(D65_2, D65_2), np.eye(3), decimal=4)  

    def test_cam_4(self):
        np.testing.assert_array_almost_equal(XYZ._cam(D65_2, D50_2, 'Identity'), np.array(str2np('''1.0144665  0.0000000  0.0000000
                        0.0000000  1.0000000  0.0000000
                        0.0000000  0.0000000  0.7578869''')), decimal=4)  
                       
if __name__ == '__main__':
    unittest.main()
    # str2np(None)
