import sys
from aocsolution.basesolution import BaseSolution

import math
from collections import deque

@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    directions = deque([0 if inp == 'L' else 1 for inp in input[0]])
    locations = {inp.split(" = ")[0]:
                [loc.strip("()") for loc in inp.split(" = ")[1].split(", ")]
                 for inp in input[2:]}

    steps = 0
    loc = 'AAA'
    while loc != 'ZZZ':
        dir = directions.popleft()
        loc = locations[loc][dir]
        directions.append(dir)
        steps += 1

    return steps


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    locations = {inp.split(" = ")[0]:
                [loc.strip("()") for loc in inp.split(" = ")[1].split(", ")]
                 for inp in input[2:]}

    locs = [loc for loc in locations.keys() if loc.endswith('A')]
    times_Z_to_Z = []
    for loc in locs:
        steps = 0
        directions = deque([0 if inp == 'L' else 1 for inp in input[0]])
        while not loc.endswith('Z') or steps == 0:
            dir = directions.popleft()
            loc = locations[loc][dir]
            directions.append(dir)
            steps += 1
        times_Z_to_Z.append(steps)

    return math.lcm(*times_Z_to_Z)


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
