from skimage import color
import numpy as np
from src.colorspace import sRGB

srgb = sRGB()

def cal_J(rgb, d = 1e-4):
    lab = srgb.rgb2lab(rgb)
    l, a, b = lab
    rgb_l = srgb.lab2rgb([l+d, a, b])
    rgb_a = srgb.lab2rgb([l, a+d, b])
    rgb_b = srgb.lab2rgb([l, a, b+d])
    J = np.stack([(rgb_l-rgb)/d, (rgb_a-rgb)/d, (rgb_b-rgb)/d], axis = -1)
    return J

def cal_k(J, r = 0.5/255):
    return r/max(np.sum(np.abs(J), axis=-1))

def producer():
    for r in range(256):
        r = r/255
        for g in range(256):
            g = g/255
            for b in range(256):
                b = b/255
                yield r,g,b


def run():
    maxk = 1000
    maxrgb = None
    m = 256*256*256
    for i, (r,g,b) in enumerate(producer()):
        if i%256==0:
            print(f"have done {i}/{m}, about {i/m*100:.2f}% percent")
        rgb = np.array([r,g,b])
        J = cal_J(rgb)
        k = cal_k(J)
        if k<maxk:
            maxk = k
            maxrgb = rgb
            print(f"newk:{k}, rgb:{rgb*255}")
    f = open('result.txt', 'w', encoding='utf-8')
    f.write(f"maxk:{maxk}, rgb:{maxrgb}")
    f.flush()

def rands():
    fw = open('fw.txt', 'w', encoding= 'utf-8')
    for r in range(10):
        for g in range(10):
            for b in range(10):
                # rgb = np.random.random(3)

                rgb = [r/9, g/9, b/9]
                fw.write(f"rgb:{rgb}\n")
                # print('rgb:', rgb)
                J = cal_J(rgb)
                k = cal_k(J)
                fw.write(f"k:{k}\n")
                # print('k', k)

from matplotlib import pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D

def draws():
    fw = open('fw.txt', 'w', encoding= 'utf-8')
    for r in range(11):
        gs, bs, zs = [], [], []
        for g in range(11):
            _gs, _bs, _zs = [], [], []
            for b in range(11):
                # rgb = np.random.random(3)
                rgb = [r/10, g/10, b/10]
                fw.write(f"rgb:{rgb}\n")
                # print('rgb:', rgb)
                J = cal_J(rgb)
                k = cal_k(J)
                fw.write(f"k:{k}\n")
                _gs.append(g/10)
                _bs.append(b/10)
                _zs.append(k)
            gs.append(_gs)
            bs.append(_bs)
            zs.append(_zs)
        gs = np.array(gs)
        bs = np.array(bs)
        zs = np.array(zs)
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot_surface(gs,bs,zs,rstride=1, cstride=1, cmap='rainbow')
        plt.show()

def draws2():
    fw = open('fw.txt', 'w', encoding= 'utf-8')
    for l in np.linspace(0, 100, 20):
        gs, bs, zs = [], [], []
        for a in np.linspace(-100, 100, 50):
            _gs, _bs, _zs = [], [], []
            bmax = min((l+16)/116*180, 100)
            for b in np.linspace(-100, bmax, 50):
                # rgb = np.random.random(3)
                rgb = srgb.lab2rgb([l*1., a*1., b*1.])
                # rgb = [r/10, g/10, b/10]
                fw.write(f"rgb:{rgb}\n")
                # print('rgb:', rgb)
                J = cal_J(rgb)
                k = cal_k(J)
                fw.write(f"k:{k}\n")
                _gs.append(a)
                _bs.append(b)
                _zs.append(k)
            gs.append(_gs)
            bs.append(_bs)
            zs.append(_zs)
        gs = np.array(gs)
        bs = np.array(bs)
        zs = np.array(zs)
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot_surface(gs,bs,zs,rstride=1, cstride=1, cmap='rainbow')
        plt.show()

if __name__ == "__main__":
    # run()
    # rands()
    draws2()
    # print(srgb.rgb2lab([1, 0.3, 0.7]))
    # print(srgb.lab2rgb([10.1,10.1,10.1]))

    # rgb = [0.03921569, 1, 1]
    # r,g,b7 = rgb
    # l, a, b = srgb.rgb2lab(rgb)
    # print(l,a,b)
    # lab = color.colorconv.rgb2lab(rgb)
    # print(lab)
    # diff = 0.5/255
    # print(diff)
    # d = 1.4/255
    # print('d', d)
    # J = cal_J(rgb)
    # print(np.linalg.inv(J)@np.array([d, d, d]))
    # print('J',J)
    # tes = [l+d, a+d, b+d]
    # r1,g1,b1 = srgb.lab2rgb(tes)
    # print(r1-r,g1-g,b1-b7)
    # print(color.colorconv.lab2rgb(tes))
