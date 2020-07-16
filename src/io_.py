import numpy as np

class IO:
    '''
    io: illuminant & observer;
    see notes of api.py for supported list for illuminant and observer; 
    '''
    def __init__(self, illuminant, observer):
        self.illuminant = illuminant
        self.observer = observer
    
    def __eq__(self, other):
        return self.illuminant==other.illuminant and self.observer==other.observer
    
    def __hash__(self):
        return hash(self.illuminant+self.observer)

A_2 = IO("A", "2")
A_10 = IO("A", "10")
D50_2 = IO("D50", "2")
D50_10 = IO("D50", "10")
D55_2 = IO("D55", "2")
D55_10 = IO("D55", "10")
D65_2 = IO("D65", "2")
D65_10 = IO("D65", "10")
D75_2 = IO("D75", "2")
D75_10 = IO("D75", "10")
E_2 = IO("E", "2")
E_10 = IO("E", "10")

def xyY2XYZ(x,y,Y=1):
    '''xyY to XYZ'''
    X = Y*x/y
    Z = Y/y*(1-x-y)
    return np.array([X,Y,Z])
    
'''data from https://en.wikipedia.org/wiki/Standard_illuminant'''
illuminants_xy = \
    {A_2: (0.44757, 0.40745),
    A_10: (0.45117, 0.40594),
    D50_2: (0.34567, 0.35850),
    D50_10: (0.34773, 0.35952),
    D55_2: (0.33242, 0.34743),
    D55_10: (0.33411, 0.34877),
    D65_2: (0.31271, 0.32902),  
    D65_10: (0.31382, 0.33100),
    D75_2: (0.29902, 0.31485),
    D75_10: (0.29968, 0.31740),
    E_2: (1/3, 1/3),
    E_10: (1/3, 1/3)}

def get_illuminant():
    '''get illuminants'''

    illuminants = {}
    for io, (x, y) in illuminants_xy.items():
        illuminants[io] = xyY2XYZ(x, y)

    # data from https://en.wikipedia.org/wiki/Illuminant_D65
    illuminants[D65_2]=np.array([0.95047, 1., 1.08883])
    illuminants[D65_10]=np.array([0.94811, 1., 1.07304])
    return illuminants

# illuminants
illuminants = get_illuminant()

class CAM:
    '''chromatic adaption matrices'''
    CAMs = {}

    Von_Kries = np.array([[ 0.40024,  0.7076 , -0.08081],
                    [-0.2263 ,  1.16532,  0.0457 ],
                    [ 0.     ,  0.     ,  0.91822]])

    Bradford = np.array([[0.8951, 0.2664, -0.1614],
            [-0.7502, 1.7135, 0.0367],
            [0.0389, -0.0685, 1.0296]])

    MAs = {'Identity':(np.eye(3), np.eye(3)), 
        'Von_Kries':(Von_Kries, np.linalg.inv(Von_Kries)),
        'Bradford':(Bradford, np.linalg.inv(Bradford))}

    @classmethod
    def cam(cls, sio, dio, method = 'Bradford'):
        '''get cam'''
        if (sio, dio, method) in cls.CAMs:
            return cls.CAMs[(sio, dio, method)]
        # function from http://www.brucelindbloom.com/index.html?ColorCheckerRGB.html
        XYZws = illuminants[sio]
        XYZWd = illuminants[dio]
        MA, MA_inv = cls.MAs[method]
        M = MA_inv@np.diag((MA@XYZWd)/(MA@XYZws))
        cls.CAMs[(sio, dio, method)] = M
        return M

'''function to get cam'''
cam = CAM.cam