import sys
from aocsolution.basesolution import BaseSolution


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data(split=False)

    key_locks = input.split('\n\n')

    keys = {}
    locks = {}

    for i, kl in enumerate(key_locks):
        lines = kl.split('\n')
        lock = all(c == '#' for c in lines[0])
        if lock:
            depths = []
            for x in range(5):
                for y in range(7):
                    if lines[y][x] == '.':
                        depths.append(y-1)
                        break
            locks[i] = depths
        else:
            depths = []
            for x in range(5):
                for y in range(7):
                    if lines[y][x] == '#':
                        depths.append(y-1)
                        break
            keys[i] = depths

    result = 0

    for k, kd in keys.items():
        for l, ld in locks.items():
            ok = True
            for x in range(5):
                if kd[x] < ld[x]:
                    ok = False
                    break
            if ok:
                result += 1

    return result


class Solution(BaseSolution):
    solve_one = solve_one


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
