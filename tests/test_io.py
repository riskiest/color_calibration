import unittest
import sys
sys.path.append(r'./')
# print(sys.path)
from src.io_ import *
# import src
import numpy as np

array = np.array


class TestIO(unittest.TestCase):
    def test_illuminants(self):
        illuminants_ = {A_2: array([1.098466069456375, 1, 0.3558228003436005]), 
                    A_10: array([1.111420406956693, 1, 0.3519978321919493]), 
                    D50_2: array([0.9642119944211994, 1, 0.8251882845188288]), 
                    D50_10: array([0.9672062750333777, 1, 0.8142801513128616]), 
                    D55_2: array([0.956797052643698, 1, 0.9214805860173273]), 
                    D55_10: array([0.9579665682254781, 1, 0.9092525159847462]), 
                    D65_2: array([0.95047, 1., 1.08883]), 
                    D65_10: array([0.94811, 1., 1.07304]), 
                    D75_2: array([0.9497220898840717, 1, 1.226393520724154]), 
                    D75_10: array([0.9441713925645873, 1, 1.2064272211720228]), 
                    E_2: array([1., 1., 1.]), 
                    E_10: array([1., 1., 1.])}
        for k in illuminants_:
            assert k in illuminants
            np.testing.assert_array_almost_equal(illuminants_[k], illuminants[k])

if __name__ == '__main__':
    unittest.main()
