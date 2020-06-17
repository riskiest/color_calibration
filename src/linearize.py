import numpy as np
from .utils import *
from .colorspace import gamma_correction

class Linear:
    def __init__(self, *args):
        pass

    def calc(self):
        pass

    def linearize(self, inp):
        return inp

class Linear_identity(Linear):
    pass


class Linear_gamma(Linear):
    def __init__(self, gamma, *_):
        self.gamma = gamma

    def linearize(self, inp):
        return gamma_correction(inp, self.gamma)

    # def delinearize(self, inp):
    #     return gamma_correction(inp, 1/self.gamma)

# class Linear_srgb(Linear):
#     def linearize(self, inp):
#         return rgb2rgbl(inp)

#     def delinearize(self, inp):
#         return rgbl2rgb(inp)

class Linear_color_polyfit(Linear):
    def __init__(self, _, deg, src, colorchecker, saturated_threshold):
        self.deg = deg
        mask = saturate(src, *saturated_threshold)
        self.src, self.dst = src[mask], colorchecker.rgbl[mask]

    def calc(self):
        rs, gs, bs = self.src[..., 0], self.src[..., 1], self.src[..., 2]
        rd, gd, bd = self.dst[..., 0], self.dst[..., 1], self.dst[..., 2]

        pr, *_ = np.polyfit(rs, rd, self.deg, full=True)
        pg, *_ = np.polyfit(gs, gd, self.deg, full=True)
        pb, *_ = np.polyfit(bs, bd, self.deg, full=True)

        self.pr, self.pg, self.pb = np.poly1d(pr), np.poly1d(pg), np.poly1d(pb)

    def linearize(self, inp):
        r, g, b = inp[..., 0], inp[..., 1], inp[..., 2]
        return np.stack([self.pr(r), self.pg(g), self.pb(b)], axis=-1)


class Linear_gray_polyfit(Linear):
    def __init__(self, _, deg, src, colorchecker, saturated_threshold):
        self.deg = deg
        mask = saturate(src[18:,:], *saturated_threshold)
        # white_mask = 
        self.src, self.dst = rgb2gray(src[18:,:][mask]), colorchecker.grayl[18:][mask]
        self.calc()

    def calc(self):
        p, *_ = np.polyfit(self.src, self.dst, self.deg, full=True)
        self.p = np.poly1d(p)
        print('p', self.p)

    def linearize(self, inp):
        return self.p(inp)

    # def delinearize(self, inp):
    #     raise Exception("polyfit can't delinearize!")
