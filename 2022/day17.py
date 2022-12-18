import aocd
import numpy as np
from itertools import cycle
from typing import Iterator, Iterable

class Chamber:
    tower_height: int
    grid: np.ndarray
    rock: np.ndarray | None
    rock_offset: np.ndarray
    pattern: Iterator[str]
    rocks: Iterator[np.ndarray]

    def __init__(self, pattern: Iterable[str], grid_height: int = 4000):
        self.tower_height = 0
        self.grid = np.zeros((grid_height, 7), dtype=int)
        self.pattern = cycle(pattern)
        self.rocks = cycle([
            np.array([[1, 1, 1, 1]]),
            np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]),
            np.array([[1, 1, 1], [0, 0, 1], [0, 0, 1]]),
            np.array([[1], [1], [1], [1]]),
            np.array([[1, 1], [1, 1]])
        ])

    @property
    def rock_position(self) -> tuple[slice, slice]:
        assert self.rock is not None
        return slice(self.rock_offset[0], self.rock_offset[0] + self.rock.shape[0]), \
            slice(self.rock_offset[1], self.rock_offset[1] + self.rock.shape[1])
    
    @property
    def collision(self) -> bool:
        assert self.rock is not None
        return bool(np.any(self.grid[self.rock_position] & self.rock))
    
    @property
    def out_of_bounds(self) -> bool:
        assert self.rock is not None
        return bool(np.any(self.rock_offset < 0) or self.rock_offset[1] + self.rock.shape[1] > self.grid.shape[1])

    def spawn_rock(self):
        self.rock = next(self.rocks)
        self.rock_offset = np.array([self.tower_height + 3, 2])

    def land_rock(self):
        assert not self.out_of_bounds and not self.collision
        self.grid[self.rock_position] |= self.rock
        self.tower_height = max(self.tower_height, self.rock_position[0].stop)
        self.rock = None
    
    def move_rock(self):
        move_offset = [0, 1] if next(self.pattern) == '>' else [0, -1]   
        self.rock_offset += move_offset
        if self.out_of_bounds or self.collision:
            self.rock_offset -= move_offset
    
    def drop_rock(self):
        move_offset = [-1, 0]
        self.rock_offset += move_offset
        if self.out_of_bounds or self.collision:
            self.rock_offset -= move_offset
            self.land_rock()
    
    def simulate_rocks(self, n: int):
        for _ in range(n):
            self.spawn_rock()
            while self.rock is not None:
                self.move_rock()
                self.drop_rock()
    
    def __str__(self) -> str:
        return '\n'.join(
            ''.join('▅' if cell else '░' for cell in line)
            for line in np.flipud(self.grid)
            if np.sum(line) > 0
        )


pattern = aocd.get_data(day=17, year=2022).strip()
chamber = Chamber(pattern)
chamber.simulate_rocks(n=2022)

print(chamber)
print(chamber.tower_height)
