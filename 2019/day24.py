import numpy as np

class Grid():
    mask_outer = np.array([[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1]]) == 1
    mask_inner = np.array([[0,0,0,0,0],[0,1,1,1,0],[0,1,0,1,0],[0,1,1,1,0],[0,0,0,0,0]]) == 1

    def __init__(self, bugs=None, upper=None, lower=None, id=0):
        self.bugs = bugs if bugs is not None else np.zeros((5,5), dtype=bool)
        self.upper = upper
        self.lower = lower
        self.id = id
    
    def __getitem__(self, indices):
        return int(self.bugs[indices])
    
    def spawn_upper(self):
        self.upper = Grid(lower=self, id=self.id+1)
    
    def spawn_lower(self):
        self.lower = Grid(upper=self, id=self.id-1)
    
    def count_self(self):
        return np.sum(self.bugs)
    
    def count_up(self):
        return self.upper.count_self() + self.upper.count_up() if self.upper else 0
    
    def count_down(self):
        return self.lower.count_self() + self.lower.count_down() if self.lower else 0
    
    def count_all(self):
        return self.count_self() + self.count_up() + self.count_down()
    
    def step(self):
        # number of neighbors for each tile
        n = np.zeros_like(self.bugs, dtype=int)

        # outer corners
        n[0,0] = self[0,1] + self[1,0] + (self.upper[1,2] + self.upper[2,1] if self.upper else 0)
        n[0,4] = self[0,3] + self[1,4] + (self.upper[1,2] + self.upper[2,3] if self.upper else 0)
        n[4,0] = self[3,0] + self[4,1] + (self.upper[3,2] + self.upper[2,1] if self.upper else 0)
        n[4,4] = self[3,4] + self[4,3] + (self.upper[3,2] + self.upper[2,3] if self.upper else 0)

        # outer sides
        n[0,1] = self[0,0] + self[0,2] + self[1,1] + (self.upper[1,2] if self.upper else 0)
        n[0,2] = self[0,1] + self[0,3] + self[1,2] + (self.upper[1,2] if self.upper else 0)
        n[0,3] = self[0,2] + self[0,4] + self[1,3] + (self.upper[1,2] if self.upper else 0)
        n[1,0] = self[0,0] + self[2,0] + self[1,1] + (self.upper[2,1] if self.upper else 0)
        n[2,0] = self[1,0] + self[3,0] + self[2,1] + (self.upper[2,1] if self.upper else 0)
        n[3,0] = self[2,0] + self[4,0] + self[3,1] + (self.upper[2,1] if self.upper else 0)
        n[1,4] = self[0,4] + self[2,4] + self[1,3] + (self.upper[2,3] if self.upper else 0)
        n[2,4] = self[1,4] + self[3,4] + self[2,3] + (self.upper[2,3] if self.upper else 0)
        n[3,4] = self[2,4] + self[4,4] + self[3,3] + (self.upper[2,3] if self.upper else 0)
        n[4,1] = self[4,0] + self[4,2] + self[3,1] + (self.upper[3,2] if self.upper else 0)
        n[4,2] = self[4,1] + self[4,3] + self[3,2] + (self.upper[3,2] if self.upper else 0)
        n[4,3] = self[4,2] + self[4,4] + self[3,3] + (self.upper[3,2] if self.upper else 0)

        # inner corners
        n[1,1] = self[0,1] + self[1,0] + self[1,2] + self[2,1]
        n[1,3] = self[0,3] + self[1,2] + self[1,4] + self[2,3]
        n[3,1] = self[2,1] + self[3,0] + self[3,2] + self[4,1]
        n[3,3] = self[2,3] + self[3,2] + self[3,4] + self[4,3]

        # inner sides
        n[1,2] = self[0,2] + self[1,1] + self[1,3] + (sum(self.lower.bugs[0,:]) if self.lower else 0)
        n[2,1] = self[2,0] + self[1,1] + self[3,1] + (sum(self.lower.bugs[:,0]) if self.lower else 0)
        n[2,3] = self[2,4] + self[1,3] + self[3,3] + (sum(self.lower.bugs[:,4]) if self.lower else 0)
        n[3,2] = self[4,2] + self[3,1] + self[3,3] + (sum(self.lower.bugs[4,:]) if self.lower else 0)

        if self.id >= 0:
            if self.upper:
                self.upper.step()
            elif np.sum(self.bugs[self.mask_outer]) != 0:
                self.spawn_upper()
                self.upper.step()
        
        if self.id <= 0:
            if self.lower:
                self.lower.step()
            elif np.sum(self.bugs[self.mask_inner]) != 0:
                self.spawn_lower()
                self.lower.step()

        # calculate new bugs
        not_dead = np.logical_and(self.bugs, n == 1)
        new_bug = np.logical_and(~self.bugs, np.logical_or(n == 1, n == 2))
        self.bugs = np.logical_or(not_dead, new_bug)

if __name__ == "__main__":
    lines = ['##...', '#.###', '.#.#.', '#....', '..###']
    bugs = np.array([[c == '#' for c in line] for line in lines])
    g = Grid(bugs)
    for it in range(200):
        g.step()
    print(g.count_all())
