from skimage import color
import numpy as np
import matplotlib.pyplot as plt
from math import pi, cos, sin
import os
R = 2.5
l = 2.5
theta = 143
tr = theta/180*pi
eps = 1e-6
tr2, tr3 = tr+pi-eps, tr+pi+eps

# r1 = np.array([l, R*cos(tr), R*sin(tr)])
# r2 = np.array([l, R*cos(tr2), R*sin(tr2)])
# r3 = np.array([l, R*cos(tr3), R*sin(tr3)])
# d1 = color.deltaE_ciede2000(r1, r2)
# d2 = color.deltaE_ciede2000(r1, r3)
# d3 = color.deltaE_ciede2000(r2, r3)
# print(f'{d1}+{d3}>{d2}', d1+d3>d2)

# exit()


# a, b = R*cos(tr), R*sin(tr)
# l, a, b = [l, a, b]
def draw(l, a, b, index, v = 201):
    
    # v = 201
    x = np.zeros((v, v))
    y = np.zeros((v, v))
    z = np.zeros((v, v))
    m = (v-1)//2
    for i in range(v):
        for j in range(v):
            da = (i-m)*0.1
            db = (j-m)*0.1
            a2 = a+da
            b2 = b+db
            x[i, j] = a2
            y[i, j] = b2
            cd = color.deltaE_ciede2000(np.array([l, a, b]), np.array([l, a2, b2]))
            print(type(cd), cd)
            z[i, j] = cd
            # exit()

    fig, ax  = plt.subplots()
    ax.scatter([a], [b], color = 'b')
    # ax.axhline(y=0, color='k')
    # ax.axvline(x=0, color='k')

    # # 设置轴的位置
    # ax.spines['left'].set_position('center')
    # # 设置轴的颜色
    # ax.spines['right'].set_color('none')
    # # 设置轴的位置
    # ax.spines['bottom'].set_position('center')
    # # 设置轴的颜色
    # ax.spines['top'].set_color('none')
    ax.set_xlabel('a*')
    ax.set_ylabel('b*')
    CS = ax.contour(x,y,z, 10)
    ax.clabel(CS, inline = 1, fontsize = 10)
    title = f'Macbeth_{index}'
    ax.set_title(title)
    plt.annotate(f'M{index}', xy=(a,b),xytext = (0, -10), textcoords = 'offset points',ha = 'center', va = 'top')

    # plt.show()
    plt.savefig(os.path.join('imgs', title+'.png'))

for i, (l, a, b) in enumerate([[37.542, 12.018, 13.33],
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
		[20.475, 0.049, -0.972]]):
    
    draw(l, a, b, i, 201)
