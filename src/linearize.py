import numpy as np
from math import log, exp
from .utils import *

class Linear:
    def __init__(self, *args):
        pass

    def calc(self):
        pass

    def linearize(self, inp):
        return inp
    
    def value(self):
        '''value函数对线性化进行评价，主要从三个角度：
        1. 单调性，如果函数不单调，则提示；
        2. 饱和度，返回函数有多少输入被截断了（即输入属于[0,1]，输出在[0,1]外）；
        3. 分布度，函数返回值在[0,1]区间的长度；
        '''
        pass

class Linear_identity(Linear):
    pass


class Linear_gamma(Linear):
    def __init__(self, gamma, *_):
        self.gamma = gamma

    def linearize(self, inp):
        return gamma_correction(inp, self.gamma)


class Linear_color_polyfit(Linear):
    def __init__(self, _, deg, src, colorchecker, saturated_threshold):
        self.deg = deg
        mask = saturate(src, *saturated_threshold)
        self.src, self.dst = src[mask], colorchecker.rgbl[mask]
        self.calc()

    def calc(self):
        '''
        虽然polyfit并非单调增函数也能使得程序进行下去，但一个更好的方式是限制回归函数单调递增
        但由于现在并没有趁手的程序来实现，这个将期望在以后的版本进行改进
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
        '''
        将在以后的版本上添加
        '''
        pass


class Linear_color_logpolyfit(Linear):
    def __init__(self, _, deg, src, colorchecker, saturated_threshold):
        self.deg = deg
        mask = saturate(src, *saturated_threshold)
        self.src, self.dst = src[mask], colorchecker.rgbl[mask]
        self.calc()

    def calc(self):
        rs, gs, bs = self.src[..., 0], self.src[..., 1], self.src[..., 2]
        rd, gd, bd = self.dst[..., 0], self.dst[..., 1], self.dst[..., 2]

        # 如果s和d值有为<=0，则该处的点不参与polyfit
        def _polyfit(s, d, deg):
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
        '''
        将在以后的版本上添加
        '''
        pass

class Linear_gray_polyfit(Linear):
    def __init__(self, _, deg, src, colorchecker, saturated_threshold):
        self.deg = deg
        mask = saturate(src, *saturated_threshold) & colorchecker.white_mask
        '''理论上由于输入的色彩空间未定，使用rgb2gray即sRGB的灰度公式并不准确，
        此外，rgb2gray也仅是sRGB的近似灰度公式；
        考虑到本身是一个线性化的近似，因此这里直接使用rgb2gray作为灰度公式的近似
        '''
        self.src, self.dst = rgb2gray(src[mask]), colorchecker.grayl[mask]
        self.calc()

    def calc(self):
        p = np.polyfit(self.src, self.dst, self.deg)
        self.p = np.poly1d(p)
        print('p', self.p)

    def linearize(self, inp):
        return self.p(inp)

class Linear_gray_logpolyfit(Linear):
    def __init__(self, _, deg, src, colorchecker, saturated_threshold):
        self.deg = deg
        mask = saturate(src, *saturated_threshold) & colorchecker.white_mask
        '''理论上由于输入的色彩空间未定，使用rgb2gray即sRGB的灰度公式并不准确，
        此外，rgb2gray也仅是sRGB的近似灰度公式；
        考虑到本身是一个线性化的近似，因此这里直接使用rgb2gray作为灰度公式的近似
        '''
        self.src, self.dst = rgb2gray(src[mask]), colorchecker.grayl[mask]
        self.calc()

    def calc(self):
        # 如果s和d值有为<=0，则该处的点不参与polyfit
        def _polyfit(s, d, deg):
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