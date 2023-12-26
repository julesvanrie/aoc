import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint
from collections import deque


dirs = {
    'v': (+1,0),
    '>': (0,+1),
    '^': (-1,0),
    '<': (0,-1),
}

@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])
    field = input

    fieldfilled = [list(r) for r in field]

    result = 0

    start = (0, 1, 0, 0, 0)
    end = (h-1, w-2)

    bifurcs = []
    joins = {}
    nexts = deque([start])
    y, x, c, py, px = start
    restart = True
    while (y, x) != end or nexts:
        if (y, x) == end:
            y, x, c, py, px = start
            continue
        if restart:
            if nexts:
                y, x, c, py, px = nexts.popleft()
        restart = False
        nextdirs = []
        prevdirs = []
        for dy, dx in dirs.values():
            # Out of bounds
            if (y+dy>=h or y+dy<0 or x+dx>=w or x+dx<0):
                continue
            # Wall
            if field[y+dy][x+dx] == '#':
                continue
            # Backtracking
            if y+dy == py and x+dx == px:
                prevdirs.append((dy,dx))
                continue
            # Against direction
            nd = dirs.get(field[y+dy][x+dx], (0,0))
            if dy == -nd[0] and dx == -nd[1]:
                 prevdirs.append((dy,dx))
                 continue
            # Next directions
            nextdirs.append((dy,dx))
        if len(prevdirs) > 1:
            joins[(py,px)] = c
            for pdy, pdx in prevdirs:
                if oldc := joins.get((y+pdy, x+pdx)):
                    c = max(c, oldc)
                else:
                    restart = True
            if restart:
                continue
        if len(nextdirs) == 1:
            ndy, ndx = nextdirs[0]
            py, px = (y, x)
            y, x, c = (y+ndy, x+ndx, c+1)
            fieldfilled[y][x] = c % 10
        elif nextdirs:
            nextnexts = []
            for ndy, ndx in nextdirs:
                if (y+ndy, x+ndx) not in bifurcs:
                    nextnexts.append((y+ndy, x+ndx, c+1, y, x))
            if nextnexts:
                nexts.extend(nextnexts[1:])
                bifurcs.append(nextnexts[0][:2])
                y, x, c, py, px = nextnexts[0]

    result = c

    return result


def next_crossings(field):
    h = len(field)
    w = len(field[0])
    neighbours = {}
    investigate = [(0,1)]
    for y in range(1,h-1):
        for x in range(1,w-1):
            if field[y][x] == '.':
                ns = 0
                for dy, dx in dirs.values():
                    if field[y+dy][x+dx] != '.':
                        ns += 1
                if ns == 4:
                    investigate.append((y,x))

    for y, x in investigate:
        for dy, dx in dirs.values():
            ny = y+dy
            nx = x+dx
            if field[ny][nx] != '#':
                neighbours[(ny,nx)] = find_previous(field, investigate, ny, nx, y, x)

    return neighbours


def find_previous(field, neighbours, y, x, py, px):
    h = len(field)
    w = len(field[0])
    l = 0
    while True:
        for dy, dx in dirs.values():
            ny = y + dy
            nx = x + dx
            # Out of bounds
            if (ny>h-1 or ny<0 or nx>w-1 or nx<0):
                continue
            # Wall
            if field[ny][nx] == '#':
                continue
            # Backtracking
            if ny == py and nx == px:
                continue
            # If in investigate
            if (ny, nx) in neighbours:
                return (ny, nx), l+2
            if (ny == h-1 and nx == w-2) or (ny == 0 and nx == 1):
                return (ny, nx), l+2
            py, px, y, x, l = (y, x, ny, nx, l+1)
            break


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    field = input
    nexts = next_crossings(field)

    start = (0, 1)
    end = (h-1, w-2)

    path = (start,)
    distances = (0,)
    visited = {0: [start]}
    y, x = start
    max_len = 0
    i = 0
    while (y, x) != end:
        lenprevpath = len(path)
        i = len(path) + 1
        for dy, dx in dirs.values():
            ny = y+dy
            nx = x+dx
            if (ny, nx) in nexts:
                n, d = nexts[(ny, nx)]
                if n == end:
                    if sum(distances) + d > max_len:
                        max_len = sum(distances) + d
                    print(max_len, end='\r')
                    continue
                if (n not in path):
                    if n in visited.get(i, []):
                        continue
                    path = path + (n,)
                    distances = distances + (d,)
                    visited[i] = visited.get(i, []) + [n]
                    y, x = n
                    break
        if len(path) == lenprevpath:
            path = path[:-1]
            distances = distances[:-1]
            if i in visited:
                visited[i] = []
            i = len(path)
            if not path:
                break
            y, x = path[-1]

    return max_len


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
