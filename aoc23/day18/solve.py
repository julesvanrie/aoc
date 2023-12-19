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
def solve_one(self):
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


@BaseSolution.time_this
def solve_twos(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    digging = [r.split(' ') for r in input]
    digging = [(dirs[r[0]], int(r[1])) for r in digging]

    points = {}

    y, x = (0, 0)
    for (dy, dx), l in digging:
        if y not in points.keys():
            points[y] =  [x] #{x: (dy, dx, l)}
        else:
            points[y].append(x) #[x] = (dy, dx, l)
        y, x = (y + l*dy, x + l*dx)

    result = 0
    yprev = min(points.keys())
    ys = sorted(points.keys())
    for i, y in enumerate(ys[:-1]):
        print(result, y)
        x = sorted(points[y])
        ny = ys[i+1]
        if len(x) == 2:
            if i == 0:
                result += (ys[i+1] - y) * (x[1] - x[0] + 1)
                prevx = x
            else:
                py = ys[i-1]
                if x[0] == prevx[0]:
                    result += (ny - y) * (prevx[1] - x[1] + 1)
                    prevx = x
                elif x[1] ==  prevx[1]:
                    result += (ny - y) * (prevx[0] - x[0] + 1)
                    prevx = x
                result += x[1] - x[0]
        elif len(x) == 4:
            print("We got 4", x, prevx)
            if (x[0] == prevx[0]):
                print("here")
                result += (ny - y) * (x[3] - x[1] + 1)
                result += x[1] - x[0]
                prevx = x
            elif (x[0] <= prevx[0]):
                result += (ny - y) * (x[2] - x[0] + 1)
                result += x[3] - x[2]
                prevx = x
            else:
                print("que", x)

        else:
            print("strange", x)
        # result += (y-yprev) * points[y]
    lastx = sorted(points[ys[-1]])
    result += lastx[1] - lastx[0] + 1

        # yprev = y


    # ymax = max(p[0] for p in points)
    # ymin = min(p[0] for p in points)
    # xmax = max(p[1] for p in points)
    # xmin = min(p[1] for p in points)

    return result

@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()

    digging = [r.split(' ') for r in input]
    digging = [(dirs[r[0]], int(r[1])) for r in digging]


    # Find the points for part 1
    y, x = (0, 0)
    points = []
    for (dy, dx), l in digging:
        y = y + dy*l
        x = x + dx*l
        points.append((y,x))

    # Find the points for part 2
    ds = [
        (0, -1),
        (+1, 0),
        (0, +1),
        (-1, 0),
    ]
    digging = [r.split(' ')[-1].strip('()#') for r in input]
    digging = [(ds[int(r[-1])], int(r[:-1],16)) for r in digging]

    y, x = (0, 0)
    points = []
    for (dy, dx), l in digging:
        y = y + dy*l
        x = x + dx*l
        points.append((y,x))


    # Shoelace
    result = 0
    for i in range(0, len(points)-1):
        result += (points[i][1] * points[i+1][0]
                     - points[i][0] * points[i+1][1])
        print(i, result)

    # Pick's theorem
    perimeter = sum(l for _, l in digging) / 2 + 1

    return abs(result) / 2 + perimeter


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
