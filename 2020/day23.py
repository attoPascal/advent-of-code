from collections import deque
from rich.progress import track

class Cups():
    def __init__(self, initial_values, extend=0):
        num_init = len(initial_values)
        self.max = max(initial_values) + extend
        self.cups = deque(initial_values + list(range(num_init+1, self.max+1)))
        self.prev_index = 0
    
    def find_index(self, value):
        try:
            if self.cups[self.prev_index] == value:
                i = self.prev_index
            else:
                i = self.cups.index(value)
            self.prev_index = i
            return i
        except ValueError:
            value -= 1
            if value < 1:
                value = self.max
            return self.find_index(value)
    
    def move(self):
        current = self.cups.popleft()
        self.cups.append(current)

        pick_up = [self.cups.popleft(), self.cups.popleft(), self.cups.popleft()]

        dest = self.find_index(current-1)
        self.cups.insert(dest+1, pick_up[0])
        self.cups.insert(dest+2, pick_up[1])
        self.cups.insert(dest+3, pick_up[2])

if __name__ == "__main__":
    input = '284573961'
    cups = Cups([int(n) for n in input], extend=1_000_000-9)

    for i in track(range(10_000_000)):
        #if not i % 100:
        #    cups.cups.rotate(-100)
        cups.move()

    cups = list(cups.cups)
    i = cups.index(1)
    cups = cups[i:] + cups[:i]
    print(cups[1] * cups[2])
