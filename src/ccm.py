from .linearize import *
from scipy.optimize import minimize, fmin
from .color_spaces import *
from .colorchecker import *
from cv2 import cv2

class CCM_3x3:
    def __init__(self, src, colorchecker, saturated_threshold, 
        pre_linear, pre_gamma, pre_deg, post_linear, post_gamma, post_deg, 
        distance, initial, xtol, ftol):
        '''src: rgb, dst: lab'''
        colorchecker = globals()['ColorChecker_' + colorchecker]()
        self.prelinear = globals()['Linear_'+pre_linear](pre_gamma, pre_deg, src, colorchecker, saturated_threshold)
        self.postlinear = globals()['Linear_'+post_linear](post_gamma, post_deg, src, colorchecker, saturated_threshold)
        self.colorchecker = colorchecker
        self.src = src

        self.mask = saturate(src, *saturated_threshold)
        self.src_rgbl = self.prelinear.linearize(self.src)
        self.src_rgb_mask = self.src[self.mask]
        self.dst_rgb_mask = self.colorchecker.rgb[self.mask]
        self.src_rgbl_mask = self.src_rgbl[self.mask]
        self.dst_rgbl_mask = self.colorchecker.rgbl[self.mask]
        self.dst_lab_mask = self.colorchecker.lab[self.mask]

        self.distance = globals()['distance_' + distance]
        self.inital_func = getattr(self, 'initial_' + initial)
        self.xtol = xtol
        self.ftol = ftol
        self.ccm = None
        
        if distance == 'rgb':
            self.calculate_rgb()
        else:
            self.calculate()
        
    def initial_white_balance(self, src_rgbl, dst_rgbl):
        rs, gs, bs = np.sum(src_rgbl, axis = 0)
        rd, gd, bd = np.sum(dst_rgbl, axis = 0)
        return np.array([[rd/rs, 0, 0], [0, gd/gs, 0], [0, 0, bd/bs]]) 

    def initial_least_square(self, src_rgbl, dst_rgbl):
        return np.linalg.lstsq(src_rgbl, dst_rgbl, rcond=None)[0]  

    def loss_rgb(self, ccm):
        ccm = ccm.reshape((-1, 3))
        lab_est = rgbl2rgb(self.src_rgbl_mask@ccm)
        dist = self.distance(lab_est, self.dst_rgb_mask)
        return sum(dist**2)
    
    def calculate_rgb(self):
        if isinstance(self.postlinear, Linear_identity):
            self.ccm = self.initial_least_square(self.src_rgb_mask, self.dst_rgb_mask)
            print('ccm', self.ccm)
            print('error:', self.loss_rgb(self.ccm.reshape((-1))))
            return
        ccm0 = self.inital_func(self.src_rgbl_mask, self.dst_rgbl_mask) 
        ccm0 = ccm0.reshape((-1))
        res = fmin(self.loss_rgb, ccm0, xtol = self.xtol, ftol = self.ftol)
        if res is not None:
            self.ccm = res.reshape((-1,3))
            print('ccm', self.ccm)
            print('error:', self.loss_rgb(res))


    def loss(self, ccm):
        '''
        for any ccm, the loss function is square-sum of color difference between 
        src_rgbl@ccm and dst
        cause one can't use matrix intial value in 
        '''
        ccm = ccm.reshape((-1, 3))
        lab_est = rgbl2lab(self.src_rgbl_mask@ccm)
        dist = self.distance(lab_est, self.dst_lab_mask)
        return sum(dist**2)

    def calculate(self):
        ccm0 = self.inital_func(self.src_rgbl_mask, self.dst_rgbl_mask)
        ccm0 = ccm0.reshape((-1))
        # print('ccm0:', ccm0)
        res = fmin(self.loss, ccm0, xtol = self.xtol, ftol = self.ftol)
        if res is not None:
            self.ccm = res.reshape((-1,3))
            print('ccm:', self.ccm)
            print('error:', self.loss(res))

              
    def infer(self, img):
        if self.ccm is None:
            raise Exception('unsuccess')
        img_lin = self.prelinear.linearize(img)
        img_ccm = img_lin@self.ccm
        img_post = self.postlinear.delinearize(img_ccm)
        return img_post

    def infer_image_256(self, img):
        out = self.infer(img)
        img = np.minimum(np.maximum(np.round(out*255), 0), 255)
        img = img.astype(np.uint8)
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)