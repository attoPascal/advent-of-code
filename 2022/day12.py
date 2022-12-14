import numpy as np
import networkx as nx
from aocd import lines

def elevation(char):
    return ord(char) - ord('a')

grid = np.array([[elevation(char) for char in line] for line in lines])
graph = nx.grid_2d_graph(*grid.shape, create_using=nx.DiGraph)

s = np.where(grid == elevation('S'))
start = s[0][0], s[1][0]
grid[start] = elevation('a')

e = np.where(grid == elevation('E'))
end = e[0][0], e[1][0]
grid[end] = elevation('z')

for node, elev in np.ndenumerate(grid):
    for neighbor in list(graph.neighbors(node)):
        if grid[neighbor] - elev > 1:
            graph.remove_edge(node, neighbor)

print("Part 1:", nx.shortest_path_length(graph, start, end))

def shortest_shortest_path(graph, end, grid):
    for length, layer in enumerate(nx.bfs_layers(graph.reverse(), end)):
        for node in layer:
            if grid[node] == 0:
                return length

print("Part 2:", shortest_shortest_path(graph, end, grid))
