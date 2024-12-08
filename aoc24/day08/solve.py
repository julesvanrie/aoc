import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint
from itertools import product
from collections import defaultdict

@BaseSolution.time_this
def solve_one(self):
    return self.solve(multi=False)


@BaseSolution.time_this
def solve_two(self):
    return self.solve(multi=True)


def solve(self, multi=True):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    antennas = defaultdict(list)
    antinodes = [[0 for _ in range(w)] for _ in range(h)]

    for (y, x) in product(range(h), range(w)):
        if (antenna := input[y][x]) not in ['.', '#']:
            antennas[antenna].append((y, x))

    for antenna in antennas.values():
        for (y_l, x_l) in antenna:
            for (y_r, x_r) in antenna:
                if (y_l, x_l) == (y_r, x_r):
                    continue
                for i in range(0 if multi else 2, max(h,w) if multi else 3):
                    y_a = y_l - i * (y_l - y_r)
                    x_a = x_l - i * (x_l - x_r)
                    if y_a < h and x_a < w and y_a >= 0 and x_a >= 0:
                        antinodes[y_a][x_a] = 1

    return sum(sum(row) for row in antinodes)


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two
    solve = solve


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
