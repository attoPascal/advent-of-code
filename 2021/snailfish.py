from math import floor, ceil
from copy import deepcopy

class SnailfishNumber():
    def __init__(self, number):
        if isinstance(number, int):
            self.number = number
        else:
            left = number[0] if isinstance(number[0], SnailfishNumber) else SnailfishNumber(number[0])
            right = number[1] if isinstance(number[1], SnailfishNumber) else SnailfishNumber(number[1])
            self.number = [left, right]
    
    @property
    def is_regular(self):
        return isinstance(self.number, int)
    
    @property
    def regular(self):
        assert(self.is_regular)
        return self.number
    
    @property
    def left(self):
        return self.number[0]
    
    @property
    def right(self):
        return self.number[1]
    
    @property
    def magnitude(self):
        if self.is_regular:
            return self.regular
        return 3*self.left.magnitude + 2*self.right.magnitude
    
    def explode(self):
        if self.is_regular:
            return False
        
        regular_paths = []
        leftmost_explode = None

        for i1, n1 in enumerate(self.number):
            if n1.is_regular:
                regular_paths.append([i1])
                continue
            for i2, n2 in enumerate(n1.number):
                if n2.is_regular:
                    regular_paths.append([i1, i2])
                    continue
                for i3, n3 in enumerate(n2.number):
                    if n3.is_regular:
                        regular_paths.append([i1, i2, i3])
                        continue
                    for i4, n4 in enumerate(n3.number):
                        if n4.is_regular:
                            regular_paths.append([i1, i2, i3, i4])
                            continue
                        else:
                            leftmost_explode = leftmost_explode or ([i1, i2, i3, i4], n4)
                        for i5, n5 in enumerate(n4.number):
                            assert(n5.is_regular)
                            regular_paths.append([i1, i2, i3, i4, i5])


        if leftmost_explode:
            path, exploding_number = leftmost_explode
            path2num = lambda path: sum(p*n for p, n in zip(path, [8, 4, 2, 1]))
            path_index = path2num(path)
            prev_regulars = [i for i in regular_paths if path2num(i) < path_index]
            next_regulars = [i for i in regular_paths if path2num(i) > path_index]
            if prev_regulars:
                prev_path = prev_regulars[-1]
                left = self[prev_path].regular + exploding_number.left.regular
                self[prev_path] = left
            if next_regulars:
                next_path = next_regulars[0]
                right = self[next_path].regular + exploding_number.right.regular
                self[next_path] = right
            self[path] = 0
            return True
        return False
    
    def split(self):
        if self.is_regular:
            return
        
        leftmost_split = None
        for i1, n1 in enumerate(self.number):
            if n1.is_regular:
                leftmost_split = (leftmost_split or ([i1], n1)) if n1.regular > 9 else leftmost_split
                continue
            for i2, n2 in enumerate(n1.number):
                if n2.is_regular:
                    leftmost_split = (leftmost_split or ([i1, i2], n2)) if n2.regular > 9 else leftmost_split
                    continue
                for i3, n3 in enumerate(n2.number):
                    if n3.is_regular:
                        leftmost_split = (leftmost_split or ([i1, i2, i3], n3)) if n3.regular > 9 else leftmost_split
                        continue
                    for i4, n4 in enumerate(n3.number):
                        if n4.is_regular:
                            leftmost_split = (leftmost_split or ([i1, i2, i3, i4], n4)) if n4.regular > 9 else leftmost_split
        if leftmost_split:
            path, split = leftmost_split
            self[path] = [floor(split.regular/2), ceil(split.regular/2)]
            return True
        return False

    def reduce(self):
        while True:
            if self.explode():
                continue
            if self.split():
                continue
            break
    
    def __add__(self, other):
        s = SnailfishNumber([deepcopy(self), deepcopy(other)])
        s.reduce()
        return s
    
    def __getitem__(self, path):
        if self.is_regular:
            return self.regular
        if len(path) == 1:
            return self.number[path[0]]
        return self.number[path[0]][path[1:]]
    
    def __setitem__(self, path, value):
        if not isinstance(value, SnailfishNumber):
            value = SnailfishNumber(value)
        if len(path) == 1:
            self.number[path[0]] = value
        else:
            self.number[path[0]][path[1:]] = value
    
    def __repr__(self):
        if self.is_regular:
            return str(self.regular)
        return f'[{self.left},{self.right}]'
