import sys
from aocsolution.basesolution import BaseSolution

from copy import deepcopy


def find_mirror(pattern):
    result = []
    for i in range(1,len(pattern)):
        candidate = True
        max_mirror = min(i, (len(pattern)-i))
        for j in range(max_mirror):
            if pattern[i-j-1] != pattern[i+j]:
                candidate = False
                break
        if candidate:
            result += [i]
    if not result:
        return [0]
    return result


def transpose(pattern):
    h = len(pattern)
    w = len(pattern[0])
    return [''.join([pattern[y][x] for y in range(h)]) for x in range(w)]


@BaseSolution.time_this
def solve_one(self):
    result = 0
    input = self.get_data(split=False).split("\n\n")

    for pattern in input[:]:
        pattern = pattern.split()

        result += 100 * find_mirror(pattern)[0]
        result += find_mirror(transpose(pattern))[0]

    return result


@BaseSolution.time_this
def solve_two(self):
    result = 0
    input = self.get_data(split=False).split("\n\n")

    for pattern in input[:]:
        pattern = [[c for c in r] for r in pattern.split()]
        intermed = 0
        for y in range(len(pattern)):
            for x in range(len(pattern[0])):
                new = deepcopy(pattern)
                new[y][x] = '.' if new[y][x] == '#' else '#'
                new = [''.join(n) for n in new]

                h_new = find_mirror(new)
                h_pattern = find_mirror(pattern)[0]
                v_new = find_mirror(transpose(new))
                v_pattern = find_mirror(transpose(pattern))[0]
                if h_new[0]:
                    if len(h_new) == 1 and h_new[0] != h_pattern:
                        intermed += 100 * h_new[0]
                    else:
                        intermed += 100 * (sum(h_new) - h_pattern)
                if v_new[0]:
                    if len(v_new) == 1 and v_new[0] != v_pattern:
                        intermed += v_new[0]
                    else:
                        intermed += sum(v_new) - v_pattern
                if intermed:
                    break
            if intermed:
                break
        result += intermed

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
