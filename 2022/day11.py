import re
from collections.abc import Callable
from dataclasses import dataclass
from math import prod
from types import CodeType

from aocd import data

@dataclass
class Monkey:
    items: list[int]
    op: CodeType
    divisor: int
    if_true: int
    if_false: int
    handled: int = 0

    operation = lambda self, old: eval(self.op)
    test = lambda self, n: n % self.divisor == 0

def parse_monkey(spec: str) -> Monkey:
    items = [int(n) for n in re.findall(r'Starting items: (.+)', spec)[0].split(', ')]
    op = compile(re.findall(r'Operation: new = (.+)', spec)[0], '<string>', 'eval')
    divisor = int(re.findall(r'Test: divisible by (\d+)', spec)[0])
    throw = [int(n) for n in re.findall(r'If \w+: throw to monkey (\d+)', spec)]
    
    return Monkey(items, op, divisor, throw[0], throw[1])

def observe(monkeys: list[Monkey], rounds: int, manage_worry: Callable[[int], int]) -> list[int]:
    for _ in range(rounds):
        for monkey in monkeys:
            for item in monkey.items:
                item = manage_worry(monkey.operation(item))
                throw_to = monkey.if_true if monkey.test(item) else monkey.if_false
                monkeys[throw_to].items.append(item)
            monkey.handled += len(monkey.items)
            monkey.items = []
    
    return [monkey.handled for monkey in monkeys]

if __name__ == '__main__':
    monkeys1 = [parse_monkey(m) for m in data.split('\n\n')]
    monkey_business1 = sorted(observe(monkeys1, rounds=20, manage_worry=lambda x: x // 3), reverse=True)
    print("Part 1:", prod(monkey_business1[:2]))

    monkeys2 = [parse_monkey(m) for m in data.split('\n\n')]
    modulo = prod(monkey.divisor for monkey in monkeys2)
    monkey_business2 = sorted(observe(monkeys2, rounds=10_000, manage_worry=lambda x: x % modulo), reverse=True)
    print("Part 2:", prod(monkey_business2[:2]))
