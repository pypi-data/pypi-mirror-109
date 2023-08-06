# coding=utf-8
from itertools import count
from typing import Iterable

from oeis.registry import registry
from oeis.utils import aliquot_sum


@registry.register("A000396")
def perfect() -> Iterable[int]:
    """Perfect numbers."""
    for n in count(start=1):
        k: int = aliquot_sum(n)
        if k == n:
            yield n
