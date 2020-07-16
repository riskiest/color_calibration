import numpy as np
from math import log, exp
from .utils import *

class Linear:
    '''linearization base'''
    def __init__(self, *args):
        '''get args'''
        pass

    def calc(self):
        '''calculate parameters'''
        pass

    def linearize(self, inp):
        '''inference'''
        return inp
    
    def value(self):
        '''evaluate linearization model'''
        pass

class Linear_identity(Linear):
    '''make no change'''
    pass

class Linear_gamma(Linear):
    '''
    gamma correction;
    see Linearization.py for details;
    '''
    def __init__(self, gamma, *_):
        self.gamma = gamma

    def linearize(self, inp):
        return gamma_correction(inp, self.gamma)

class Linear_color_polyfit(Linear):
    '''
    polynomial fitting channels respectively;
    see Linearization.py for details;
    '''    
    def __init__(self, _, deg, src, colorchecker, saturated_threshold):
        self.deg = deg
        mask = saturate(src, *saturated_threshold)
        self.src, self.dst = src[mask], colorchecker.rgbl[mask]
        self.calc()

    def calc(self):
        '''
        monotonically increase is not guaranteed;
        see Linearization.py for more details;
        '''
        rs, gs, bs = self.src[..., 0], self.src[..., 1], self.src[..., 2]
        rd, gd, bd = self.dst[..., 0], self.dst[..., 1], self.dst[..., 2]

        pr = np.polyfit(rs, rd, self.deg)
        pg = np.polyfit(gs, gd, self.deg)
        pb = np.polyfit(bs, bd, self.deg)

        self.pr, self.pg, self.pb = np.poly1d(pr), np.poly1d(pg), np.poly1d(pb)

    def linearize(self, inp):
        r, g, b = inp[..., 0], inp[..., 1], inp[..., 2]
        return np.stack([self.pr(r), self.pg(g), self.pb(b)], axis=-1)

    def value(self):
        '''NOTICE: The method is not yet complete.'''
        pass


class Linear_color_logpolyfit(Linear):
    '''
    logarithmic polynomial fitting channels respectively;
    see Linearization.py for details;
    '''      
    def __init__(self, _, deg, src, colorchecker, saturated_threshold):
        self.deg = deg
        mask = saturate(src, *saturated_threshold)
        self.src, self.dst = src[mask], colorchecker.rgbl[mask]
        self.calc()

    def calc(self):
        '''
        monotonically increase is not guaranteed;
        see Linearization.py for more details;
        '''        
        rs, gs, bs = self.src[..., 0], self.src[..., 1], self.src[..., 2]
        rd, gd, bd = self.dst[..., 0], self.dst[..., 1], self.dst[..., 2]

        # values less than or equal to 0 cannot participate in calculation for 
        # features of the logarithmic function
        def _polyfit(s, d, deg):
            '''polyfit for s>0 and d>0'''
            mask = (s>0) & (d>0)
            s = s[mask]
            d = d[mask]
            p = np.polyfit(np.log(s), np.log(d), deg)
            return np.poly1d(p)
        
        self.pr, self.pg, self.pb = _polyfit(rs, rd, self.deg), _polyfit(gs, gd, self.deg), _polyfit(bs, bd, self.deg)


    def linearize(self, inp):
        def _lin(p, x):
            mask = x>0
            y = x.copy()
            y[mask] = np.exp(p(np.log(x[mask])))
            y[~mask] = 0
            return y
        r, g, b = inp[..., 0], inp[..., 1], inp[..., 2]
        return np.stack([_lin(self.pr, r), _lin(self.pg, g), _lin(self.pb, b)], axis=-1)

    def value(self):
        '''NOTICE: The method is not yet complete.'''
        pass

class Linear_gray_polyfit(Linear):
    '''
    grayscale polynomial fitting;
    see Linearization.py for details;
    '''      
    def __init__(self, _, deg, src, colorchecker, saturated_threshold):
        self.deg = deg
        mask = saturate(src, *saturated_threshold) & colorchecker.white_mask

        # the grayscale function is approximate for src is in relative color space;
        # see Linearization.py for more details;
        self.src, self.dst = rgb2gray(src[mask]), colorchecker.grayl[mask]
        self.calc()

    def calc(self):
        '''
        monotonically increase is not guaranteed;
        see Linearization.py for more details;
        '''        
        p = np.polyfit(self.src, self.dst, self.deg)
        self.p = np.poly1d(p)
        print('p', self.p)

    def linearize(self, inp):
        return self.p(inp)

    def value(self):
        '''NOTICE: The method is not yet complete.'''
        pass

class Linear_gray_logpolyfit(Linear):
    '''
    grayscale logarithmic polynomial fitting;
    see Linearization.py for details;
    '''      
    def __init__(self, _, deg, src, colorchecker, saturated_threshold):
        self.deg = deg
        mask = saturate(src, *saturated_threshold) & colorchecker.white_mask
        
        # the grayscale function is approximate for src is in relative color space;
        # see Linearization.py for more details;
        self.src, self.dst = rgb2gray(src[mask]), colorchecker.grayl[mask]
        self.calc()

    def calc(self):
        '''
        monotonically increase is not guaranteed;
        see Linearization.py for more details;
        '''        

        # values less than or equal to 0 cannot participate in calculation for 
        # features of the logarithmic function
        def _polyfit(s, d, deg):
            '''polyfit for s>0 and d>0'''
            mask = (s>0) & (d>0)
            s = s[mask]
            d = d[mask]
            p = np.polyfit(np.log(s), np.log(d), deg)
            return np.poly1d(p)
        
        self.p = _polyfit(self.src, self.dst, self.deg)

    def linearize(self, inp):
        def _lin(p, x):
            mask = x>0
            y = x.copy()
            y[mask] = np.exp(p(np.log(x[mask])))
            y[~mask] = 0
            return y

        return _lin(self.p, inp)

    def value(self):
        '''NOTICE: The method is not yet complete.'''
        pass