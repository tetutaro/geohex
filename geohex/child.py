#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Hex番号を計算する
'''


def calc_child(x0s, x0, x1s, x1, x2s, x2, hexes):
	'''
	Hex座標から子Hex番号を計算してhexesに格納する
	子Hex番号により親Hex番号が変わるケースにも対応

	:param int x0s: 親Hexを中心としたx0座標の符号(0 or -1)
	:param int x0: 親Hexを中心としたx0座標
	:param int x1s: 親Hexを中心としたx1座標の符号(0 or -1)
	:param int x1: 親Hexを中心としたx1座標
	:param int x2s: 親Hexを中心としたx2座標の符号(0 or -1)
	:param int x2: 親Hexを中心としたx2座標
	:param list hexes: hex番号リスト
	:rtype: x0,x1,x2軸それぞれの中心移動量
	'''
	d0, d1, d2, child, diff = _calc_child(x0s, x0, x1s, x1, x2s, x2)
	_shift_parent(hexes, -1, diff)
	hexes.append(child)
	return d0, d1, d2


def shift_center(n):
	'''
	Hex番号からHex中心のずれを計算する

	:param int n: Hex番号
	:param int o: Hex列オフセット
	:rtype: x0,x1,x2各軸の中心のずれ（単位：Hex半径）
	'''
	return _shift_center(n // 3, n % 3)


def _calc_child(x0s, x0, x1s, x1, x2s, x2):
	'''
	子Hex番号を計算する内部関数

	:param int x0s: 親Hexを中心としたx0座標の符号(0 or -1)
	:param int x0: 親Hexを中心としたx0座標
	:param int x1s: 親Hexを中心としたx1座標の符号(0 or -1)
	:param int x1: 親Hexを中心としたx1座標
	:param int x2s: 親Hexを中心としたx2座標の符号(0 or -1)
	:param int x2: 親Hexを中心としたx2座標
	:rtype: 移動Hex番号、子Hex番号、親Hex番号の差分
	'''
	x0v = x0 + (x0s * 3)
	x1v = x1 + (x1s * 3)
	x2v = x2 + (x2s * 3)
	# 親子判定ロジック
	y = (x1v - x2v + 1) // 3
	o = (y - x1v + 2 + ((x0v - y + 1) // 2)) // 2
	l = (-y - x2v + 2 + ((x0v + y + 1) // 2)) // 2
	move = (3 * l) + o
	if 0 <= move <= 8:
		# 親Hex番号が変わらない場合
		child = move
		diff = 0
	else:
		# 親Hex番号が変わる場合
		if move in [-1, 11]:
			child = 2
		else:  # move in [-3, 9]:
			child = 6
		if 8 < move:
			diff = move - 8
		else:  # move < 0
			diff = move
	d0, d1, d2 = _shift_center(l, o)
	return d0, d1, d2, child, diff


def _shift_center(l, o):
	'''
	Hex列,Hex列offsetから中心のずれを計算する内部関数

	:param int l: Hex列番号
	:param int o: Hex列オフセット
	:rtype: x0,x1,x2各軸の中心のずれ（単位：Hex半径）
	'''
	d0 = o + l - 2
	d1 = l + 1 - (2 * o)
	d2 = o + 1 - (2 * l)
	return d0, d1, d2


def _shift_parent(hexes, offset, diff):
	'''
	親Hex番号をずらす内部関数

	:param list hexes: Hex番号リスト
	:param int offset: 何番目のHexをずらすか（負の値）
	:param int diff: Hex番号の差分
	:param int move: 移動Hex番号
	:rtype: None
	'''
	if diff == 0:
		return
	parent = hexes[offset]
	# Hexの並びが折れ曲がる場合の特殊ケース
	if (diff == -1) and (parent in [0, 3, 6]):
		parent -= 6
	elif (diff == 1) and (parent in [2, 5, 8]):
		parent += 6
	# 親のHex番号を更新
	parent += diff
	if 0 <= parent <= 8:
		diff = 0
	parent = parent % 9
	hexes[offset] = parent
	# さらに親をずらす処理を行う、再帰的呼び出し
	offset -= 1
	return _shift_parent(hexes, offset, diff)
