import sys
from aocsolution.basesolution import BaseSolution

import re

@BaseSolution.time_this
def solve_one(self):
    return self.solve_two()[0]


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    first = []
    last = []
    for history in input:
        diff_levels = []
        diff = [int(h) for h in history.split()]
        while set(diff) != {0,}:
            diff_levels.append(diff)
            diff = [diff[i+1] - diff[i] for i in range(len(diff)-1)]
        for i in range(len(diff_levels)-1,0,-1):
            diff_levels[i-1].append(diff_levels[i-1][-1]+diff_levels[i][-1])
            diff_levels[i-1].insert(0, diff_levels[i-1][0]-diff_levels[i][0])
        last.append(diff_levels[0][-1])
        first.append(diff_levels[0][0])
    return sum(last), sum(first)


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
