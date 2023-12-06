import sys
from aocsolution.basesolution import BaseSolution

import re

@BaseSolution.time_this
def solve_one(self):
    result = 1
    input = self.get_data()
    times = re.findall(r"\d+", input[0])
    distances = re.findall(r"\d+", input[1])

    def ways(time, distance):
        # speed = t
        # distance = (time - t) * speed
        # distance = t * distance
        #          = -t**2 + t*time
        #  t**2 - t*time + distance = 0
        a = 1;  b = -time; c = distance
        D = b**2 - 4*a*c
        sol1 = (-b - D**0.5) / 2 / a
        sol2 = (-b + D**0.5) / 2 / a
        sol1int = int(sol1)+1 # if int(sol1) < sol1 else int(sol1)-1
        sol2int = int(sol2) if int(sol2) < sol2 else int(sol2)-1
        span = sol2int - sol1int + 1
        # print(sol1, sol2, sol1int, sol2int, span)
        return span

    for t, d in zip(times, distances):
        result *= ways(int(t), int(d))
    return result


@BaseSolution.time_this
def solve_two(self):
    # result = 1
    input = self.get_data()
    times = ''.join(re.findall(r"\d+", input[0]))
    distances = ''.join(re.findall(r"\d+", input[1]))

    def ways(time, distance):
        # speed = t
        # distance = (time - t) * speed
        # distance = t * distance
        #          = -t**2 + t*time
        #  t**2 - t*time + distance = 0
        a = 1;  b = -time; c = distance
        D = b**2 - 4*a*c
        sol1 = (-b - D**0.5) / 2 / a
        sol2 = (-b + D**0.5) / 2 / a
        sol1int = int(sol1)+1 # if int(sol1) < sol1 else int(sol1)-1
        sol2int = int(sol2) if int(sol2) < sol2 else int(sol2)-1
        span = sol2int - sol1int + 1
        print(sol1, sol2, sol1int, sol2int, span)
        return span

    result = ways(int(times), int(distances))
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
