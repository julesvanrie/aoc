import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint


@BaseSolution.time_this
def solve_one(self):
    return self.solve()[0]

@BaseSolution.time_this
def solve_two(self):
    return self.solve()[1]

def solve(self):
    input = self.get_data()
    result_one = 0
    result_two = 0
    for line in input:
        numbers = [int(x) for x in line.split(' ')]
        if is_safe(numbers):
            result_one += 1
        if can_be_made_safe(numbers):
            result_two += 1

    return result_one, result_two

def is_safe(numbers):
    incr = numbers[-1] > numbers[0]
    for i in range(len(numbers)-1):
        if numbers[i+1] == numbers[i]:
            return False
        if abs(numbers[i+1] - numbers[i]) > 3:
            return False
        if (numbers[i+1] > numbers[i]) != incr:
            return False
    return True

def can_be_made_safe(numbers):
    for i in range(len(numbers)):
        if is_safe(numbers[:i] + numbers[i+1:]):
            return True
    return False


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
