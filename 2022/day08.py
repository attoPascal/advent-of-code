import numpy as np
from aocd import lines

trees   = np.array([list(line) for line in lines], dtype=int)
visible = np.zeros_like(trees)
scenic  = np.ones_like(trees)

for (x, y), tree in np.ndenumerate(trees):
    directions = [trees[x, :y][::-1], trees[:x, y][::-1], trees[x+1:, y], trees[x, y+1:]]
    for direction in directions:
        if np.all(direction < tree):
            visible[x, y] = 1
            scenic[x, y] *= direction.size
        else:
            scenic[x, y] *= np.argmax(direction >= tree) + 1

print("Part 1:", np.sum(visible))
print("Part 2:", np.max(scenic))
