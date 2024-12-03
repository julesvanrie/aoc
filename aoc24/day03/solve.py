import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint


mul_finder = re.compile(r"(mul\(\d+,\d+\))")

@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    result = 0
    for line in input:
        result += base_calc(line)
    return result


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    return calc(''.join(input), enabled=True)

def base_calc(input):
    result = 0
    for mul in mul_finder.findall(input):
            left, right = re.compile(r"(\d+)").findall(mul)
            result += int(left) * int(right)
    return result

def calc(input, enabled=True):
    enable = input.find("do()")
    disable = input.find("don't()")
    # If everything that follows should be calculated
    if (enabled and disable == -1):
        return base_calc(input)
    if enabled:
        start = 4 if enable == 0 else 0
        if disable == -1:
            result = calc(input[start:], enabled=True)
        else:
            result = calc(input[start:disable], enabled=True)
            result += calc(input[disable+7:], enabled=False)
        return result
    # If not enabled and no re-enabling afterwards
    if enable == -1:
        return 0
    return calc(input[enable+4:], enabled=True)


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
