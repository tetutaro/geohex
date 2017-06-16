#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import numpy as np
from ..axes import _degree2offset, _offset2base3


def test_degree2offset():
	xlist = np.random.rand(10) * 6.0 - 3.0
	xlist = list(xlist)
	xlist.append(-2.99999999999999)
	xlist.append(2.99999999999999)
	for x in xlist:
		t1x, _, _ = _degree2offset(x, x, x, 1.0, 1)
		t2x, _, _ = _degree2offset(x, x, x, 1.0, 2)
		t3x, _, _ = _degree2offset(x, x, x, 1.0, 3)
		assert t1x == t2x // 3
		assert t1x == t3x // 9
		t3x = t3x % 9
		assert t2x % 3 == t3x // 3
	return


def test_offset2base3_positive():
	i = 0
	for d1 in range(3):
		for d2 in range(3):
			for d3 in range(3):
				x0, _, _ = _offset2base3(i, i, i, 3)
				assert x0[0] == 0
				assert x0[1] == d1
				assert x0[2] == d2
				assert x0[3] == d3
				i += 1


def test_offset2base3_negative():
	i = -1
	for d1 in range(3):
		for d2 in range(3):
			for d3 in range(3):
				x0, _, _ = _offset2base3(i, i, i, 3)
				assert x0[0] == -1
				assert x0[1] == 2 - d1
				assert x0[2] == 2 - d2
				assert x0[3] == 2 - d3
				i -= 1
	return
