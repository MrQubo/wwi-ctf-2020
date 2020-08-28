#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from io import StringIO


def calc_solution(num):
    out = StringIO()

    def write_name_h(n, k):
        for _ in range(n):
            if k % 3 == 0:
                out.write('przeddzidzia ')
            elif k % 3 == 1:
                out.write('sroddzidzia ')
            else:
                out.write('zadzidzia ')
            k //= 3
        out.write('dzidy')

    def write_name(n, k):
        if n == 0:
            out.write('Dzida')
            return
        if k % 3 == 0:
            out.write('Przeddzidzie ')
        elif k % 3 == 1:
            out.write('Sroddzidzie ')
        else:
            out.write('Zadzidzie ')
        write_name_h(n-1, k//3)

    def step(n, k):
        write_name(n, k)
        out.write(' sklada sie z przeddzidzia ')
        write_name_h(n, k)
        out.write(', sroddzidzia ')
        write_name_h(n, k)
        out.write(' i zadzidzia ')
        write_name_h(n, k)
        out.write('.\n')

    for n in range(num):
        for k in range(3**n):
            step(n, k)

    return out.getvalue()


def solve(num):
    return solution[num-1]


if __name__ == '__main__':
    print(calc_solution(eval(input())))
else:
    solution = [calc_solution(n) for n in range(1, 11)]
