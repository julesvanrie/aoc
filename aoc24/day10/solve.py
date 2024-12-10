import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint
from itertools import product

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])
    ps = [[int(c) for c in row] for row in input]
    counts = [[set() for _ in range(w)] for _ in range(h)]
    visited = set()

    for sy, sx in product(range(h), range(w)):
        if ps[sy][sx] == 0:
            cand = {(sy, sx, 0)}
            while cand:
                c = cand.pop()
                visited.add((sy, sx, c))
                y, x, alt = c
                new_cand = []
                for d in directions:
                    ny = y + d[0]; nx = x + d[1]
                    if ny >= 0 and ny < h and nx >= 0 and nx < w:
                        nalt = ps[ny][nx]
                        if nalt - alt == 1:
                            new_cand.append((ny, nx, ps[ny][nx]))
                for nc in new_cand:
                    if nc[2] == 9:
                        counts[sy][sx].add((nc[0], nc[1]))
                    else:
                        if (sy, sx, nc) not in visited:
                            cand.add(nc)

    return sum(sum(len(counts[y][x]) for x in range(w)) for y in range(h))


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])
    ps = [[int(c) for c in row] for row in input]
    counts = [[set() for _ in range(w)] for _ in range(h)]
    visited = set()

    for sy, sx in product(range(h), range(w)):
        if ps[sy][sx] == 0:
            cand = {(sy, sx, 0, None)}
            while cand:
                c = cand.pop()
                visited.add((sy, sx, c))
                y, x, alt, _ = c
                new_cand = []
                for d in directions:
                    ny = y + d[0]; nx = x + d[1]
                    if ny >= 0 and ny < h and nx >= 0 and nx < w:
                        nalt = ps[ny][nx]
                        if nalt - alt == 1:
                            new_cand.append((ny, nx, ps[ny][nx], c))
                for nc in new_cand:
                    if nc[2] == 9:
                        counts[sy][sx].add((nc[0], nc[1], nc[3]))
                    else:
                        if (sy, sx, nc) not in visited:
                            cand.add(nc)

    return sum(sum(len(counts[y][x]) for x in range(w)) for y in range(h))

class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
