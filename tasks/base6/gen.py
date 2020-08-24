#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base64 import b64encode

import string


b64_num_to_char = (
    string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/')
b64_char_to_num = {c: i for i, c in enumerate(b64_num_to_char)}


def byte_to_bits(n):
    assert 0 <= n < 256
    return bin(256 + n)[3:]

def bits_to_pairs(s):
    return list(a+b for a, b in zip(s[::2], s[1::2]))

flag_bytes = b'CTF{f0R6OtT3n-8iT5-;C}'
flag_bits = ''.join(map(byte_to_bits, flag_bytes))
flag_bits_pairs = bits_to_pairs(flag_bits)


def encoded_lines_gen(f):
    for line in f:
        line = line.strip()
        if len(line) == 0:
            continue

        enc = bytearray(b64encode(bytes(line, 'utf-8')))

        if enc.endswith(b'=='):
            bits_pairs_count = 2
        elif enc.endswith(b'='):
            bits_pairs_count = 1
        else:
            bits_pairs_count = 0

        if bits_pairs_count == 0:
            continue

        bits_to_hide = 0
        for _ in range(bits_pairs_count):
            try:
                bits_pair = flag_bits_pairs.pop(0)
            except IndexError as e:
                print('Invalid flag length.')
                raise e
            bits_to_hide <<= 2
            bits_to_hide |= int(bits_pair, 2)

        c = chr(enc[-bits_pairs_count-1])
        n = b64_char_to_num[c]
        n |= bits_to_hide
        c = ord(b64_num_to_char[n])
        enc[-bits_pairs_count-1] = c

        yield enc.decode('ascii')

        if len(flag_bits_pairs) == 0:
            return

with open('text.txt', 'r') as f:
    encoded_lines = list(encoded_lines_gen(f))
with open('enc.txt', 'w') as f:
    for line in encoded_lines:
        f.write(line)
        f.write('\n')
