from skimage import color
import numpy as np
import matplotlib.pyplot as plt
from math import pi, cos, sin
R = 2.5
l = 2.5
theta = 143
tr = theta/180*pi
eps = 1e-6
tr2, tr3 = tr+pi-eps, tr+pi+eps

r1 = np.array([l, R*cos(tr), R*sin(tr)])
r2 = np.array([l, R*cos(tr2), R*sin(tr2)])
r3 = np.array([l, R*cos(tr3), R*sin(tr3)])
d1 = color.deltaE_ciede2000(r1, r2)
d2 = color.deltaE_ciede2000(r1, r3)
d3 = color.deltaE_ciede2000(r2, r3)
print(f'{d1}+{d3}>{d2}', d1+d3>d2)

exit()
a, b = R*cos(tr), R*sin(tr)
L, a, b = [l, a, b]

v = 201
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
        cd = color.deltaE_ciede2000(np.array([L, a, b]), np.array([L, a2, b2]))
        print(type(cd), cd)
        z[i, j] = cd
        # exit()

fig, ax  = plt.subplots()
CS = ax.contour(x,y,z, 10)
ax.clabel(CS, inline = 1, fontsize = 10)
ax.set_title("xxx")
plt.show()