import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    h = len(input)

    result = 0

    for line in input:
        test, numbers = line.split(': ')
        test = int(test)
        numbers = list(map(int, numbers.split(' ')))

        options = calc_one(numbers)

        # print(options)

        if test in options:
            result += test


    return result

def calc_one(numbers):
    if len(numbers) == 2:
        return [
            numbers[0] + numbers[1],
            numbers[0] * numbers[1]
            ]
    else:
        return calc_one([numbers[0] + numbers[1]] + numbers[2:]) + \
               calc_one([numbers[0] * numbers[1]] + numbers[2:])

def calc_two(numbers):
    if len(numbers) == 2:
        return [
            numbers[0] + numbers[1],
            numbers[0] * numbers[1],
            numbers[0] * (10 ** (len(str(numbers[1])))) + numbers[1]
            ]
    else:
        return calc_one([numbers[0] + numbers[1]] + numbers[2:]) + \
               calc_one([numbers[0] * numbers[1]] + numbers[2:]) + \
               calc_one([numbers[0] * (10 ** (len(str(numbers[1])))) + numbers[1]] + numbers[2:])

@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    h = len(input)

    result = 0

    for line in input:
        test, numbers = line.split(': ')
        test = int(test)
        numbers = list(map(int, numbers.split(' ')))

        options = calc_two(numbers)

        # print(options)

        if test in options:
            result += test


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
