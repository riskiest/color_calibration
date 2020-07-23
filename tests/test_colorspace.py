import unittest
import sys
sys.path.append(r'./')
# print(sys.path)
from newsrc.colorspace import *
from newsrc.io_ import *
# import newsrc
import numpy as np

array = np.array

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
        # AdobeRGB, AdobeRGBL = bind(AdobeRGB_)
        # WideGamutRGB, WideGamutRGBL = bind(WideGamutRGB_)
        # ProPhotoRGB, ProPhotoRGBL = bind(ProPhotoRGB_)
        # DCI_P3_RGB, DCI_P3_RGBL = bind(DCI_P3_RGB_)
        # AppleRGB, AppleRGBL = bind(AppleRGB_)
        # REC_709_RGB, REC_709_RGBL = bind(REC_709_RGB_)
        # REC_2020_RGB, REC_2020_RGBL = bind(REC_2020_RGB_)
        # for k in illuminants_:
        #     assert k in illuminants
        #     np.testing.assert_array_almost_equal(illuminants_[k], illuminants[k])

if __name__ == '__main__':
    unittest.main()
