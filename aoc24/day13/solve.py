import sys
from aocsolution.basesolution import BaseSolution

import re


def solve(self, part=1):
    input = self.get_data(split=False)

    result = 0

    pattern = re.compile(r"(\d+)")
    machines = pattern.findall(input)
    for i in range(len(machines) // 6):
        (ax, ay, bx, by, tx, ty) = [int(machines[6*i+j]) for j in range(6)]
        tx += (part - 1) * 10000000000000
        ty += (part - 1) * 10000000000000

        """
        Base equations
          ax * a + bx * b = tx
          ay * a + by * b = ty

        Multiply with by and bx respectively
          by * ax * a + by * bx * b = by * tx
          bx * ay * a + bx * by * b = bx * ty

        Subtract the two equations
          by * tx - bx * ty = by * ax * a - bx * ay * a
        """

        # Extract a
        a = (by * tx - bx * ty) / (by * ax - bx * ay)

        # Then calculate b
        b = (tx - ax * a) / bx

        if (int(a) == a and int(b) == b
            and a >= 0 and b >= 0):
            result += int(a) * 3 + int(b)

    return result


@BaseSolution.time_this
def solve_one(self):
    return self.solve(1)


@BaseSolution.time_this
def solve_two(self):
    return self.solve(2)


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
