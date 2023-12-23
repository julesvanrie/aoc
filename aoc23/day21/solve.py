import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint
from collections import deque
from numpy.polynomial.polynomial import polyfit, polyval


dirs = [
    (0, +1),
    (+1, 0),
    (0, -1),
    (-1, 0),
]

@BaseSolution.time_this
def solve_one(self, nb=64):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    field = [list(f) for f in input]

    even = 1 if (nb % 2) == 0 else 0

    # Find the start
    start = ()
    for y, r in enumerate(field):
        for x, c in enumerate(r):
            if c == 'S':
                start = (y, x, 0)
                field[y][x] = 0

    visited = {(start[0], start[1]): 0}

    result = even

    # Saving next spots to explore
    nexts = deque([start])
    while nexts:
        y, x, c = nexts.popleft()
        for dy, dx in dirs:
            ny = y + dy
            nx = x + dx
            # If we hit a rock
            if field[ny % h][nx % w] == '#':
                continue
            # If we haven't been here
            if (ny,nx) not in visited:
                visited[(ny,nx)] = c + 1
                if c % 2 == even:
                    result += 1
            # If we have been here before,
            # but needed more steps
            elif visited[(ny,nx)] > c+1:
                visited[(ny,nx)] = c+1
            else:
                continue
            # If we didn't run out of steps
            if c + 1 < nb:
                nexts.append((ny, nx, c+1))

    return result


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    h = len(input)
    x = [0, 1, 2]
    nb = list(map(lambda x: int(h/2) + h * x, x))
    y = list(map(self.solve_one, nb))
    coefs = polyfit(x, y, deg=2)
    nb_fields = (26501365 - int(h/2)) / h
    return int(polyval(nb_fields, coefs))


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
