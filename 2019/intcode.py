from collections import deque
from typing import Optional, Callable

Input = deque[int] | list[int] | Callable[[], int]
Output = deque[int] | list[int] | Callable[[int], None]

class Intcode():
    ops: dict[int, tuple[str, int, int]] = {
        # op, num_reads, num_writes
        1:  ('add', 2, 1),
        2:  ('mul', 2, 1),
        3:  ('inp', 0, 1),
        4:  ('out', 1, 0),
        5:  ('jit', 2, 0),
        6:  ('jif', 2, 0),
        7:  ('les', 2, 1),
        8:  ('equ', 2, 1),
        9:  ('adj', 1, 0),
        99: ('hlt', 0, 0)
    }
    
    def __init__(self, memory: list[int], inp: Optional[Input] = None, out: Optional[Output] = None, extend_memory=1000):
        self.memory = memory.copy() + [0]*extend_memory
        
        match inp:
            case deque():
                self.input = inp.popleft
            case list():
                self.input = lambda: inp.pop(0)
            case None:
                self.input = lambda: int(input())
            case callable:
                self.input = callable

        match out:
            case deque() | list():
                self.output = out.append
            case None:
                self.output = print
            case callable:
                self.output = callable
        
        self.ptr = 0
        self.base = 0
        self.op = ''
        self.args = []
        self.halted = False
    
    def run(self):
        while not self.halted:
            self.fetch_exec()

    def fetch(self):
        if not self.halted:
            op, args = self.getargs(self.ptr)
            self.ptr += len(args) + 1
            self.op = op
            self.args = args

    def exec(self):
        if not self.halted:
            if self.op == 'hlt':
                self.halted = True
            else:
                getattr(self, self.op)(*self.args)
    
    def fetch_exec(self):
        self.fetch()
        self.exec()
    
    def getargs(self, ptr) -> tuple[str, list[int]]:
        instr = self.memory[ptr]
        opcode = instr % 100
        instr //= 100
        op, ninputs, noutputs = self.ops[opcode]
        args: list[int] = []
        for i in range(ninputs+noutputs):
            parmode = instr % 10
            instr //= 10
            par = self.memory[ptr+1+i]
            if i < ninputs:
                if parmode == 0:
                    args.append(self.memory[par])
                if parmode == 1:
                    args.append(par)
                if parmode == 2:
                    args.append(self.memory[self.base + par])
            else:
                if parmode == 0:
                    args.append(par)
                if parmode == 2:
                    args.append(self.base + par)     
        return op, args
    
    def add(self, p1, p2, p3):
        self.memory[p3] = p1 + p2
    
    def mul(self, p1, p2, p3):
        self.memory[p3] = p1 * p2
    
    def inp(self, p1):
        self.memory[p1] = self.input()
    
    def out(self, p1):
        self.output(p1)

    def jit(self, p1, p2):
        if p1:
            self.ptr = p2
    
    def jif(self, p1, p2):
        if not p1:
            self.ptr = p2
    
    def les(self, p1, p2, p3):
        self.memory[p3] = int(p1 < p2)
    
    def equ(self, p1, p2, p3):
        self.memory[p3] = int(p1 == p2)

    def adj(self, p1):
        self.base += p1
