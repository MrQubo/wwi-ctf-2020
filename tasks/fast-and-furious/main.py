#!/usr/bin/python3

import socket
from time import sleep
from sys import stderr

HOST = '0.0.0.0'
PORT = 8000
FLAG = 'CTF{Th3-F45tEsT-DR4W-1n-Th3-W35T}'
MSG = b"There's absolutely nothing hidden in here!"
assert len(MSG) >= len(FLAG)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, _ = s.accept()
        with conn:
            for flag_char in FLAG:
                try:
                    conn.sendall(flag_char.encode())
                except Exception as e:
                    print(e, file=stderr)
                    pass
                sleep(0.004)
            try:
                cursor_back = b'\033[' + str(len(FLAG)).encode('ascii') + b'D'
                conn.sendall(cursor_back + MSG + b'\n')
            except Exception as e:
                print(e, file=stderr)
                pass
            conn.shutdown(socket.SHUT_RDWR)
