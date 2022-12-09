from dataclasses import dataclass, field
from itertools import chain
from aocd import lines

@dataclass
class Dir():
    parent: 'Dir'
    dirs: dict = field(default_factory=dict)
    filesize: int = 0

    def mkdir(self, name):
        self.dirs[name] = Dir(parent=self)
    
    @property
    def size(self):
        return self.filesize + sum(d.size for d in self.dirs.values())
    
    @property
    def tree(self):
        yield self
        yield from chain.from_iterable(d.tree for d in self.dirs.values())

root = Dir(parent=None)
cwd = None

for line in lines:
    match line.split():
        case '$', 'cd', '/':
            cwd = root
        case '$', 'cd', '..':
            cwd = cwd.parent
        case '$', 'cd', name:
            cwd = cwd.dirs[name]
        case '$', 'ls':
            pass
        case 'dir', name:
            cwd.mkdir(name)
        case size, name:
            cwd.filesize += int(size)

print("Part 1:", sum(d.size for d in root.tree if d.size <= 100000))
print("Part 2:", min(d.size for d in root.tree if d.size >= root.size - 40000000))
