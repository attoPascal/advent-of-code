from dataclasses import dataclass, field
from aocd import lines

@dataclass
class File():
    name: str
    size: int

@dataclass
class Dir():
    name: str
    parent: 'Dir'
    content: dict = field(default_factory=dict)

    @property
    def size(self):
        return sum(f.size for f in self.content.values())

root = Dir('/', parent=None)
cwd = None

for line in lines:
    match line.split():
        case '$', 'cd', '/':
            cwd = root
        case '$', 'cd', '..':
            cwd = cwd.parent
        case '$', 'cd', dirname:
            cwd = cwd.content[dirname]
        case '$', 'ls':
            pass
        case 'dir', name:
            cwd.content[name] = Dir(name, parent=cwd)
        case size, name:
            cwd.content[name] = File(name, int(size))

def all_dirs(cwd=root):
    yield cwd
    for f in cwd.content.values():
        yield from all_dirs(f) if isinstance(f, Dir) else ()

print("Part 1:", sum(dir.size for dir in all_dirs() if dir.size <= 100000))
print("Part 2:", min(dir.size for dir in all_dirs() if dir.size >= root.size - 40000000))
