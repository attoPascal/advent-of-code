import numpy as np
from scipy.signal import convolve

def ndconway(initial, ndims=3, niter=6):
    block_shape = tuple([1]*(ndims-2) + list(initial.shape))
    block_index = tuple([0]*(ndims-2))
    kernel_shape = tuple([3] * ndims)
    kernel_index = tuple([1] * ndims)

    blocks = np.zeros(block_shape, dtype=int)
    blocks[block_index, :] = np.where(initial == '#', 1, 0)

    kernel = np.ones(kernel_shape, dtype=int)
    kernel[kernel_index] = 0

    for _ in range(niter):
        neighbors = convolve(blocks, kernel)
        blocks = np.pad(blocks, 1)
        stays_active = np.logical_and(blocks == 1, np.logical_or(neighbors == 2, neighbors == 3))
        becomes_active = np.logical_and(blocks == 0, neighbors == 3)
        blocks = np.where(np.logical_or(stays_active, becomes_active), 1, 0)
    
    return np.sum(blocks)

input = """##.#####
#.##..#.
.##...##
###.#...
.#######
##....##
###.###.
.#.#.#.."""
input = np.array([[c for c in line] for line in input.splitlines()])

print(ndconway(input, ndims=3))
print(ndconway(input, ndims=4))
