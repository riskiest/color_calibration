from .linearize import *
from scipy.optimize import minimize, fmin
from .colorspace import *
from .colorchecker import *
from .utils import *
from .distance import *
from cv2 import cv2

class CCM_3x3:
    def __init__(self, src, dst, dst_colorspace, dst_illuminant, dst_observer, 
        dst_whites, colorchecker, saturated_threshold, colorspace, linear, gamma, deg, 
        distance, dist_illuminant, dist_observer, weights_list, weights_coeff, weight_color,
        initial_method, xtol, ftol):

        # src
        self.src = src
        
        # colorchecker
        dist_io = IO(dist_illuminant, dist_observer)
        self.cs = globals()[colorspace]()
        self.cs.set_default(dist_io)
        # self.cs = globals()[colorspace].set_default(dist_io)
        if dst:
            cc = ColorChecker(dst, dst_colorspace, IO(dst_illuminant, dst_observer), dst_whites)
        else:
            cc = globals()['colorchecker_' + colorchecker]
        self.cc = ColorCheckerMetric(cc, self.cs, dist_io)

        # linear method
        self.linear = globals()['Linear_'+linear](gamma, deg, src, self.cc, saturated_threshold)
        
        self.weights = None        
        if weights_list:
            self.weights = weights_list
        elif weights_coeff!=0:
            '''注意，由于目标函数为sum(weights*d^2),意味着weights_coeff=2时，系数与亮度成正比；
            为1时为与亮度的平方根成正比'''
            self.weights = np.power(self.cc.lab[..., 0], weights_coeff)
        
        weight_mask = np.ones(self.src.shape[0], dtype=bool)
        if weight_color:
            weight_mask = self.cc.color_mask

        # drop the saturated value, the _masked means the drop is done
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
        self.src_rgb_masked = self.src[self.mask]
        self.src_rgbl_masked = self.src_rgbl[self.mask]
        self.dst_rgb_masked = self.cc.rgb[self.mask]
        self.dst_rgbl_masked = self.cc.rgbl[self.mask]
        self.dst_lab_masked = self.cc.lab[self.mask]
        if self.weights is not None:
            self.weights_masked = self.weights[self.mask]
            '''weights归一化不影响结果，但好处在于可以进行横向比较（不同配置的比较）'''
            self.weights_masked_norm = self.weights_masked/np.mean(self.weights_masked)
        self.masked_len = len(self.src_rgb_masked)

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

        self.prepare()

        # distance function may affect the loss function and the calculate function
        # 'rgbl distance'
        if distance == 'rgb':
            self.calculate_rgb()
        elif distance == 'rgbl':
            self.calculate_rgbl()
        else:
            self.calculate()
    
    def prepare(self):
        pass
        
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
        lab_est = self.cs.rgbl2rgb(self.src_rgbl_masked@ccm)
        dist = self.distance(lab_est, self.dst_rgb_masked)
        dist = np.power(dist, 2)
        if self.weights:
            dist = self.weights_masked_norm*dist
        return sum(dist)

    def calculate_rgb(self):
        '''calculate ccm if distance function is rgb'''
        ccm0 = self.inital_func(self.src_rgbl_masked, self.dst_rgbl_masked) 
        ccm0 = ccm0.reshape((-1))
        res = fmin(self.loss_rgb, ccm0, xtol = self.xtol, ftol = self.ftol)
        if res is not None:
            self.ccm = res.reshape((-1,3))
            print('ccm', self.ccm)
            print('error:', (self.loss_rgb(res)/self.masked_len)**0.5)

    def calculate_rgbl(self):
        self.ccm = self.initial_least_square(self.src_rgbl_masked, self.dst_rgbl_masked)

    def loss(self, ccm):
        '''
        loss function of de76 de94 and de00
        it is square-sum of color difference between src_rgbl@ccm and dst
        '''
        ccm = ccm.reshape((-1, 3))
        lab_est = self.cs.rgbl2lab(self.src_rgbl_masked@ccm)
        dist = self.distance(lab_est, self.dst_lab_masked)
        dist = np.power(dist, 2)
        if self.weights is not None:
            dist = self.weights_masked_norm*dist
        return sum(dist)

    def calculate(self):
        '''calculate ccm if distance function is de76 de94 and de00'''
        ccm0 = self.inital_func(self.src_rgbl_masked, self.dst_rgbl_masked)
        ccm0 = ccm0.reshape((-1))
        res = fmin(self.loss, ccm0, xtol = self.xtol, ftol = self.ftol)
        if res is not None:
            self.ccm = res.reshape((-1,3))
            print('ccm:', self.ccm)
            print('error:', (self.loss(res)/self.masked_len)**0.5)

    def value(self):
        '''对全流程计算结果进行评价，全流程包括：
        1. 线性化
        2. CCM
        3. 反线性化
        主要在2个方面：
        1. 饱和度，多少输入在返回时被截断了（即输入"属于[0,1]输出在[0,1]外"占输入的比例）；
        2. 分布度，函数返回值在[0, 1]^3的空间的比例
        很可能将 饱和度×分布度 作为最终的评价结果。

        这部分内容将在以后获得支持
        '''
        pass

    def infer(self, img, L=False):
        '''infer using calculated ccm'''
        if self.ccm is None:
            raise Exception('No CCM values!')
        img_lin = self.linear.linearize(img)
        img_ccm = img_lin@self.ccm
        if L:
            return img_ccm
        return self.cs.rgbl2rgb(img_ccm)

    def infer_image(self, imgfile, L=False, inp_size=255, out_size=255, out_dtype = np.uint8):
        '''infer image and output as an BGR image with uint8 type
        mainly for debug!
        '''
        img = cv2.imread(imgfile)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)/inp_size
        out = self.infer(img, L)
        img = np.minimum(np.maximum(np.round(out*out_size), 0), out_size)
        img = img.astype(out_dtype)
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

class CCM_4x3(CCM_3x3):
    def prepare(self):
        self.src_rgbl_masked = self.add_column(self.src_rgbl_masked)
    
    @staticmethod
    def add_column(arr):
        return np.c_[arr, np.ones((*arr.shape[:-1], 1))]

    def initial_white_balance(self, src_rgbl, dst_rgbl):
        '''calculate nonlinear-optimization initial value by white balance:
        res = diag(mean(s_r)/mean(d_r), mean(s_g)/mean(d_g), mean(s_b)/mean(d_b))
        https://www.imatest.com/docs/colormatrix/
        '''
        rs, gs, bs = np.sum(src_rgbl, axis = 0)
        rd, gd, bd = np.sum(dst_rgbl, axis = 0)
        return np.array([[rd/rs, 0, 0], [0, gd/gs, 0], [0, 0, bd/bs]]) 

    def infer(self, img, L=False):
        '''infer using calculated ccm'''
        if self.ccm is None:
            raise Exception('No CCM values!')
        img_lin = self.linear.linearize(img)
        img_ccm = self.add_column(img_lin)@self.ccm
        if L:
            return img_ccm
        return self.cs.rgbl2rgb(img_ccm)
