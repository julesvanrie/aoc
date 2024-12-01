import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint


@BaseSolution.time_this
def solve(self):
    input = self.get_data()
    lefties = []
    righties = []

    for line in input:
        left, right = line.split('   ')
        lefties.append(int(left))
        righties.append(int(right))

    result_one = 0
    result_two = 0
    for left, right in zip(sorted(lefties), sorted(righties)):
        result_one += abs(right - left)
        result_two += left * len([
            right for right in righties if right == left
        ])

    return result_one, result_two


class Solution(BaseSolution):
    solve = solve

if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution_one, solution_two = Solution(test=test).solve()
    print("The result for part 1 is:", solution_one)
    print("The result for part 2 is:", solution_two)
