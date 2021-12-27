# %%
from copy import copy
from functools import cache

# %%
class Burrow():
    def __init__(self, a, b, c, d):
        self.hallway = [None] * 11
        self.room_a = list(a)
        self.room_b = list(b)
        self.room_c = list(c)
        self.room_d = list(d)
        self.energy = 0
        self.energy_consumption = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
        self.connections = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
        self.hallway_steppable = set(range(len(self.hallway))) - set(self.connections.values())
    
    def __getitem__(self, tile):
        if len(tile) == 1:
            return {'H': self.hallway,
                    'A': self.room_a,
                    'B': self.room_b,
                    'C': self.room_c,
                    'D': self.room_d}[tile]
        return self[tile[0]][int(tile[1:])]
    
    def __setitem__(self, tile, value):
        room, num = self.coords(tile)
        if   room == 'H': self.hallway = self.hallway.copy()
        elif room == 'A': self.room_a = self.room_a.copy()
        elif room == 'B': self.room_b = self.room_b.copy()
        elif room == 'C': self.room_c = self.room_c.copy()
        elif room == 'D': self.room_d = self.room_d.copy()
        self[room][num] = value
    
    @classmethod
    @cache
    def coords(cls, tile):
        return tile[0], int(tile[1:])
    
    def can_move_from_room(self, room, num):
        # assert(room in 'ABCD')
        if all(a == room for a in self[room] if a):
            return False # room already in target organization
        if any(a for a in self[room][:num]):
            return False # can't move past other amphipod
        con = self.connections[room]
        if self[f'H{con-1}'] and self[f'H{con+1}']:
            return False # no space in hallway
        return True
    
    def can_move_from_hallway(self, num):
        amphipod = self.hallway[num]
        if not all(a == amphipod for a in self[amphipod] if a):
            return False # can't join amphipods in wrong room
        con = self.connections[amphipod]
        path = self.hallway[min(num+1, con):max(num, con+1)]
        if any(a for a in path):
            return False # can't reach entrace
        return True

    def can_move(self, from_room, from_num, to_room, to_num):
        if not self[from_room][from_num]:
            return False # from empty
        if self[to_room][to_num]:
            return False # to occupied
        if from_room in 'ABCD' and not self.can_move_from_room(from_room, from_num):
            return False
        if from_room == 'H' and not self.can_move_from_hallway(from_num):
            return False
        
        amphipod = self[from_room][from_num]
        if to_room in 'ABCD':
            if amphipod != to_room:
                return False # can only move to home room
            if not all(a for a in self[to_room][to_num+1:]):
                return False # can't leave empty spaces below
            return True
        else:
            con = self.connections[from_room]
            path = self.hallway[min(to_num+1, con):max(to_num, con+1)]
            if any(a for a in path):
                return False # can't go that far in hallway
            return True
    
    def move(self, from_tile, to_tile, energy=None):
        # assert(self.can_move_to(from_tile, to_tile))
        self.energy += energy or self.energy_for_move(from_tile, to_tile)
        self[to_tile] = self[from_tile]
        self[from_tile] = None
    
    def energy_for_move(self, from_tile, to_tile):
        from_room, from_num = self.coords(from_tile)
        to_room, to_num = self.coords(to_tile)

        amphipod = self[from_room][from_num]
        if from_room == 'H':
            hall_num, room_num, room = from_num, to_num, to_room
        else:
            hall_num, room_num, room = to_num, from_num, from_room
        
        hall_steps = abs(hall_num - self.connections[room])
        room_steps = room_num + 1
        return (hall_steps + room_steps) * self.energy_consumption[amphipod]

    @property
    def valid_moves(self):
        # from hallway to room
        for room in 'ABCD':
            tiles = self[room]
            vacant_num = sum(1 for a in tiles if not a) - 1
            if vacant_num >= 0:
                for from_num in self.hallway_steppable:
                    if self.can_move('H', from_num, room, vacant_num):
                        # stepping home is alway an optimal move
                        m = (f'H{from_num}', f'{room}{vacant_num}')
                        return [m]
        #from room to hallway
        moves = []
        for room in 'ABCD':
            tiles = self[room]
            occupied_num = len(tiles) - sum(1 for a in tiles if a)
            if occupied_num < len(tiles):
                for to_num in self.hallway_steppable:
                    if self.can_move(room, occupied_num, 'H', to_num):
                        moves.append((f'{room}{occupied_num}', f'H{to_num}'))
        return moves
    
    @property
    def finished(self):
        f = True
        for room in 'ABCD':
            f &= all(a == room for a in self[room])
        return f
    
    def print(self):
        def tile(room, num):
            if num < 0 or num >= len(self[room]):
                return '#'
            t = self[room][num]
            return t if t else '.'
        
        for a in range(len(self.hallway) + 2):
            print('#', end='')
        print()
        print('#', end='')
        for h in range(len(self.hallway)):
            print(tile('H', h), end='')
        print('#')

        max_len = max(len(self[r]) for r in 'ABCD')
        print(f"###{tile('A', 0)}#{tile('B', 0)}#{tile('C', 0)}#{tile('D', 0)}###")
        for r in range(max_len):
            print(f"  #{tile('A', r+1)}#{tile('B', r+1)}#{tile('C', r+1)}#{tile('D', r+1)}#  ")


# %%
abort_energy = float('inf')
def try_all_moves(burrow, moves=None):
    global abort_energy
    moves = moves or []
    
    if burrow.energy < abort_energy:
        if burrow.finished:
            abort_energy = burrow.energy
            yield burrow, moves
        else:
            valid_moves = burrow.valid_moves
            energy = [burrow.energy_for_move(*m) for m in valid_moves]
            for e, m in sorted(zip(energy, valid_moves)):
                b2 = copy(burrow)
                b2.move(*m, energy=e)
                yield from try_all_moves(b2, moves + [m])


if __name__ == '__main__':
    # burrow = Burrow('DB', 'DA', 'CB', 'CA')
    burrow = Burrow('DDDB', 'DCBA', 'CBAB', 'CACA')

    abort_energy = float('inf')
    for solution in try_all_moves(burrow):
        print(solution[0].energy, solution[1])

    for m in solution[1]:
        burrow.print()
        print()
        burrow.move(*m)
    burrow.print()
