#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string


b64_num_to_char = (
    string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/')
b64_char_to_num = {c: i for i, c in enumerate(b64_num_to_char)}


def byte_to_bits(n):
    assert 0 <= n < 256
    return bin(256 + n)[3:]


def flag_bits_gen(f):
    for enc in f:
        enc = enc.strip()

        if enc.endswith('=='):
            bits_pairs_count = 2
        elif enc.endswith('='):
            bits_pairs_count = 1
        else:
            bits_pairs_count = 0

        if bits_pairs_count == 0:
            continue
        elif bits_pairs_count == 1:
            mask = 0b11
        else:
            mask = 0b1111

        c = enc[-bits_pairs_count-1]
        n = b64_char_to_num[c]
        hidden_bits = n & mask

        yield from byte_to_bits(hidden_bits)[-2*bits_pairs_count:]

flag = []
with open('enc.txt', 'r') as f:
    flag_bits = ''.join(flag_bits_gen(f))
for i in range(0, len(flag_bits), 8):
    byte_bits = flag_bits[i:i+8]
    flag.append(chr(int(byte_bits, 2)))
print(''.join(flag))
