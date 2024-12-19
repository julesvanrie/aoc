import sys
from aocsolution.basesolution import BaseSolution

from functools import cache


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()

    self.available = input[0].split(", ")
    self.desired = input[2:]

    result = 0

    for design in self.desired:
        if self.is_valid(design):
            result += 1

    return result

@cache
def is_valid(self, design):
    valid = False
    for towel in self.available:
        if design == towel:
            return True
        elif design.startswith(towel):
            valid = self.is_valid(design[len(towel):])
        if valid:
            return True
    return False

@cache
def get_valids(self, design, so_far):
    nb_valids = so_far
    for towel in self.available:
        if design == towel:
            nb_valids += 1
        elif design.startswith(towel):
            nb_valids += (
                self.get_valids(design[len(towel):], so_far)
            )
    return nb_valids

@BaseSolution.time_this
def solve_two(self):
    result = 0

    for design in self.desired:
        result += (self.get_valids(design, 0))

    return result


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two
    is_valid = is_valid
    get_valids = get_valids


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
