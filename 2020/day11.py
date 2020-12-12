import numpy as np

with open('input11.txt') as f:
    lines = f.read().splitlines()

symbol = {'.': 2, 'L': 3, '#': 5}
seats2  = np.array([[symbol[c] for c in line] for line in lines], dtype=int)

def check_taken(dir):
    if dir.size == 0:
        return False
    prod = np.prod(dir)
    if prod % symbol['L'] != 0:
        return True
    if prod % symbol['#'] != 0:
        return False
    print(prod)
    print(dir)
    print(np.nonzero(dir == symbol['#']), np.nonzero(dir == symbol['L']) )
    return np.nonzero(dir == symbol['#'])[0][0] < np.nonzero(dir == symbol['L'])[0][0]    

def check_directions(seats, x, y):
    seat = seats[x, y]
    if seat == symbol['.']:
        return seat
    
    n = seats[:x, y][::-1]
    s = seats[x+1:, y]
    w = seats[x, :y][::-1]
    e = seats[x, y+1:]
    nw = np.rot90(seats[:x,     :y], 2).diagonal()
    ne = np.rot90(seats[:x,   y+1:], 3).diagonal()
    se = np.rot90(seats[x+1:, y+1:], 0).diagonal()
    sw = np.rot90(seats[x+1:,   :y], 1).diagonal()
    dirs = [n, ne, e, se, s, sw, w, nw]

    neighbors = sum(check_taken(dir) for dir in dirs)

    if seat == symbol['L'] and neighbors == 0:
        return symbol['#']
    if seat == symbol['#'] and neighbors >= 5:
        return symbol['L']
    return seat

it = 0
while True:
    print(it)
    it += 1
    new_seats = seats2.copy()
    for (x, y), s in np.ndenumerate(seats2):
        new_seats[x, y] = check_directions(seats2, x, y)

    if np.array_equal(seats2, new_seats):
        print("====")
        print(np.count_nonzero(seats2 == symbol['#']))
        break
    if it > 5:
        break
    seats2 = new_seats
