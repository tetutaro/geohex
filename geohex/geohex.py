#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
緯度経度をHexコードに変換する
'''
import math
from .mercator import real2mercator, mercator2real
from .axes import rec2hex, hex2rec
from .child import calc_child, shift_center
from .base30 import encode_str, encode_hexes, decode_hexcode


class GeoHex(object):
    '''
    緯度経度をHexコードに変換するクラス

    :param float lat: 緯度
    :param float lng: 経度
    :param int level: Hexレベル
    :rtype: GeoHexクラス
    '''

    # 緯度（引数として与えられたもの）
    lat = None
    # 経度（引数として与えられたもの）
    lng = None
    # Hex情報を格納する辞書
    hexes = None

    def __init__(self, lat, lng, level=10):
        if not (isinstance(lat, int) or isinstance(lat, float)):
            raise TypeError("latitude is must be int or float")
        if not (isinstance(lng, int) or isinstance(lng, float)):
            raise TypeError("longitude is must be int or float")
        if not isinstance(level, int):
            raise TypeError("level is must be int")
        if not -85.5 <= lat <= 85.5:
            raise ValueError("latitude is must be between -85.0 and 85.0")
        if not -180.0 <= lng <= 180.0:
            raise ValueError("longitude is must be between -180.0 and 180.0")
        if not -2 <= level <= 15:
            raise ValueError("level is must be between -2 and 15")
        self.hexes = dict()
        self.lat = lat
        self.lng = lng
        # 内部計算用のHexレベルに変換する
        level += 3
        # メルカトル図法における角度（要するに赤道と子午線をそれぞれx軸y軸としたときの座標）を計算する
        lat, lng = real2mercator(lat, lng)
        # Hexレベル0の中心から辺までの長さ（半径と呼んでしまう）（単位：角度）
        h0 = 60.0 * math.sqrt(3.0)
        # Hexレベル0の一辺の長さ（単位：角度）
        e0 = 120.0
        # Hexの辺と直行する斜めの座標系（３進数）に変換する
        x0, x1, x2 = rec2hex(lat, lng, h0, level)
        # 各座標の符号
        x0s, x1s, x2s = x0[0], x1[0], x2[0]
        # 指定された緯度経度の座標
        t_x0, t_x1, t_x2 = x0s, x1s, x2s
        # Hexの中心の座標
        c_x0, c_x1, c_x2 = 0, 0, 0
        # Hex番号を格納するリスト
        hexes = list()
        # Hexレベル0から指定されたレベルまで計算する
        for i in range(level):
            # そのHexレベルの半径と一辺の長さ
            h = round(h0 / pow(3.0, i), 15)
            e = round(e0 / pow(3.0, i), 15)
            # 子Hex番号を計算してhexesに追加する
            d0, d1, d2 = calc_child(
                x0s, x0[i + 1],
                x1s, x1[i + 1],
                x2s, x2[i + 1],
                hexes
            )
            # 指定された緯度経度の座標を計算する（単位：子Hexの半径）
            t_x0 = (t_x0 * 3) + x0[i + 1]
            t_x1 = (t_x1 * 3) + x1[i + 1]
            t_x2 = (t_x2 * 3) + x2[i + 1]
            # 子Hexの中心座標を計算する（単位：子Hexの半径）
            c_x0 = (c_x0 * 3) + d0
            c_x1 = (c_x1 * 3) + d1
            c_x2 = (c_x2 * 3) + d2
            # Hex中心からの符号を計算する
            x0s = 0 if t_x0 >= c_x0 else -1
            x1s = 0 if t_x1 >= c_x1 else -1
            x2s = 0 if t_x2 >= c_x2 else -1
            if i > -3:
                # Hexレベルiにおける情報
                i_ret = dict()
                i_ret['level'] = i - 2
                # HexコードをHex情報に追加する
                if i > 1:
                    i_ret['code'] = encode_hexes(hexes)
                else:
                    i_ret['code'] = 'xx' + ''.join(str(x) for x in hexes)
                i_ret['raw_code'] = ''.join(str(x) for x in hexes)
                # 中心の緯度経度を計算する
                c_lat, c_lng = hex2rec(c_x0 * h, c_x1 * h, c_x2 * h)
                # 中心とHexの各頂点の緯度経度を計算してHex情報に追加する
                i_ret['center'] = mercator2real(c_lat, c_lng)
                i_ret['right'] = mercator2real(c_lat, c_lng + e)
                i_ret['t_right'] = mercator2real(c_lat + h, c_lng + (0.5 * e))
                i_ret['t_left'] = mercator2real(c_lat + h, c_lng - (0.5 * e))
                i_ret['left'] = mercator2real(c_lat, c_lng - e)
                i_ret['b_left'] = mercator2real(c_lat - h, c_lng - (0.5 * e))
                i_ret['b_right'] = mercator2real(c_lat - h, c_lng + (0.5 * e))
                # Hex情報を追加
                self.hexes[i - 2] = i_ret
        return

    def __str__(self):
        info = list()
        info.append("緯度: %f, 経度: %f" % (self.lat, self.lng))
        for i in range(len(self.hexes)):
            i_hex = self.hexes[i - 2]
            info.append("レベル%d" % i_hex['level'])
            info.append("  コード: %s" % i_hex['code'])
            info.append("  RAWコード: %s" % i_hex['raw_code'])
            info.append(
                "  中心座標: (%f, %f)" % (
                    i_hex['center'][0],
                    i_hex['center'][1]
                )
            )
            info.append(
                "  右: (%f, %f)" % (i_hex['right'][0], i_hex['right'][1])
            )
            info.append(
                "  右上: (%f, %f)" % (i_hex['t_right'][0], i_hex['t_right'][1])
            )
            info.append(
                "  左上: (%f, %f)" % (i_hex['t_left'][0], i_hex['t_left'][1])
            )
            info.append(
                "  左: (%f, %f)" % (i_hex['left'][0], i_hex['left'][1])
            )
            info.append(
                "  左下: (%f, %f)" % (i_hex['b_left'][0], i_hex['b_left'][1])
            )
            info.append(
                "  右下: (%f, %f)" % (i_hex['b_right'][0], i_hex['b_right'][1])
            )
        return '\n'.join(info)


# Hexコードの数字部分
integer_str = "012345678"


def code2hex(code):
    '''
    HexコードからHex情報を計算する

    :param str code: Hexコード
    :rtype: Hex情報の辞書
    '''
    if not isinstance(code, str):
        raise TypeError("code is must be str")
    if len(code) < 2:
        raise ValueError("invalid code")
    for i, c in enumerate(code):
        if i < 2:
            if c not in encode_str and c != 'x':
                raise ValueError("invalid code")
        else:
            if c not in integer_str:
                raise ValueError("invalid code")
    if code[0:2] == 'xx':
        hexes = [int(x) for x in code[2:]]
    else:
        hexes = decode_hexcode(code)
    c_x0, c_x1, c_x2 = 0, 0, 0
    for child in hexes:
        d0, d1, d2 = shift_center(child)
        c_x0 = (c_x0 * 3) + d0
        c_x1 = (c_x1 * 3) + d1
        c_x2 = (c_x2 * 3) + d2
    level = len(hexes)
    h0 = 60.0 * math.sqrt(3.0)
    e0 = 120.0
    h = round(h0 / pow(3.0, level - 1), 15)
    e = round(e0 / pow(3.0, level - 1), 15)
    hex_info = dict()
    hex_info['level'] = level - 3
    hex_info['code'] = code
    hex_info['raw_code'] = ''.join([str(x) for x in hexes])
    c_lat, c_lng = hex2rec(c_x0 * h, c_x1 * h, c_x2 * h)
    hex_info['center'] = mercator2real(c_lat, c_lng)
    hex_info['right'] = mercator2real(c_lat, c_lng + e)
    hex_info['t_right'] = mercator2real(c_lat + h, c_lng + (0.5 * e))
    hex_info['t_left'] = mercator2real(c_lat + h, c_lng - (0.5 * e))
    hex_info['left'] = mercator2real(c_lat, c_lng - e)
    hex_info['b_left'] = mercator2real(c_lat - h, c_lng - (0.5 * e))
    hex_info['b_right'] = mercator2real(c_lat - h, c_lng + (0.5 * e))
    return hex_info
