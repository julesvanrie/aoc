import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy

@BaseSolution.time_this
def solve_one(self):
    result = 0
    input = self.get_data()

    h = len(input)
    w = len(input[0])
    cols = ['#' + ''.join([input[y][x] for y in range(h)])
            for x in range(w)]

    for col in cols:
        rocks = [r.start() for r in re.finditer(r"O", col)]
        cubes = [r.start() for r in re.finditer(r"#", col)]
        new = []
        for j in range(len(cubes)):
            pos = cubes[j]
            for i in range(len(rocks)):
                i < len(rocks)
                if(
                    rocks[i] > cubes[j]
                    and ((j < len(cubes) -1 and rocks[i] < cubes[j+1])
                         or
                         (j == len(cubes)-1 and rocks[i] < h + 1))
                ):
                    pos += 1
                    new.append(pos)
        result += sum(h + 1 - n for n in new)

    return result


@BaseSolution.time_this
def solve_two(self):
    result = 0
    input = self.get_data()

    old_states = {0: ''.join(input) }

    iter = 0
    cycles = 1_000_000_000
    while iter < cycles*4 + 0:
        h = len(input)
        w = len(input[0])
        # rows = ['#' + input[y] + '#' for y in range(h)]
        cols = ['#' + ''.join([input[y][x] for y in range(h)]) + '#'
                for x in range(w)]
        all_cubes = [[r.start() for r in re.finditer(r"#", cols[x])] for x in range(h)]
        all_rocks = [[r.start() for r in re.finditer(r"O", cols[x])] for x in range(h)]

        for x in range(len(cols)):
            rocks = all_rocks[x]
            cubes = all_cubes[x]
            all_rocks[x] = []
            for j in range(len(cubes)-1):
                pos = cubes[j]
                for i in range(len(rocks)):
                    i < len(rocks)
                    if(
                        rocks[i] > cubes[j]
                        and rocks[i] < cubes[j+1]
                    ):
                        pos += 1
                        all_rocks[x].append(pos)
        new_pos = [['#' if y+1 in all_cubes[x] else 'O' if y+1 in all_rocks[x] else '.' for x in range(w)] for y in range(h)]
        # print(iter, end='\n')
        # viz = deepcopy(new_pos)
        # for m in range(iter % 4):
        #     viz = counter_clock_wise(viz)
        # for r in viz:
        #     print(''.join(r))
        input = clock_wise(new_pos)
        new_state = ''.join(''.join(row) for row in input)
        if new_state in old_states.values():
            indexes = [idx for idx, state in old_states.items() if state == new_state]
            for idx in indexes:
                skips = iter - idx
                if iter + skips < 4_000_000_000:
                    print(iter, "skipping", skips)
                    iter += skips
                    break
            old_states[iter] = new_state
        else:
            old_states[iter] = new_state
        iter += 1

    iter -= 1
    viz = deepcopy(new_pos)
    for m in range(iter % 4):
        viz = counter_clock_wise(viz)
    # for r in viz:
    #     print(''.join(r))
    cols = ['#' + ''.join([viz[y][x] for y in range(h)]) + '#'
                for x in range(w)]
    all_rocks = [[r.start() for r in re.finditer(r"O", cols[x])] for x in range(h)]
    result = sum(sum(h + 1 - r for r in all_rocks[x]) for x in range(w))

    return result

def clock_wise(old):
    h = len(old)
    w = len(old[0])
    return [''.join(old[y][x] for y in range(h-1,-1,-1)) for x in range(w)] # clock

def counter_clock_wise(old):
    h = len(old)
    w = len(old[0])
    return [''.join(old[y][w-1-x] for y in range(h)) for x in range(w)]


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
