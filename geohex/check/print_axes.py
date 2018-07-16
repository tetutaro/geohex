#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
axes.pyの関数を検証する
'''
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
from ..axes import _rec2hex, hex2rec


degrees = np.arange(-180.0, 180.0, 360.0 / 1000)
x0s = list()
x1s = list()
x2s = list()
for d in degrees:
    r = math.radians(d)
    x0, x1, x2 = _rec2hex(math.sin(r), math.cos(r))
    x0s.append(x0)
    x1s.append(x1)
    x2s.append(x2)
plt.plot(degrees, x0s, color=sns.husl_palette(3)[0], label="x0")
plt.plot(degrees, x1s, color=sns.husl_palette(3)[1], label="x1")
plt.plot(degrees, x2s, color=sns.husl_palette(3)[2], label="x2")
plt.xlabel("degree")
plt.ylabel("x0/x1/x2")
plt.xlim(-180.0, 180.0)
plt.ylim(-1.0, 1.0)
plt.legend(loc=0)
plt.savefig("axes_x1x2.png")

plt.clf()

xs = list()
ys = list()
for i in range(1000):
    y, x = hex2rec(x0s[i], x1s[i], x2s[i])
    xs.append(x)
    ys.append(y)
plt.plot(xs, ys, color=sns.husl_palette(2)[0], label="rectangle coodinate")
plt.xlabel("x")
plt.ylabel("y")
plt.xlim(-1.0, 1.0)
plt.ylim(-1.0, 1.0)
plt.legend(loc=0)
plt.savefig("axes_xy.png")
