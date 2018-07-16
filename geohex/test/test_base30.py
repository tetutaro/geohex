#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
base30.pyの検証をする
'''
from ..base30 import encode_str, _decode_char
from ..base30 import _encode_base30, _decode_base30


def test_decode_char():
    for i, c in enumerate(encode_str):
        assert i == _decode_char(c)
    return


def test_encode_decode():
    for val in range(900):
        v0, v1, v2 = val // 100, (val % 100) // 10, val % 10
        s0, s1 = _encode_base30(v0, v1, v2)
        r_v0, r_v1, r_v2 = _decode_base30(s0, s1)
        assert s0 in encode_str
        assert s1 in encode_str
        assert v0 == r_v0
        assert v1 == r_v1
        assert v2 == r_v2
