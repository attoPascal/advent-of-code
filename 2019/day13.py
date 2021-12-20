from intcode import Intcode
from collections import deque
import numpy as np

with open('input13.txt') as f:
    instructions = [int(n) for n in f.read().split(',')]

def run(part):
    input = deque()
    output = deque()
    intcode = Intcode(instructions, input=input, output=output)
    intcode.memory[0] = part

    screen = np.zeros((44, 24))
    score = 0
    paddle = 0

    while True:
        if intcode.halted:
            break

        if len(output) >= 3:
            x = output.popleft()
            y = output.popleft()
            t = output.popleft()

            if x == -1 and y == 0:
                score = t
            else:
                screen[x, y] = t
                if t == 3:
                    paddle = x
                if t == 4:
                    ball = x
                    input.append(np.sign(ball - paddle))
        else:
            intcode.fetch_exec()

    return screen, score

screen, _ = run(1)
print(np.count_nonzero(screen == 2))

_, score = run(2)
print(score)
