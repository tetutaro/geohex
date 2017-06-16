#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
直交座標系とHexの並行する辺のペアと直行する斜交座標系の変換
'''
import math


def _rec2hex(lat, lng):
	'''
	直交座標系から、Hexの並行する辺のペアと直行する斜交座標系に変換する内部関数

	:param float lat: 緯度（y座標）
	:param float lng: 経度（x座標）
	:rtype: 12時の方向であるx0軸、4時の方向であるx1軸、8時の方向であるx2軸それぞれの座標
	'''
	rad_x1 = math.pi / 6.0
	x1 = (lng * math.cos(rad_x1)) - (lat * math.sin(rad_x1))
	rad_x2 = math.pi * 5.0 / 6.0
	x2 = (lng * math.cos(rad_x2)) - (lat * math.sin(rad_x2))
	return lat, x1, x2


def _degree2offset(x0, x1, x2, h0, digits):
	'''
	斜交座標系の各座標を、求めるHexの半径で丸める

	:param float x0: x0座標
	:param float x1: x1座標
	:param float x2: x2座標
	:param float h0: レベル0のHex半径
	:param int digit: 求める３進数の桁数
	:rtype: x0,x1,x2各軸をHex半径で丸めた値
	'''
	h = round(h0 / pow(3, digits - 1), 15)
	x0 = math.floor(x0 / h)
	x1 = math.floor(x1 / h)
	x2 = math.floor(x2 / h)
	return x0, x1, x2


def _offset2base3(x0, x1, x2, digits):
	'''
	斜交座標系の各座標を符号付き３進数のリストに変換する

	:param float x0: x0座標
	:param float x1: x1座標
	:param float x2: x2座標
	:param int digit: 求める３進数の桁数
	:rtype: x0,x1,x2軸それぞれの座標の符号付き３進数のリスト
	'''
	x0s = list()
	x1s = list()
	x2s = list()
	for i in range(digits + 1):
		base = pow(3, digits - i)
		x0s.append(x0 // base)
		x1s.append(x1 // base)
		x2s.append(x2 // base)
		x0 = x0 % base
		x1 = x1 % base
		x2 = x2 % base
	return x0s, x1s, x2s


def rec2hex(lat, lng, h0, digits):
	'''
	直交座標系から、Hexの並行する辺のペアと直行する斜交座標系に変換する
	さらに斜交座標系を最小値を０とした３進数変換する

	:param float lat: 緯度（y座標）
	:param float lng: 経度（x座標）
	:param float h0: 元となるHexの半径
	:param int digit: 求める３進数の桁数
	:rtype: 12時の方向であるx0軸、10時の方向であるx1軸、8時の方向であるx2軸それぞれの座標（３進数）
	'''
	x0, x1, x2 = _rec2hex(lat, lng)
	x0, x1, x2 = _degree2offset(x0, x1, x2, h0, digits)
	return _offset2base3(x0, x1, x2, digits)


def hex2rec(x0, x1, x2):
	'''
	Hexの並行する辺のペアと直行する斜交座標系から直交座標系に変換する

	:param float x0: x0座標
	:param float x1: x1座標
	:param float x2: x2座標
	:rtype: 直交座標系のy座標（緯度）、x座標（経度）
	'''
	return x0, (x0 + (2.0 * x1)) / math.sqrt(3.0)
