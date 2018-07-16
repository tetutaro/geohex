#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
メルカトル図法の角度に変換する
'''
import math


def real2mercator(lat, lng):
    '''
    実際の緯度経度から、メルカトル図法における緯度経度
    （要するに地図における赤道と子午線をそれぞれx軸y軸とした直行座標系の座標）
    に変換する
    緯度の計算にはグーデルマン関数の逆関数（ランベルト関数）を用いる。
    簡単のためにWolframAlpfaにある式を使う
    cf. http://mathworld.wolfram.com/InverseGudermannian.html

    :param float lat: 実際の緯度（角度）
    :param float lng: 実際の経度（角度）
    :rtype: メルカトル図法における緯度、経度
    '''
    rad_lat = math.radians(lat)
    mer_rad = math.log((1.0 / math.cos(rad_lat)) + math.tan(rad_lat))
    return math.degrees(mer_rad), lng


def mercator2real(lat, lng):
    '''
    実際の緯度経度から、メルカトル図法における緯度経度に変換する
    緯度の計算にはグーデルマン関数を用いる。
    簡単のためにWolframAlpfaにある式を使う
    cf. http://mathworld.wolfram.com/Gudermannian.html

    :param float lat: メルカトル図法における緯度（角度）
    :param float lng: メルカトル図法における経度（角度）
    :rtype: 実際の緯度、経度
    '''
    rad_lat = math.radians(lat)
    real_rad = 2.0 * math.atan(math.tanh(0.5 * rad_lat))
    return round(math.degrees(real_rad), 8), round(lng, 8)
