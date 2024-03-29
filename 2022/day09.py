import math
from aocd import lines

def move(knot, direction):
    match direction:
        case 'R': return knot + 1
        case 'L': return knot - 1
        case 'U': return knot + 1j
        case 'D': return knot - 1j

def follow(knot, prev):
    diff = prev - knot
    if abs(diff) < 2:
        return knot
    else:
        hstep = math.copysign(diff.real != 0, diff.real)
        vstep = math.copysign(diff.imag != 0, diff.imag)
        return knot + complex(hstep, vstep)

def simulate(rope_length, directions):
    rope = [0j] * rope_length
    visited = set()

    for direction, steps in directions:
        for _ in range(steps):
            rope[0] = move(rope[0], direction)
            for knot in range(1, len(rope)):
                rope[knot] = follow(rope[knot], rope[knot-1])
            visited.add(rope[-1])

    return visited

directions = [(line[0], int(line[2:])) for line in lines]

print("Part 1:", len(simulate(2,  directions)))
print("Part 2:", len(simulate(10, directions)))
