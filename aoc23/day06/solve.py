import sys
from aocsolution.basesolution import BaseSolution

import re

def ways(time, distance):
    # distance = (time - t) * speed
    #          = (time - t) * t
    #          = time*t - t*t
    #  t**2 - t*time + distance = 0
    a = 1;  b = -time; c = distance
    D = b**2 - 4*a*c
    sol1 = (-b - D**0.5) / 2 / a
    sol2 = (-b + D**0.5) / 2 / a
    sol1int = int(sol1) + 1
    sol2int = int(sol2) if int(sol2) < sol2 else int(sol2)-1
    span = sol2int - sol1int + 1
    return span

@BaseSolution.time_this
def solve_one(self):
    return self.solve_two()[0]


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    times = re.findall(r"\d+", input[0])
    distances = re.findall(r"\d+", input[1])

    # Part one
    result_one = 1
    for t, d in zip(times, distances):
        result_one *= ways(int(t), int(d))

    # Part two
    time_two = int(''.join(times))
    distance_two = int(''.join(distances))
    result_two = ways(time_two, distance_two)
    return result_one, result_two


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two()[1])
