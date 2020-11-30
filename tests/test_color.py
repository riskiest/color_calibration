import unittest
import sys
sys.path.append(r'./')
# print(sys.path)
from src.colorspace import *
from src.io_ import *
from src.color import *
# import src
import numpy as np

array = np.array
na = np.testing.assert_array_almost_equal
color = 0

class TestIO(unittest.TestCase):
    def test_srgb(self):
        color = Color(np.array([0.3,0.2,0.5]), sRGB)
        color_rgb = color.to(sRGB)
        color_rgbl = color.to(sRGBL)
        color_xyz = color.to(XYZ_D65_2)
        color_lab = color.to(Lab_D65_2)
        color_xyz_d50 = color.to(XYZ_D50_2)
        color_lab_d50 = color.to(Lab_D50_2)

        np.testing.assert_array_almost_equal(color_rgb.colors, array([0.3,0.2,0.5]), decimal=4)
        np.testing.assert_array_almost_equal(color_rgbl.colors, array([0.07323896,0.03310477,0.21404114]), decimal=4)
        np.testing.assert_array_almost_equal(color_xyz.colors, array([0.080666, 0.054699, 0.208766]), decimal=4)
        np.testing.assert_array_almost_equal(color_lab.colors, array([28.0337, 29.9289, -39.4065]), decimal=2)
        np.testing.assert_array_almost_equal(color_xyz_d50.colors, array([0.075310, 0.053003, 0.157097]), decimal=4)
        np.testing.assert_array_almost_equal(color_lab_d50.colors, array([27.5736, 25.9112, -39.9261]), decimal=2)
        pass

    def test_adobergbl(self): 
        color = Color(np.array([[0.3,0.2,0.5],[0.7,0.1,0.4]]), AdobeRGBL)
        color_rgb = color.to(AdobeRGB)
        color_rgbl = color.to(AdobeRGBL)
        color_xyz = color.to(XYZ_D65_2)
        color_lab = color.to(Lab_D65_2)
        color_xyz_d50 = color.to(XYZ_D50_2)
        color_lab_d50 = color.to(Lab_D50_2)

        np.testing.assert_array_almost_equal(color_rgb.colors, array([[0.578533, 0.481157, 0.729740],
                                                            [0.850335, 0.351119, 0.659353]]), decimal=4)
        np.testing.assert_array_almost_equal(color_rgbl.colors, array([[0.3,0.2,0.5],[0.7,0.1,0.4]]), decimal=4)
        np.testing.assert_array_almost_equal(color_xyz.colors, array([[0.304223, 0.252320, 0.517802],
                                                            [0.497541, 0.301008, 0.422436]]), decimal=4)
        np.testing.assert_array_almost_equal(color_lab.colors, array([[57.3008, 26.0707, -29.7295],
                                                            [61.7411, 67.8735, -11.8328]]), decimal=2)
        np.testing.assert_array_almost_equal(color_xyz_d50.colors, array([[0.298587, 0.250078, 0.390442],
                                                            [0.507043, 0.305640, 0.317661]]), decimal=4)
        np.testing.assert_array_almost_equal(color_lab_d50.colors, array([[57.0831, 23.2605, -29.8401],
                                                            [62.1379, 66.7756, -10.7684]]), decimal=2)
        pass

    def test_xyz(self):
        color = Color(np.array([0.3,0.2,0.5]), XYZ_D65_2)
        color_rgb = color.to(ProPhotoRGB, 'Von_Kries')
        color_rgbl = color.to(ProPhotoRGBL, 'Von_Kries')
        color_xyz = color.to(XYZ_D65_2, 'Von_Kries')
        color_lab = color.to(Lab_D65_2, 'Von_Kries')
        color_xyz_d50 = color.to(XYZ_D50_2, 'Von_Kries')
        color_lab_d50 = color.to(Lab_D50_2, 'Von_Kries')
      
        na(color_rgb.colors, array([0.530513,0.351224,0.648975]), decimal=4)
        na(color_rgbl.colors, array([0.319487,0.152073,0.459209]), decimal=4)
        na(color_xyz.colors, array([0.3,0.2,0.5]), decimal=4)
        na(color_lab.colors, array([51.8372, 48.0307, -37.3395]), decimal=2)
        na(color_xyz_d50.colors, array([0.289804, 0.200321, 0.378944]), decimal=4)
        na(color_lab_d50.colors, array([51.8735, 42.3654, -37.2770]), decimal=2)
        pass

    def test_lab(self):
        color = Color(np.array([30., 20., 10.]), Lab_D50_2)
        color_rgb = color.to(AppleRGB, 'Identity')
        color_rgbl = color.to(AppleRGBL, 'Identity')
        color_xyz = color.to(XYZ_D65_2, 'Identity')
        color_lab = color.to(Lab_D65_2, 'Identity')
        color_xyz_d50 = color.to(XYZ_D50_2, 'Identity')
        color_lab_d50 = color.to(Lab_D50_2, 'Identity')
      
        na(color_rgb.colors, array([0.323999,0.167314,0.165874]), decimal=4)
        na(color_rgbl.colors, array([0.131516,0.040028,0.039410]), decimal=4)
        na(color_xyz.colors, array([0.079076, 0.062359, 0.045318]), decimal=4)
        na(color_lab.colors, array([30.0001, 19.9998, 9.9999]), decimal=2)        
        na(color_xyz_d50.colors, array([0.080220,0.062359,0.034345]), decimal=4)
        na(color_lab_d50.colors, array([30,20,10]), decimal=2)


    def test_grays(self):
        grays = np.array([False, False, False, False, False, False,
                        False, False, False, False,False, False,
                        False, False, False, False,False, False,
                        True, True, True, True, True, True])
        a = Macbeth_D50_2
        a.get_gray()
        b = Macbeth_D65_2
        b.get_gray()
        assert (a.grays==grays).all()
        assert (b.grays==grays).all()

    def test_gray_luminant(self):        
        color = Color(np.array([0.3,0.2,0.5]), sRGB)
        na(color.toGray(color.cs.io),np.array([0.054699]), decimal=4)
        na(color.toLuminant(color.cs.io),np.array([28.0337]), decimal=4)
        color = Color(np.array([[0.3,0.2,0.5],[0.7,0.1,0.4]]), sRGB)
        na(color.toGray(color.cs.io),np.array([0.054699,0.112033]), decimal=4)
        na(color.toLuminant(color.cs.io),np.array([28.0337,39.9207]), decimal=4)

    def test_diff(self):
        color1 = Color(np.array([0.3,0.2,0.5]), sRGB)
        color2 = Color(np.array([0.3,0.2,0.5]), XYZ_D50_2)
        # print(color1.to(sRGBL).colors)
        # print(color2.to(sRGBL).colors)
        
        na(color1.diff(color2, method='de00', io=D65_2), np.array([22.58031]), decimal=2)
        na(color1.diff(color2, method='de94', io=D65_2), np.array([25.701214]), decimal=2)
        na(color1.diff(color2, method='de76', io=D65_2), np.array([34.586351]), decimal=2)
        na(color1.diff(color2, method='cmc', io=D65_2), np.array([33.199419]), decimal=2)
        na(color1.diff(color2, method='rgb', io=D65_2), np.array([0.51057]), decimal=4)
        na(color1.diff(color2, method='rgbl', io=D65_2), np.array([0.556741]), decimal=4)

if __name__ == '__main__':
    unittest.main()
    # str2np(None)
