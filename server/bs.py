#!/usr/bin/python
# -*- coding: utf-8 -*-
import binascii

s = u'ls\r'
str_16 = binascii.hexlify(s)  # 字符串转16进制
print(str_16)
un_str_16 = binascii.unhexlify(str_16)  # 字符串转16进制
print(un_str_16)
