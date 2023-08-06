# coding=utf-8
"""Various utility functions."""
from functools import lru_cache
from math import gcd, isqrt
from typing import List, Set

__all__ = [
    "aliquot_sum",
    "coprime",
    "divisors",
    "proper_divisors",
    "sigma",
]


def aliquot_sum(n: int) -> int:
    """Return the aliquot sum of n - s(n)."""
    return sum(proper_divisors(n))


def coprime(a: int, b: int) -> bool:
    """Determine whether a and b are coprime."""
    return gcd(a, b) == 1


@lru_cache
def divisors(n: int) -> List[int]:
    """Return the divisors of n."""
    ret: Set[int] = set()
    for i in range(1, isqrt(n) + 1):
        if n % i == 0:
            ret.add(i)
            ret.add(n // i)
    return sorted(ret)


@lru_cache
def proper_divisors(n: int) -> List[int]:
    """Return the proper divisors of n."""
    return divisors(n)[:-1]


def sigma(n: int) -> int:
    """Return the sum of the positive divisors of n, including 1 and n itself."""
    return sum(divisors(n))
