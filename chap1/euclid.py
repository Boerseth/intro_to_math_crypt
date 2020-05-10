from typing import List, Tuple
from math import copysign

import numpy as np


def gcd(a: int, b: int) -> int:
    return abs(a) if b == 0 else gcd(b, a % b)


def gcd_nonrecursive(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def solve_lin(a: int, b: int) -> Tuple[int, int]:
    """Given (a, b), find integers (u, v) such that
               au + bv = gcd(a, b)
    """
    # Special cases:
    if a < 0:
        u, v = solve_lin(-a, b)
        return -u, v
    if b < 0:
        u, v = solve_lin(a, -b)
        return u, -v
    if a == 0 or b == 0:
        return copysign(1, a), copysign(1, b)

    # Simplify problem
    gcd_ab = gcd(a, b)
    if gcd_ab > 1:
        return solve_lin(a // gcd_ab, b // gcd_ab)

    # Euclidean algorithm
    r1, r2 = a, b
    q1, q2 = 1, 0
    p1, p2 = 0, 1
    sign = 1
    while r2 != 0:
        q = (r1 - r1 % r2) // r2
        sign = -sign
        r1, r2 = r2, r1 % r2
        q1, q2 = q2, q * q2 + q1
        p1, p2 = p2, q * p2 + p1
    assert a * q1 - b * p1 == sign
    return sign * q1, -sign * p1


if __name__ == "__main__":
    print("Testing the equation solver for a, b = -100, ... , 100")
    for a in range(-100, 100):
        for b in range(-100, 100):
            u, v = solve_lin(a, b)
            assert a * u + b * v == gcd(a, b)
    print("Success!")
