from .linearize import *
from scipy.optimize import minimize, fmin
from .colorspace import *
from color import *
from .colorchecker import *
from .utils import *
from .distance import *
from cv2 import cv2
import numpy as np

class CCM_3x3:
    def __init__(self, src,
        dst,
        ccm_shape, 
        colorspace,
        distance, 
        saturated_threshold, 
        linear, gamma, deg, 
        weights_list, weights_coeff,
        initial_method, xtol, ftol):
        '''
        After being called, the method produce a CCM_3x3 instance (a color correction 
        model in fact) for inference.

        The meanings of the arguments have been detailed in api.py;
        '''

        # detected colors
        self.src = src
        
        # the absolute RGB color space that detected colors convert to
        self.dst = dst

        self.cs = colorspace
        # self.dio = IO(dist_illuminant, dist_observer)
        # self.cs = globals()[colorspace]()

        # see notes of colorchecker.py for difference between 
        # ColorChecker and ColorCheckerMetric
        # if dst:
        #     cc = ColorChecker(dst, dst_colorspace, IO(dst_illuminant, dst_observer), dst_whites)
        # else:
        #     cc = globals()['colorchecker_' + colorchecker]
        # self.cc = ColorCheckerMetric(dst, colorspace)

        # linear method
        saturate_mask = saturate(src, *saturated_threshold)

        self.linear = globals()['Linear_'+linear](gamma, deg, src, self.dst, saturate_mask)
        
        self.cal_weights_masks(weights_list, weights_coeff, saturate_mask)

        # prepare the data; _masked means colors having been filtered
        # self.src_rgbl = self.linear.linearize(self.src)
        # self.src_masked = self.src[self.mask]
        self.src_rgbl = self.linear.linearize(self.src[self.mask]) 
        
        # self.dst_rgb_masked = self.cc.rgb[self.mask]
        # self.dst_rgbl_masked = self.cc.rgbl[self.mask]
        # self.dst_lab_masked = self.cc.lab[self.mask]
        self.dst = self.dst[self.mask]
        self.dst_rgbl = self.dst.to(self.cs.l)


        # the nonlinear optimization options:
        # 1. distance function
        # self.distance = globals()['distance_' + distance]
        self.distance = distance
        # 2. initial function
        self.inital_func = getattr(self, 'initial_' + initial_method)
        # 3. xtol and ftol
        self.xtol = xtol
        self.ftol = ftol
        # 4. the output
        self.ccm = None

        # empty for CCM_3x3, not empty for CCM_4x3
        # make __init__ method can also be used by CCM_4x3 class
        self.prepare()

        # distance function may affect the loss function and the fitting function
        if distance == 'rgbl':
            self.initial_least_square(fit=True)
        else:
            self.fitting()
        
    def cal_weights_masks(self, weights_list, weights_coeff, saturate_mask):
        # weights    
        self.weights = None 
        if weights_list:
            self.weights = weights_list
        elif weights_coeff!=0:
            self.weights = np.power(self.dst.toLuminant(self.cs.io), weights_coeff)
        
        # masks
        weight_mask = np.ones(self.src.shape[0], dtype=bool)  
        if self.weights is not None:
            weight_mask = self.weights>0
        self.mask = saturate_mask & weight_mask

        # weights' mask
        if self.weights is not None:
            weights_masked = self.weights[self.mask]
            self.weights = weights_masked/np.mean(weights_masked)
            # self.weights = (self.weights**0.5)[:, np.newaxis]
        self.masked_len = np.sum(self.mask)        

    def prepare(self):
        '''make no change for CCM_3x3 class'''
        pass
    
    def initial_white_balance(self):
        '''
        fitting nonlinear-optimization initial value by white balance:
        res = diag(mean(s_r)/mean(d_r), mean(s_g)/mean(d_g), mean(s_b)/mean(d_b))
        see CCM.pdf for details;
        '''
        rs, gs, bs = np.sum(self.src_rgbl, axis = 0)
        rd, gd, bd = np.sum(self.dst_rgbl, axis = 0)
        return np.array([[rd/rs, 0, 0], [0, gd/gs, 0], [0, 0, bd/bs]]) 

    def initial_least_square(self, fit=False):
        '''
        fitting nonlinear-optimization initial value by least square:
        res = np.linalg.lstsq(src_rgbl, dst_rgbl)
        see CCM.pdf for details;
        '''        
        '''fitting ccm if distance function is rgbl'''
        if self.weights is None: 
            ccm, r, *_ = np.linalg.lstsq(self.src_rgbl, self.dst_rgbl)
        else:
            w = (self.weights**0.5)[:, np.newaxis]
            ccm, r, *_  = np.linalg.lstsq(w*self.src_rgbl, w*self.dst_rgbl)
        if not fit:
            return ccm
        self.ccm = ccm
        self.error = np.sum(r) 

    def loss(self, ccm):
        '''
        loss function of de76 de94 and de00
        it is square-sum of color difference between src_rgbl@ccm and dst
        '''
        
        ccm = ccm.reshape((-1, 3))
        dist = Color(self.src_rgbl@ccm, self.cs).diff(self.dst, self.distance)
        dist = np.power(dist, 2)
        if self.weights:
            dist = self.weights*dist
        return np.sum(dist)

    def fitting(self):
        '''fitting ccm if distance function is associated with CIE Lab color space'''
        ccm0 = self.inital_func()
        ccm0 = ccm0.reshape((-1))
        res = fmin(self.loss, ccm0, xtol = self.xtol, ftol = self.ftol)
        if res is not None:
            self.ccm = res.reshape((-1,3))
            self.error = (self.loss(res)/self.masked_len)**0.5
            print('ccm:', self.ccm)
            print('error:', self.error)         




    # def fitting_rgbl(self):
    #     '''fitting ccm if distance function is rgbl'''
    #     if self.weights is None: 
    #         self.ccm, r, *_ = np.linalg.lstsq(self.src_rgbl_masked, self.dst_rgbl_masked)
    #     else:
    #         w = np.diag(np.power(self.weights_masked_norm, 0.5))
    #         self.ccm, r, *_  = np.linalg.lstsq(w@self.src_rgbl_masked, w@self.dst_rgbl_masked)
    #     self.error = np.sum(r)

   

    # def loss_rgb(self, ccm):
    #     '''
    #     loss function if distance function is rgb
    #     it is square-sum of color difference between src_rgbl@ccm and dst
    #     '''
    #     ccm = ccm.reshape((-1, 3))
    #     return self.distances(self.cs.rgbl2rgb(self.src_rgbl_masked@ccm), self.dst_rgb_masked)


    # def fitting_rgb(self):
    #     '''fitting ccm if distance function is rgb'''
    #     ccm0 = self.inital_func(self.src_rgbl_masked, self.dst_rgbl_masked) 
    #     ccm0 = ccm0.reshape((-1))
    #     res = fmin(self.loss_rgb, ccm0, xtol = self.xtol, ftol = self.ftol)
    #     if res is not None:
    #         self.ccm = res.reshape((-1,3))
    #         self.error = (self.loss_rgb(res)/self.masked_len)**0.5
    #         print('ccm', self.ccm)
    #         print('error:', self.error)

   



    # def loss(self, ccm):
    #     '''
    #     loss function of de76 de94 and de00
    #     it is square-sum of color difference between src_rgbl@ccm and dst
    #     '''
    #     ccm = ccm.reshape((-1, 3))
    #     # Color(self.src_rgbl_masked@ccm, cs).diff(self.dst_lab_masked)
    #     return self.distances(Color(self.src_rgbl_masked@ccm, cs).diff(self.dst_lab_masked))

    # def fitting(self):
    #     '''fitting ccm if distance function is associated with CIE Lab color space'''
    #     ccm0 = self.inital_func(self.src_rgbl_masked, self.dst_rgbl_masked)
    #     ccm0 = ccm0.reshape((-1))
    #     res = fmin(self.loss, ccm0, xtol = self.xtol, ftol = self.ftol)
    #     if res is not None:
    #         self.ccm = res.reshape((-1,3))
    #         self.error = (self.loss(res)/self.masked_len)**0.5
    #         print('ccm:', self.ccm)
    #         print('error:', self.error)

    # def value(self, number = 10000):
    #     '''
    #     evaluate the model by residual error, overall saturation and coverage volume;
    #     see Algorithm.py for details;

    #     NOTICE: The method is not yet complete.
    #     '''
        # print('error:', self.error)
        # 饱和度
        # rand = np.random.random((number, 3))
        # mask = saturate(self.infer(rand), 0, 1)
        # self.sat = np.sum(mask)/number
        # print('sat:', self.sat)
        # # 分布度
        # rgbl = self.cs.rgb2rgbl(rand)
        # mask = saturate(rgbl@np.linalg.inv(self.ccm), 0, 1)
        # self.dist = np.sum(mask)/number
        # print('dist:', self.dist)

    def infer(self, img, L=False):
        '''infer using fittingd ccm'''
        if self.ccm is None:
            raise Exception('No CCM values!')
        img_lin = self.linear.linearize(img)
        img_ccm = img_lin@self.ccm
        if L:
            return img_ccm
        return self.cs.rgbl2rgb(img_ccm)

    def infer_image(self, imgfile, L=False, inp_size=255, out_size=255, out_dtype = np.uint8):
        '''
        infer image and output as an BGR image with uint8 type
        mainly for test or debug!
        '''
        img = cv2.imread(imgfile)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)/inp_size
        out = self.infer(img, L)
        img = np.minimum(np.maximum(np.round(out*out_size), 0), out_size)
        img = img.astype(out_dtype)
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

class CCM_4x3(CCM_3x3):
    def prepare(self):
        '''see CCM.pdf for details'''
        self.src_rgbl_masked = self.add_column(self.src_rgbl_masked)
    
    @staticmethod
    def add_column(arr):
        '''convert matrix A to [A, 1]'''
        return np.c_[arr, np.ones((*arr.shape[:-1], 1))]

    def initial_white_balance(self, src_rgbl, dst_rgbl):
        '''
        fitting nonlinear-optimization initial value by white balance:
        see CCM.pdf for details;
        '''
        rs, gs, bs = np.sum(src_rgbl, axis = 0)
        rd, gd, bd = np.sum(dst_rgbl, axis = 0)
        return np.array([[rd/rs, 0, 0], [0, gd/gs, 0], [0, 0, bd/bs]]) 

    def infer(self, img, L=False):
        '''infer using fittingd ccm'''
        if self.ccm is None:
            raise Exception('No CCM values!')
        img_lin = self.linear.linearize(img)
        img_ccm = self.add_column(img_lin)@self.ccm
        if L:
            return img_ccm
        return self.cs.rgbl2rgb(img_ccm)

    def value(self, number = 10000):
        '''
        evaluate the model by residual error, overall saturation and coverage volume;
        see Algorithm.py for details;

        NOTICE: The method is not yet complete.
        '''
        # print('error:', self.error)
        # # 饱和度
        # rand = np.random.random((number, 3))
        # mask = saturate(self.infer(rand), 0, 1)
        # self.sat = np.sum(mask)/number
        # print('sat:', self.sat)
        # # 分布度
        # rgbl = self.cs.rgb2rgbl(rand)
        # up, down = self.ccm[:3, :], self.ccm[3:, :]
        # mask = saturate((rgbl-np.ones((number, 1))@down)@np.linalg.inv(up), 0, 1)
        # self.dist = np.sum(mask)/number
        # print('dist:', self.dist)