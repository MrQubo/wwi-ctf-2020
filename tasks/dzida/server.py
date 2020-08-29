#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from io import StringIO

import socketserver

from recurse_interpreter import Interpreter
from dzida import solve
from secret import FLAG


class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            self.request.sendall(b'Gib me your code!\n')
            self.request.sendall(b"Your code can't have more than 10^5 characters.\n")
            self.request.sendall(b"End the code with line ' -- CODE END --'.\n")
            code = []
            for line in self.rfile:
                line = line.decode('ascii')
                if line[-1] == '\n':
                    line = line[:-1]
                if line == ' -- CODE END --':
                    break
                code.append(line)
            code = '\n'.join(code)
            if len(code) > 100 * 1000:
                self.request.sendall(b'Your code is too long!\n')
                return
            interpreter = Interpreter()
            interpreter.parser.parse(code)
            for n in range(1, 11):
                interpreter.stdin = StringIO(str(n))
                interpreter.stdout = StringIO()
                interpreter.execute()
                if solve(n).strip() != interpreter.stdout.getvalue().strip():
                    self.request.sendall(b'Nope!\n')
                    return
                else:
                    self.request.sendall(b'OK!\n')
            self.request.sendall(bytes(FLAG))
        except Exception:
            import traceback
            from sys import stderr
            traceback.print_exc()
            stderr.flush()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    HOST_PORT = '0.0.0.0', 8000
    with ThreadedTCPServer(HOST_PORT, ThreadedTCPRequestHandler) as server:
        server.serve_forever()
