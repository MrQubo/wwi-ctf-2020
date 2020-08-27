#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
from subprocess import check_call, CalledProcessError

try:
    check_call(['gzip', '-d', 'Bluebird.bmp.gz'])
except CalledProcessError:
    pass

FLAG = b'CTF{Us3le55-Byt3Z}'
with open('Bluebird.bmp', 'rb') as f:
    data = bytearray(f.read())
for i, x in enumerate(FLAG):
    data[0x8d + 4*i] = x
with open('Bluebird.bmp', 'wb') as f:
    f.write(data)

check_call(['gzip', 'Bluebird.bmp'])
