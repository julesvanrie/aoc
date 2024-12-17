import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint
from itertools import product

dirs = ((0,1), (1,0), (0,-1), (-1,0))

@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    start = (h-2, 1, 0)
    dest = (1, w-2)

    visited = [start]
    candidates = {start: 0}

    y, x, dir = start

    while (y, x) != dest:
        y, x, dir = sorted(candidates, key=candidates.get, reverse=False)[0]
        cost = candidates.pop((y, x, dir))

        for dd, (dy, dx) in enumerate(dirs):
            if input[y+dy][x+dx] != '#' and (dd == dir or (dd - dir) % 2 != 0):
                new_cost = cost + 1 + (1000 if dd != dir else 0)
                if (y+dy, x+dx, dd) not in visited:
                    if candidates.get((y+dy, x+dx, dd), 2**63) > new_cost:
                        candidates[(y+dy, x+dx, dd)] = new_cost
        visited.append((y, x, dir))

    return cost


@BaseSolution.time_this
def solve_two(self, target):
    """target is the result of part 1"""
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    start = (h-2, 1, 0)
    dest = (1, w-2)

    y, x, dir = start

    paths = {(start,): 0}
    best_paths = set()
    visited = {start: 0}

    while paths:
        new_paths = {}
        while paths:
            path, cost = paths.popitem()
            y, x, dir = path[-1]
            for dd, (dy, dx) in enumerate(dirs):
                if input[y+dy][x+dx] != '#' and (dd == dir or (dd - dir) % 2 != 0):
                    penalty = 1000 if (y != 1 and dd != 3) else 0
                    penalty = 1000 if (x != w-2 and dd != 0) else 0
                    penalty = 2000 if dd == 1 else 0
                    penalty = 2000 if dd == 2 else 0
                    penalty += y - 2 + w - x - 2

                    if (new_cost := cost + 1 + (1000 if dd != dir else 0)) + penalty <= target:
                        if visited.get((y+dy, x+dx, dd), 2**63) >= new_cost:
                            visited[(y+dy, x+dx, dd)] = new_cost
                            the_path = path + ((y+dy, x+dx, dd),)
                            if (y+dy, x+dx) == dest and new_cost == target:
                                best_paths.add(path + ((y+dy, x+dx, dd),))
                            else:
                                new_paths[the_path] = new_cost
        paths = new_paths

    hotspots = [[False for _ in range(w)] for _ in range(h)]

    for path in best_paths:
        for point in path:
            hotspots[point[0]][point[1]] = True

    return sum(sum(row) for row in hotspots)


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    sol_one = solution.solve_one()
    print("The result for part 1 is:", sol_one)
    print("The result for part 2 is:", solution.solve_two(target=sol_one))
