from .io_ import *
from .colorspace import *
from .distance import *

class Color:
    def __init__(self, colors, cs):
        '''
        color defined by color_values and color space;
        self.grays is mask of grayscale color;
        self.colored is mask of colored color;
        self._history is storage of historical conversion;
        '''
        self.colors = colors
        self.cs = cs
        self.grays = None
        self.colored = None
        self._history = {}
        
    def to(self, cs, method = 'Bradford', save=True):
        '''
        change to other color space; return Color;
        The conversion process incorporates linear transformations to speed up.
        method is chromatic adapation method;
        when save if True, get data from self._history first;
        '''
        def do_operation(colors, operations):
            M = None
            for op in operations:
                if isinstance(op, np.ndarray):
                    if M is None:
                        M = op
                    else:
                        M = M@op
                else:
                    if M is not None:
                        colors = colors@M
                        M = None
                    colors = op(colors)
            if M is not None:
                colors = colors@M
            return colors

        if cs in self._history:
            return self._history[cs]
        f = self.cs.relate(cs)
        if f:
            return Color(f(self.colors), cs)
        
        operations = [*self.cs.to, *(XYZ(self.cs.io).cam(cs.io, method)), *cs.from_]
        colors = do_operation(self.colors, operations)
        color = Color(colors, cs)
        if save:
            self._history[cs] = color
        return color

    def toGray(self, io, method = 'Bradford', save=True):
        '''self.cs -> gray'''
        return self.to(XYZ(io), method, save).colors[...,1]

    def toLuminant(self, io, method = 'Bradford', save=True):
        '''self.cs -> L*'''
        return self.to(Lab(io), method, save).colors[...,0]

    def get_gray(self, JDN=2):
        '''calculate gray mask'''
        if self.grays is not None:
            return
        color = self.to(Lab_D65_2).colors
        L = color[..., 0]
        a, b = np.zeros(L.shape), np.zeros(L.shape)
        gray = np.stack([L, a, b], axis=-1)
        dis = distance_de00(color, gray)
        # print(dis)
        self.grays = (dis<JDN)
        self.colored = ~self.grays
    
    def diff(self, other, method='de00', io = None, DEBUG = False):
        '''return distance between self and other'''
        if not io: 
            io=self.cs.io
        if method in ['de00', 'de94', 'de76', 'cmc']:
            if DEBUG:
                print('to_lab: ', self.to(Lab(io)).colors)
                print('other_lab: ',other.to(Lab(io)).colors)
            return globals()['distance_'+method](self.to(Lab(io)).colors, other.to(Lab(io)).colors)
        elif method in ['rgb']:
            return globals()['distance_'+method](self.to(self.cs.nl).colors, other.to(self.cs.nl).colors)
        elif method in ['rgbl']:
            return globals()['distance_'+method](self.to(self.cs.l).colors, other.to(self.cs.l).colors)

    def __getitem__(self, mask):
        '''return masked color'''
        return Color(self.colors[mask],self.cs)



'''
Data is from https://www.imatest.com/wp-content/uploads/2011/11/Lab-data-Iluminate-D65-D50-spectro.xls
see Miscellaneous.md for details.
'''
ColorChecker2005_Lab_D50_2 = np.array([[37.986, 13.555, 14.059],
        [65.711, 18.13, 17.81],
        [49.927, -4.88, -21.925],
        [43.139, -13.095, 21.905],
        [55.112, 8.844, -25.399],
        [70.719, -33.397, -0.199],
        [62.661, 36.067, 57.096],
        [40.02, 10.41, -45.964],
        [51.124, 48.239, 16.248],
        [30.325, 22.976, -21.587],
        [72.532, -23.709, 57.255],
        [71.941, 19.363, 67.857],
        [28.778, 14.179, -50.297],
        [55.261, -38.342, 31.37],
        [42.101, 53.378, 28.19],
        [81.733, 4.039, 79.819],
        [51.935, 49.986, -14.574],
        [51.038, -28.631, -28.638],
        [96.539, -0.425, 1.186],
        [81.257, -0.638, -0.335],
        [66.766, -0.734, -0.504],
        [50.867, -0.153, -0.27],
        [35.656, -0.421, -1.231],
        [20.461, -0.079, -0.973]])

ColorChecker2005_Lab_D65_2 = np.array([[37.542, 12.018, 13.33],
        [65.2, 14.821, 17.545],
        [50.366, -1.573, -21.431],
        [43.125, -14.63, 22.12],
        [55.343, 11.449, -25.289],
        [71.36, -32.718, 1.636],
        [61.365, 32.885, 55.155],
        [40.712, 16.908, -45.085],
        [49.86, 45.934, 13.876],
        [30.15, 24.915, -22.606],
        [72.438, -27.464, 58.469],
        [70.916, 15.583, 66.543],
        [29.624, 21.425, -49.031],
        [55.643, -40.76, 33.274],
        [40.554, 49.972, 25.46],
        [80.982, -1.037, 80.03],
        [51.006, 49.876, -16.93],
        [52.121, -24.61, -26.176],
        [96.536, -0.694, 1.354],
        [81.274, -0.61, -0.24],
        [66.787, -0.647, -0.429],
        [50.872, -0.059, -0.247],
        [35.68, -0.22, -1.205],
        [20.475, 0.049, -0.972]])

'''Macbeth ColorChecker with 2deg D50'''
Macbeth_D50_2 = Color(ColorChecker2005_Lab_D50_2, Lab_D50_2)

'''Macbeth ColorChecker with 2deg D65'''
Macbeth_D65_2 = Color(ColorChecker2005_Lab_D65_2, Lab_D65_2)

