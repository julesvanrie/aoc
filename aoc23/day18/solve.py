import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    result = 0

    input = [[[[(142-y)+(142-x)]*4]*4 for x in range(142)] for y in range(142)]
    for kl in range(142*142):
        min = 2**63
        miny = None
        minx = None
        mind = None
        minc = None
        for y in range(142):
            for x in range(142):
                for d in range(4):
                    for c in range(4):
                        # penalized_distance = distances[y][x][d][c] #+ prev_dir_counts[y][x][d]
                        if (min > input[y][x][d][c]):# + prev_dir_counts[y][x][d]):
                            min = input[y][x][d][c]
                            miny = y
                            minx = x
    return miny, minx

    return result


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    result = 0

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
