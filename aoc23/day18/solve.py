import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint
from collections import defaultdict


dirs = {
    'L': (0, -1),
    'D': (+1, 0),
    'R': (0, +1),
    'U': (-1, 0),
}

@BaseSolution.time_this
def solve_one_old(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    digging = [r.split(' ') for r in input]
    digging = [(dirs[r[0]], int(r[1])) for r in digging]

    digged = {}

    pos = (0, 0)
    digged[pos] = '#'
    for (dy, dx), l in digging:
        for i in range(1,l+1):
            digged[(pos[0] + i*dy, pos[1] + i*dx)] = '#'
        pos = (pos[0] +  l*dy, pos[1] + l*dx)

    result = 0

    ymax = max(k[0] for k in digged.keys())
    ymin = min(k[0] for k in digged.keys())
    xmax = max(k[1] for k in digged.keys())
    xmin = min(k[1] for k in digged.keys())
    pprint(digged.keys())

    check = []
    for y in range(ymin-1, ymax+1):
        digged[(y, xmin-1)] = 'o'
        check.append((y, xmin-1))
        digged[(y, xmax+1)] = 'o'
        check.append((y, xmax+1))
        for x in range(xmin-1, xmax+2):
            digged[(ymin-1, x)] = 'o'
            check.append((ymin-1, x))
            digged[(ymax+1, x)] = 'o'
            check.append((ymax+1, x))
            print(digged.get((y,x), '.'), end='')
        print()

    # Points to check: neighbours connected to this point are outside if not on the loop
    for y, x in check:
        # Check all directions
        for dy, dx in dirs.values():
            ny = y + dy
            nx = x + dx
            if (
                ny>=ymin-1 and ny<ymax+1 and    # If not beyond the border
                nx>=xmin-1 and nx<xmax+1 and    #
                digged.get((ny, nx), '.') == '.'  #    not checked before, not on the loop
            ):
                digged[(ny, nx)] = 'o'  # Point is outside
                check.append((ny, nx))    # Add point to points to check next

    for y in range(ymin-1, ymax+1):
        for x in range(xmin-1, xmax+2):
            v = digged.get((y,x), '.')
            print(v, end='')
            result += 1 if v != 'o' else 0
        print()

    return result


def shoelace(digging):
    y, x = (0, 0)
    points = []
    for (dy, dx), l in digging:
        (y, x) = (y + dy*l, x + dx*l)
        points.append((y,x))

    shoelace = sum(points[i][1] * points[i+1][0]
                 - points[i][0] * points[i+1][1]
                   for i in range(0, len(points)-1))

    picks_perimeter = sum(l for _, l in digging) / 2 + 1

    return int(abs(shoelace) / 2 + picks_perimeter)


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()

    digging = [r.split(' ') for r in input]
    digging = [(dirs[r[0]], int(r[1])) for r in digging]

    return shoelace(digging)


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()

    ds = list(dirs.values())

    digging = [r.split(' ')[-1].strip('()#') for r in input]
    digging = [(ds[int(r[-1])], int(r[:-1],16)) for r in digging]

    return shoelace(digging)

class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
