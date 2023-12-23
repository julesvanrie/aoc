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


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])
    field = [['#' if c == '#' else '.' for c in r] for r in input]

    fieldfilled = [r for r in field]

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


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
