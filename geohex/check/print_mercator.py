#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
mercator.pyの関数を検証する
'''
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from ..mercator import real2mercator, mercator2real


real_lats = np.arange(-85.0, 85.0, 170.0 / 2000.0)
lngs = np.arange(-180.0, 180.0, 360.0 / 2000.0)
m_lats = list()
m_lngs = list()
for i in range(2000):
	m_lat, m_lng = real2mercator(real_lats[i], lngs[i])
	m_lats.append(m_lat)
	m_lngs.append(m_lng)
plt.plot(real_lats, m_lats, color=sns.husl_palette(2)[0], label="latitude")
plt.plot(lngs, m_lngs, color=sns.husl_palette(2)[1], label="longitude")
plt.xlabel("latitude/longitude (real)")
plt.ylabel("latitude/longitude (mercator)")
plt.xlim(-180.0, 180.0)
plt.ylim(-180.0, 180.0)
plt.legend(loc=0)
plt.savefig("latlng_merc.png")

plt.clf()

merc_lats = np.arange(-180.0, 180.0, 360.0 / 2000.0)
r_lats = list()
r_lngs = list()
for i in range(2000):
	r_lat, r_lng = mercator2real(merc_lats[i], lngs[i])
	r_lats.append(r_lat)
	r_lngs.append(r_lng)
plt.plot(merc_lats, r_lats, color=sns.husl_palette(2)[0], label="latitude")
plt.plot(lngs, r_lngs, color=sns.husl_palette(2)[1], label="longitude")
plt.xlabel("latitude/longitude (mercator)")
plt.ylabel("latitude/longitude (real)")
plt.xlim(-180.0, 180.0)
plt.ylim(-180.0, 180.0)
plt.legend(loc=0)
plt.savefig("latlng_real.png")
