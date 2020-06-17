import numpy as np

def saturate(src, low, up):
    return np.all(np.logical_and(src>=low,src<=up), axis = 1)               

def rgb2gray(rgb):
    '''
    In fact, every kind of rgb has a different function to gray.
    because we don't know the exact color space of the input, we use it as an approximation.
    '''
    return rgb@np.array([0.2126, 0.7152, 0.0722])

class IO:
    def __init__(self, illuminant, observer):
        self.illuminant = illuminant
        self.observer = observer
    
    def __eq__(self, other):
        return self.illuminant==other.illuminant and self.observer==other.observer
    
    # def update(self, illuminant = None, observer = None):
    #     if illuminant:
    #         self.illuminant = illuminant
    #     if observer:
    #         self.observer = observer
    
    def __hash__(self):
        return hash(self.illuminant+self.observer)

D65_2 = IO('D65', '2')