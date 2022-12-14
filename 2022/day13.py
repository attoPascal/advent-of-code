import json
from itertools import chain
from functools import cmp_to_key
from typing import Any

from aocd import data


def compare_ints(left: int, right: int) -> int:
    return left - right

def compare_lists(left: list[Any], right: list[Any]) -> int:
    for l, r in zip(left, right):
        if not_same := compare(l, r):
            return not_same
    return len(left) - len(right)

def compare(left: list[Any] | int, right: list[Any] | int) -> int:
    if isinstance(left, int) and isinstance(right, int):
        return compare_ints(left, right)
    left = [left] if isinstance(left, int) else left
    right = [right] if isinstance(right, int) else right
    return compare_lists(left, right)


pairs = [tuple(map(json.loads, p.splitlines())) for p in data.split('\n\n')]
print("Part 1:", sum(i for i, (left, right) in enumerate(pairs, 1) if compare(left, right) < 0))

packets = [p for p in chain.from_iterable(pairs)]
packets += [[[2]], [[6]]]
packets.sort(key=cmp_to_key(compare))
print("Part 2:", (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1))
