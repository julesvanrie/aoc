import sys
from aocsolution.basesolution import BaseSolution

from functools import cache


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data(split=False).split(" ")

    tmp = input
    for _ in range(25):
        new_tmp = []
        for stone in tmp:
            if stone == '0':
                new_tmp.append('1')
            elif (length := len(stone)) % 2 == 0:
                if length > 1:
                    new_tmp.extend([
                        str(int(stone[:length//2])),
                        str(int(stone[length//2:]))
                    ])
                else:
                    new_tmp.append(str(int(stone) * 2024))
            else:
                new_tmp.append(str(int(stone) * 2024))
        tmp = new_tmp

    return len(tmp)


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data(split=False).split(" ")

    return sum(get_count(stone, 75) for stone in input)

@cache
def get_count(stone, i):
    if i == 0:
        return 1
    if stone == '0':
        return get_count('1', i-1)
    if (length := len(stone)) % 2 == 0:
        return get_count(str(stone[:length//2]), i-1) \
                + get_count(str(int(stone[length//2:])), i-1)
    return get_count(str(int(stone) * 2024), i-1)


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
