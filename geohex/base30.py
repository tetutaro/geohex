#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Hexコードの先頭３つを30進数変換して２文字に圧縮する
'ABCDEFG...' という文字列ひとつで格好良く変換できるが、
面倒くさいので辞書で持っちゃうことにする
'''

# 30進数の文字列に変換する文字列
encode_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcde"


def _decode_char(c):
    '''
    30進数の文字列から整数に直す関数

    :param char c: 30進数の文字
    :rtype: 30進数の整数
    '''
    c_ord = ord(c)
    if 96 < c_ord:
        return c_ord - 71
    else:
        return c_ord - 65


def _encode_base30(v0, v1, v2):
    '''
    30進数変換して３桁の数字を２文字に変換する内部関数

    :param int c0: ３桁目の数字
    :param int c2: ２桁目の数字
    :param int c3: １桁目の数字
    :rtype: 30進数変換した２つの文字
    '''
    val = (v0 * 100) + (v1 * 10) + v2
    return encode_str[val // 30], encode_str[val % 30]


def _decode_base30(s0, s1):
    '''
    圧縮された２文字を30進数変換して３桁の数字にする内部関数

    :param str s0: ２桁目の文字
    :param str s1: １桁目の文字
    :rtype: 30進数逆変換した３つの整数
    '''
    val = (_decode_char(s0) * 30) + _decode_char(s1)
    return val // 100, (val % 100) // 10, val % 10


def encode_hexes(hexes):
    '''
    Hex番号の配列から30進数変換しつつHexコードを生成する

    :param list hexes: Hex番号のリスト
    :rtype: Hexコードの文字列
    '''
    s1, s2 = _encode_base30(hexes[0], hexes[1], hexes[2])
    return s1 + s2 + ''.join([str(x) for x in hexes[3:]])


def decode_hexcode(hexcode):
    '''
    Hexコードから30進数変換してHex番号の文字列を生成する

    :param str hexcode: Hexコード
    :rtype: Hex番号のリスト
    '''
    hexes = list(_decode_base30(hexcode[0], hexcode[1]))
    hexes.extend([int(x) for x in hexcode[2:]])
    return hexes
