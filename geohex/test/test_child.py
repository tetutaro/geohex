#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from ..child import _calc_child, _shift_parent

expected_children = [
	([-1, 0, -1, 2, 0, 2], [-3, 6, -3]),
	([-1, 0, 0, 0, 0, 2], [-3, 6, -3]),
	([-1, 0, 0, 0, 0, 1], [0, 0, 0]),
	([-1, 0, 0, 1, 0, 1], [0, 0, 0]),
	([-1, 0, 0, 1, 0, 0], [0, 0, 0]),
	([-1, 0, 0, 2, 0, 0], [-1, 2, -1]),
	([-1, 0, 0, 2, -1, 2], [-1, 2, -1]),
	([-1, 1, -1, 1, 0, 2], [1, 1, 0]),
	([-1, 1, -1, 2, 0, 2], [1, 1, 0]),
	([-1, 1, -1, 2, 0, 1], [1, 1, 0]),
	([-1, 1, 0, 0, 0, 1], [0, 0, 0]),
	([-1, 1, 0, 0, 0, 0], [0, 0, 0]),
	([-1, 1, 0, 1, 0, 0], [0, 0, 0]),
	([-1, 1, 0, 1, -1, 2], [3, 3, 0]),
	([-1, 1, 0, 2, -1, 2], [3, 3, 0]),
	([-1, 1, 0, 2, -1, 1], [3, 3, 0]),
	([-1, 2, -1, 0, 0, 2], [2, 2, 0]),
	([-1, 2, -1, 1, 0, 2], [1, 1, 0]),
	([-1, 2, -1, 1, 0, 1], [1, 1, 0]),
	([-1, 2, -1, 2, 0, 1], [1, 1, 0]),
	([-1, 2, -1, 2, 0, 0], [4, 4, 0]),
	([-1, 2, 0, 0, 0, 0], [4, 4, 0]),
	([-1, 2, 0, 0, -1, 2], [4, 4, 0]),
	([-1, 2, 0, 1, -1, 2], [3, 3, 0]),
	([-1, 2, 0, 1, -1, 1], [3, 3, 0]),
	([-1, 2, 0, 2, -1, 1], [3, 3, 0]),
	([-1, 2, 0, 2, -1, 0], [6, 6, 0]),
	([0, 0, -1, 0, 0, 2], [2, 2, 0]),
	([0, 0, -1, 0, 0, 1], [5, 5, 0]),
	([0, 0, -1, 1, 0, 1], [5, 5, 0]),
	([0, 0, -1, 1, 0, 0], [5, 5, 0]),
	([0, 0, -1, 2, 0, 0], [4, 4, 0]),
	([0, 0, -1, 2, -1, 2], [4, 4, 0]),
	([0, 0, 0, 0, -1, 2], [4, 4, 0]),
	([0, 0, 0, 0, -1, 1], [7, 7, 0]),
	([0, 0, 0, 1, -1, 1], [7, 7, 0]),
	([0, 0, 0, 1, -1, 0], [7, 7, 0]),
	([0, 0, 0, 2, -1, 0], [6, 6, 0]),
	([0, 1, -1, 0, 0, 1], [5, 5, 0]),
	([0, 1, -1, 0, 0, 0], [5, 5, 0]),
	([0, 1, -1, 1, 0, 0], [5, 5, 0]),
	([0, 1, -1, 1, -1, 2], [8, 8, 0]),
	([0, 1, -1, 2, -1, 2], [8, 8, 0]),
	([0, 1, -1, 2, -1, 1], [8, 8, 0]),
	([0, 1, 0, 0, -1, 1], [7, 7, 0]),
	([0, 1, 0, 0, -1, 0], [7, 7, 0]),
	([0, 1, 0, 1, -1, 0], [7, 7, 0]),
	([0, 2, -1, 0, 0, 0], [9, 6, 1]),
	([0, 2, -1, 0, -1, 2], [9, 6, 1]),
	([0, 2, -1, 1, -1, 2], [8, 8, 0]),
	([0, 2, -1, 1, -1, 1], [8, 8, 0]),
	([0, 2, -1, 2, -1, 1], [8, 8, 0]),
	([0, 2, -1, 2, -1, 0], [11, 2, 3]),
	([0, 2, 0, 0, -1, 0], [11, 2, 3]),
]

expected_centers = {
	-3: (-3, 0, 3),
	-1: (-3, 3, 0),
	0: (-2, 1, 1),
	1: (-1, -1, 2),
	2: (0, -3, 3),
	3: (-1, 2, -1),
	4: (0, 0, 0),
	5: (1, -2, 1),
	6: (0, 3, -3),
	7: (1, 1, -2),
	8: (2, -1, -1),
	9: (3, -3, 0),
	11: (3, 0, -3),
}


def test_calc_child():
	for x, r in expected_children:
		x0s, x0, x1s, x1, x2s, x2 = x
		r_move, r_child, r_diff = r
		r_d0, r_d1, r_d2 = expected_centers[r_move]
		d0, d1, d2, child, diff = _calc_child(x0s, x0, x1s, x1, x2s, x2)
		assert r_child == child
		assert r_diff == diff
		assert r_d0 == d0
		assert r_d1 == d1
		assert r_d1 == d1
	return


expected_parents = {
	0: {
		-1: (2, -1),
		-3: (6, -3),
		3: (3, 0),
		1: (1, 0),
	},
	1: {
		-1: (0, 0),
		-3: (7, -3),
		3: (4, 0),
		1: (2, 0),
	},
	2: {
		-1: (1, 0),
		-3: (8, -3),
		3: (5, 0),
		1: (0, 1),
	},
	3: {
		-1: (5, -1),
		-3: (0, 0),
		3: (6, 0),
		1: (4, 0),
	},
	4: {
		-1: (3, 0),
		-3: (1, 0),
		3: (7, 0),
		1: (5, 0),
	},
	5: {
		-1: (4, 0),
		-3: (2, 0),
		3: (8, 0),
		1: (3, 1),
	},
	6: {
		-1: (8, -1),
		-3: (3, 0),
		3: (0, 3),
		1: (7, 0),
	},
	7: {
		-1: (6, 0),
		-3: (4, 0),
		3: (1, 3),
		1: (8, 0),
	},
	8: {
		-1: (7, 0),
		-3: (5, 0),
		3: (2, 3),
		1: (6, 1),
	},
}


def test_shift_parent():
	for pp in range(9):
		for p in range(9):
			for diff in [-3, -1, 1, 3]:
				hexes = [4, pp, p]
				before_hexes = hexes[:]
				temp_diff = diff
				_shift_parent(hexes, -1, diff)
				for off in range(2, -1, -1):
					c_parent = hexes[off]
					x_parent = before_hexes[off]
					e_parent, next_diff = expected_parents[x_parent][temp_diff]
					assert c_parent == e_parent
					temp_diff = next_diff
					if temp_diff == 0:
						break
	return
