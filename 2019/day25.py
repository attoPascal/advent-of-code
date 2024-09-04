import aocd
from intcode import Intcode
from collections import deque

data = aocd.get_data(day=25, year=2019)
instructions = [int(n) for n in data.split(',')]

actions = [ord(c) for c in """\
east
take whirled peas
north
take coin
west
north
west
take astrolabe
east
south
south
take antenna
north
east
south
east
north
take prime number
south
east
east
east
take dark matter
west
west
west
west
west
north
take fixed point
north
take weather machine
east
"""]

input_deque = deque(actions)

for n in range(256):
    s = ""
    s += "take dark matter\n" if (1 & n) else "drop dark matter\n"
    s += "take coin\n" if (2 & n) else "drop coin\n"
    s += "take whirled peas\n" if (4 & n) else "drop whirled peas\n"
    s += "take fixed point\n" if (8 & n) else "drop fixed point\n"
    s += "take astrolabe\n" if (16 & n) else "drop astrolabe\n"
    s += "take prime number\n" if (32 & n) else "drop prime number\n"
    s += "take antenna\n" if (64 & n) else "drop antenna\n"
    s += "take weather machine\n" if (128 & n) else "drop weather machine\n"
    s += "south\n"
    input_deque.extend([ord(c) for c in s])

def inp():
    if len(input_deque) == 0:
        input_deque.extend([ord(c) for c in input()] + [10])
    return input_deque.popleft()

def out(o):
    print(chr(o), end='')

Intcode(instructions, inp, out).run()
