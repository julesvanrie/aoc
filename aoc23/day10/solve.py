import sys
from aocsolution.basesolution import BaseSolution

import re
from pprint import pprint

@BaseSolution.time_this
def solve_one(self):
    result = 0
    p = self.get_data()
    h = len(p)
    w = len(p[0])

    # Find start
    for y in range(h):
        if (x := p[y].find('S')) != -1:
            sx = x
            sy = y
            break

    # Distances
    d = [[-1 for i in range(w)] for j in range(h)]
    d[sy][sx] = 0

    # Connections
    c = {
        (0, -1): ['-', 'F', 'L'],
        (0, +1): ['-', '7', 'J'],
        (-1, 0): ['|', 'F', '7'],
        (+1, 0): ['|', 'L', 'J'],
    }

    dirs = {
        '|': [(-1, 0), (+1, 0)],
        '-': [(0, -1), (0, +1)],
        'J': [(0, -1), (-1, 0)],
        '7': [(0, -1), (+1, 0)],
        'L': [(0, +1), (-1, 0)],
        'F': [(0, +1), (+1, 0)],
        'S': c.keys()
    }

    # Next positions
    n = [(sy, sx)]
    for y, x in n:
        # Check all directions
        for dy, dx in dirs[p[y][x]]:
            ny = y + dy
            nx = x + dx
            # If not beyond the border
            if (ny>=0 and ny<h and
                nx>=0 and nx<w):
                # If not checked before
                if d[ny][nx] == -1:
                    # If connected to previous one
                    if p[ny][nx] in c[(dy,dx)]:
                        # # If two neighbours
                        # nn = 0
                        # for ndy, ndx in c.keys():
                        #     # If not beyond the border
                        #     if (ny+ndy>0 and ny+ndy<h and
                        #         nx+ndx>0 and nx+ndx<w):
                        #         if p[ny+ndy][nx+ndx] in c[(dy,dx)]:
                        #             nn += 1
                        #             # print(nn)
                        # if True or nn == 2:
                        n.append((y+dy, x+dx))
                        d[y+dy][x+dx] = d[y][x] + 1

    return max(max(r) for r in d)


@BaseSolution.time_this
def solve_two(self):
    result = 0
    p = self.get_data()
    p = ['-'.join(r) for r in p]
    p = [p[i//2] if not i % 2 else '|'*len(p[0]) for i in range(len(p)*2)]

    h = len(p)
    w = len(p[0])

    # Find start
    for y in range(h):
        if (x := p[y].find('S')) != -1:
            sx = x
            sy = y
            break

    # Distances
    d = [[-1 for i in range(w)] for j in range(h)]
    d[sy][sx] = 0

    # Connections
    c = {
        (0, -1): ['-', 'F', 'L'],
        (0, +1): ['-', '7', 'J'],
        (-1, 0): ['|', 'F', '7'],
        (+1, 0): ['|', 'L', 'J'],
    }

    dirs = {
        '|': [(-1, 0), (+1, 0)],
        '-': [(0, -1), (0, +1)],
        'J': [(0, -1), (-1, 0)],
        '7': [(0, -1), (+1, 0)],
        'L': [(0, +1), (-1, 0)],
        'F': [(0, +1), (+1, 0)],
        'S': c.keys()
    }

    # Next positions
    n = [(sy, sx)]
    for y, x in n:
        # pprint(n)

        # Check all directions
        for dy, dx in dirs[p[y][x]]:
            ny = y + dy
            nx = x + dx
            # If not beyond the border
            if (ny>=0 and ny<h and
                nx>=0 and nx<w):
                # If not checked before
                if d[ny][nx] == -1:
                    # If connected to previous one
                    if p[ny][nx] in c[(dy,dx)]:
                        n.append((y+dy, x+dx))
                        d[y+dy][x+dx] = d[y][x] + 1


    #################### Part two ###########
    nests = [['.' for i in range(w)] for j in range(h)]
    checks = []
    for y in range(h):
        for x in [0, w-1]:
            if d[y][x] == -1:
                nests[y][x] = 'O'
                checks.append((y, x))
        for x in range(w):
            if d[y][x] >= 0:
                nests[y][x] = 'P'
    for x in range(w):
        for y in [0, h-1]:
            if d[y][x] == -1:
                nests[y][x] = 'O'
                checks.append((y, x))

    for y, x in checks:
        # Check all directions
        for dy, dx in c.keys():
            ny = y + dy
            nx = x + dx
            # If not beyond the border
            if (ny>=0 and ny<h and
                nx>=0 and nx<w):
                if nests[ny][nx] == '.':
                    nests[ny][nx] = 'O'
                    checks.append((ny, nx))


    for r in nests[::2]:
        # print(''.join(r[::2]))
        result += r[::2].count('.')

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
