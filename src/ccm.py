from .linearize import *
from scipy.optimize import minimize, fmin
from .color_spaces import *
from .colorchecker import *
from cv2 import cv2


class CCM_3x3:
    def __init__(self, src, dst, dst_colorspace, dst_illuminant, dst_observer, 
        dst_whites , colorchecker, saturated_threshold, colorspace, linear, gamma, deg, 
        distance, dist_illuminant, dist_observer, weights_list, weights_coeff, weight_color,
        initial_method, xtol, ftol):
        # src
        self.src = src
        # dst
        self.cs = globals()[colorspace]
        if dst:
            cc = ColorChecker(dst, dst_colorspace, dst_illuminant, dst_observer, dst_whites)
        else:
            cc = globals()['ColorChecker_' + colorchecker]()
        self.colorchecker = ColorCheckerMetric(cc, self.cs, dist_illuminant, dist_observer)

        # linear method
        self.linear = globals()['Linear_'+linear](gamma, deg, src, self.colorchecker, saturated_threshold)
        self.weights = None
        # weight_mask = [True, ...]
        
        if weights_list:
            self.weights = weights_list
        elif weights_coeff!=0:
            self.weights = np.power(self.colorchecker.lab[..., 0], weights_coeff)
        
        weight_mask = None
        if weight_color:
            weight_mask = np.ones(dst.shape, dtype=False)
            weight_mask[self.colorchecker.cc.whites] = False


        # drop the saturated value, the _mask means the drop is done
        # we want to get 
        # if dist == 'rgb':
        #    src.rgbl, dst.rgb
        # elif dist == 'rgbl':
        #    src.rgbl, dst.rgbl
        # else:
        #    src.rgbl, dst.lab
        saturate_mask = saturate(src, *saturated_threshold)
        self.mask = saturate_mask & weight_mask
        self.src_rgbl = self.linear.linearize(self.src)
        self.src_rgb_mask = self.src[self.mask]
        self.dst_rgb_mask = self.colorchecker.rgb[self.mask]
        self.src_rgbl_mask = self.src_rgbl[self.mask]
        self.dst_rgbl_mask = self.colorchecker.rgbl[self.mask]
        self.dst_lab_mask = self.colorchecker.lab[self.mask]
        self.weights_mask = self.weights[self.mask]
        self.weights_mask = self.weights_mask/np.sum(self.weights_mask)

        # the nonlinear optimization options:
        # 1. distance function
        self.distance = globals()['distance_' + distance]
        # 2. initial function
        self.inital_func = getattr(self, 'initial_' + initial_method)
        # 3. xtol and ftol
        self.xtol = xtol
        self.ftol = ftol
        # the output
        self.ccm = None
        
        # distance function may affect the loss function and the calculate function
        # 'rgbl distance?'
        if distance == 'rgb':
            self.calculate_rgb()
        elif distance == 'rgbl':
            self.calculate_rgbl()
        else:
            self.calculate()
        
    def initial_white_balance(self, src_rgbl, dst_rgbl):
        '''calculate nonlinear-optimization initial value by white balance:
        res = diag(mean(s_r)/mean(d_r), mean(s_g)/mean(d_g), mean(s_b)/mean(d_b))
        https://www.imatest.com/docs/colormatrix/
        '''
        rs, gs, bs = np.sum(src_rgbl, axis = 0)
        rd, gd, bd = np.sum(dst_rgbl, axis = 0)
        return np.array([[rd/rs, 0, 0], [0, gd/gs, 0], [0, 0, bd/bs]]) 

    def initial_least_square(self, src_rgbl, dst_rgbl):
        '''calculate nonlinear-optimization initial value by least square:
        res = np.linalg.lstsq(src_rgbl, dst_rgbl)
        '''        
        return np.linalg.lstsq(src_rgbl, dst_rgbl, rcond=None)[0]  

    def loss_rgb(self, ccm):
        '''loss function if distance function is rgb
        it is square-sum of color difference between src_rgbl@ccm and dst
        '''
        ccm = ccm.reshape((-1, 3))
        lab_est = self.cs.rgbl2rgb(self.src_rgbl_mask@ccm)
        dist = self.distance(lab_est, self.dst_rgb_mask)
        dist = self.weights_mask*dist
        return sum(dist**2)
    
    def calculate_rgbl(self):
        self.ccm = self.initial_least_square(self.src_rgb_mask, self.dst_rgb_mask)
        return

    def calculate_rgb(self):
        '''calculate ccm if distance function is rgb'''
        # if isinstance(self.linear, Linear_identity):
        #     self.ccm = self.initial_least_square(self.src_rgb_mask, self.dst_rgb_mask)
        #     print('ccm', self.ccm)
        #     print('error:', self.loss_rgb(self.ccm.reshape((-1))))
        #     return
        ccm0 = self.inital_func(self.src_rgbl_mask, self.dst_rgbl_mask) 
        ccm0 = ccm0.reshape((-1))
        res = fmin(self.loss_rgb, ccm0, xtol = self.xtol, ftol = self.ftol)
        if res is not None:
            self.ccm = res.reshape((-1,3))
            print('ccm', self.ccm)
            print('error:', self.loss_rgb(res))

    def loss(self, ccm):
        '''
        loss function of de76 de94 and de00
        it is square-sum of color difference between src_rgbl@ccm and dst
        '''
        ccm = ccm.reshape((-1, 3))
        lab_est = self.cs.rgbl2lab(self.src_rgbl_mask@ccm)
        dist = self.distance(lab_est, self.dst_lab_mask)
        dist = self.weights_mask*dist
        return sum(dist**2)

    def calculate(self):
        '''calculate ccm if distance function is de76 de94 and de00'''
        ccm0 = self.inital_func(self.src_rgbl_mask, self.dst_rgbl_mask)
        ccm0 = ccm0.reshape((-1))
        res = fmin(self.loss, ccm0, xtol = self.xtol, ftol = self.ftol)
        if res is not None:
            self.ccm = res.reshape((-1,3))
            print('ccm:', self.ccm)
            print('error:', self.loss(res))

              
    def infer(self, img, L=False):
        '''infer using calculated ccm'''
        if self.ccm is None:
            raise Exception('unsuccess')
        img_lin = self.linear.linearize(img)
        img_ccm = img_lin@self.ccm
        if L:
            return img_ccm
        return self.cs.rgbl2rgb(img_ccm)
        # img_post = self.sc.delinearize(img_ccm)
        # return img_post

    def infer_image_256(self, img, L=False):
        '''infer image and output as an BGR image with uint8 type'''
        out = self.infer(img, L)
        img = np.minimum(np.maximum(np.round(out*255), 0), 255)
        img = img.astype(np.uint8)
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

class CCM_4x3:
    def __init__(self, src, dst, dst_colorspace, dst_illuminant, dst_observer, 
        dst_whites , colorchecker, saturated_threshold, colorspace, linear, gamma, deg, 
        distance, dist_illuminant, dist_observer, weights_list, weights_coeff, weight_color,
        initial_method, xtol, ftol):
        # src
        self.src = src
        # dst
        self.cs = globals()[colorspace]
        if dst:
            cc = ColorChecker(dst, dst_colorspace, dst_illuminant, dst_observer, dst_whites)
        else:
            cc = globals()['ColorChecker_' + colorchecker]()
        self.colorchecker = ColorCheckerMetric(cc, self.cs, dist_illuminant, dist_observer)

        # linear method
        self.linear = globals()['Linear_'+linear](gamma, deg, src, self.colorchecker, saturated_threshold)
        self.weights = None
        # weight_mask = [True, ...]
        
        if weights_list:
            self.weights = weights_list
        elif weights_coeff!=0:
            self.weights = np.power(self.colorchecker.lab[..., 0], weights_coeff)
        
        weight_mask = None
        if weight_color:
            weight_mask = np.ones(dst.shape, dtype=False)
            weight_mask[self.colorchecker.cc.whites] = False


        # drop the saturated value, the _mask means the drop is done
        # we want to get 
        # if dist == 'rgb':
        #    src.rgbl, dst.rgb
        # elif dist == 'rgbl':
        #    src.rgbl, dst.rgbl
        # else:
        #    src.rgbl, dst.lab
        saturate_mask = saturate(src, *saturated_threshold)
        self.mask = saturate_mask & weight_mask
        self.src_rgbl = self.linear.linearize(self.src)
        self.src_rgb_mask = self.src[self.mask]
        self.dst_rgb_mask = self.colorchecker.rgb[self.mask]
        self.src_rgbl_mask = self.src_rgbl[self.mask]
        self.dst_rgbl_mask = self.colorchecker.rgbl[self.mask]
        self.dst_lab_mask = self.colorchecker.lab[self.mask]
        self.weights_mask = self.weights[self.mask]
        self.weights_mask = self.weights_mask/np.sum(self.weights_mask)

        # the nonlinear optimization options:
        # 1. distance function
        self.distance = globals()['distance_' + distance]
        # 2. initial function
        self.inital_func = getattr(self, 'initial_' + initial_method)
        # 3. xtol and ftol
        self.xtol = xtol
        self.ftol = ftol
        # the output
        self.ccm = None
        
        # distance function may affect the loss function and the calculate function
        # 'rgbl distance?'
        if distance == 'rgb':
            self.calculate_rgb()
        elif distance == 'rgbl':
            self.calculate_rgbl()
        else:
            self.calculate()
        
    def initial_white_balance(self, src_rgbl, dst_rgbl):
        '''calculate nonlinear-optimization initial value by white balance:
        res = diag(mean(s_r)/mean(d_r), mean(s_g)/mean(d_g), mean(s_b)/mean(d_b))
        https://www.imatest.com/docs/colormatrix/
        '''
        rs, gs, bs = np.sum(src_rgbl, axis = 0)
        rd, gd, bd = np.sum(dst_rgbl, axis = 0)
        return np.array([[rd/rs, 0, 0], [0, gd/gs, 0], [0, 0, bd/bs]]) 

    def initial_least_square(self, src_rgbl, dst_rgbl):
        '''calculate nonlinear-optimization initial value by least square:
        res = np.linalg.lstsq(src_rgbl, dst_rgbl)
        '''        
        return np.linalg.lstsq(src_rgbl, dst_rgbl, rcond=None)[0]  

    def loss_rgb(self, ccm):
        '''loss function if distance function is rgb
        it is square-sum of color difference between src_rgbl@ccm and dst
        '''
        ccm = ccm.reshape((-1, 3))
        lab_est = self.cs.rgbl2rgb(self.src_rgbl_mask@ccm)
        dist = self.distance(lab_est, self.dst_rgb_mask)
        dist = self.weights_mask*dist
        return sum(dist**2)
    
    def calculate_rgbl(self):
        self.ccm = self.initial_least_square(self.src_rgb_mask, self.dst_rgb_mask)
        return

    def calculate_rgb(self):
        '''calculate ccm if distance function is rgb'''
        # if isinstance(self.linear, Linear_identity):
        #     self.ccm = self.initial_least_square(self.src_rgb_mask, self.dst_rgb_mask)
        #     print('ccm', self.ccm)
        #     print('error:', self.loss_rgb(self.ccm.reshape((-1))))
        #     return
        ccm0 = self.inital_func(self.src_rgbl_mask, self.dst_rgbl_mask) 
        ccm0 = ccm0.reshape((-1))
        res = fmin(self.loss_rgb, ccm0, xtol = self.xtol, ftol = self.ftol)
        if res is not None:
            self.ccm = res.reshape((-1,3))
            print('ccm', self.ccm)
            print('error:', self.loss_rgb(res))

    def loss(self, ccm):
        '''
        loss function of de76 de94 and de00
        it is square-sum of color difference between src_rgbl@ccm and dst
        '''
        ccm = ccm.reshape((-1, 3))
        lab_est = self.cs.rgbl2lab(self.src_rgbl_mask@ccm)
        dist = self.distance(lab_est, self.dst_lab_mask)
        dist = self.weights_mask*dist
        return sum(dist**2)

    def calculate(self):
        '''calculate ccm if distance function is de76 de94 and de00'''
        ccm0 = self.inital_func(self.src_rgbl_mask, self.dst_rgbl_mask)
        ccm0 = ccm0.reshape((-1))
        res = fmin(self.loss, ccm0, xtol = self.xtol, ftol = self.ftol)
        if res is not None:
            self.ccm = res.reshape((-1,3))
            print('ccm:', self.ccm)
            print('error:', self.loss(res))

              
    def infer(self, img, L=False):
        '''infer using calculated ccm'''
        if self.ccm is None:
            raise Exception('unsuccess')
        img_lin = self.linear.linearize(img)
        img_ccm = img_lin@self.ccm
        if L:
            return img_ccm
        return self.cs.rgbl2rgb(img_ccm)
        # img_post = self.sc.delinearize(img_ccm)
        # return img_post

    def infer_image_256(self, img, L=False):
        '''infer image and output as an BGR image with uint8 type'''
        out = self.infer(img, L)
        img = np.minimum(np.maximum(np.round(out*255), 0), 255)
        img = img.astype(np.uint8)
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)