from functools import reduce

from aocd import lines
from more_itertools import chunked, divide, one


def common_item(collections):
    return one(reduce(set.intersection, collections[1:], set(collections[0])))

def priority(item):
    return ord(item) - 38 if item.isupper() else ord(item) - 96

compartments = (divide(2, rucksack) for rucksack in lines)
wrong_items  = (common_item(c) for c in compartments)
badge_items  = (common_item(group) for group in chunked(lines, 3))

print("Part 1:", sum(priority(item) for item in wrong_items))
print("Part 2:", sum(priority(item) for item in badge_items))
