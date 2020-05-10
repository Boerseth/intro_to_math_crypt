from time import time
from typing import Callable, Iterable, List


def get_base_two(number: int) -> str:
    return bin(number)[2:]


def get_repeated_squares(base: int, mod: int) -> Iterable[int]:
    base = base % mod  # Can be removed if we know that  base < mod
    while True:
        yield base
        base = (base * base) % mod


def power_fast(base: int, power: int, mod: int) -> int:
    power_digits = get_base_two(power)
    base_squares = get_repeated_squares(base, mod)
    result = 1
    for base_square, digit in zip(base_squares, reversed(power_digits)):
        if digit == "1":
            result = (result * base_square) % mod
    return result


def my_timeit(f: Callable, number: int = 10000) -> float:
    start = time()
    for _ in range(number):
        f()
    end = time()
    return end - start


if __name__ == "__main__":
    # Try timing the allegedly faster and naive computation
    base, power, mod = 123463, 1234, 43414123414143
    fast_expr = lambda: power_fast(base, power, mod)
    slow_expr = lambda: (base ** power) % mod

    # Quick check that it works
    print(fast_expr())
    print(slow_expr())
    assert fast_expr() == slow_expr()

    fast_time = my_timeit(fast_expr)
    slow_time = my_timeit(slow_expr)

    print(f"Time lapsed 'fast': {fast_time}s")
    print(f"Time lapsed 'slow': {slow_time}s (should be MUCH slower)")
