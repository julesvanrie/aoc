import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint

vizs = {
    0: '>',
    1: 'v',
    2: '<',
    3: '^',
}

dirs = {
    0: (0,+1),
    1: (+1,0),
    2: (0,-1),
    3: (-1,0),
}

def deviate(direction, tile):
    if tile == '.':
        return [direction]
    if tile == '-':
        if direction in [0,2]:
            return [direction]
        else:
            return [0,2]
    if tile == '|':
        if direction in [1,3]:
            return [direction]
        else:
            return [1,3]
    if tile == '\\':
        if direction in [0,2]:
            return [(direction + 1) % 4]
        else:
            return [(direction - 1) % 4]
    if tile == '/':
        if direction in [0,2]:
            return [(direction - 1) % 4]
        else:
            return [(direction + 1) % 4]


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    initial = (0,0,0)
    return self.energize(input, initial)

def energize(self, input, initial):
    h = len(input)
    w = len(input[0])

    states = [[0 for x in range(w)] for y in range(h)]

    # viz = [[input[y][x] for x in range(w)] for y in range(h)]

    next_up = [initial]
    while next_up:
        y, x, d = next_up.pop()
        states[y][x] |= 2**d
        new = deviate(d, input[y][x])
        for dn in new:
            yn = y + dirs[dn][0]
            xn = x + dirs[dn][1]
            if yn >= h or yn < 0 or xn >= w or xn < 0:
                continue
            if not states[yn][xn] & 2**dn:
                next_up.append((yn,xn,dn))
            # if viz[yn][xn] == '.':
            #     viz[yn][xn] = vizs[dn]
            # print(state, tile, new_state)

    # for row in viz:
    #     print(''.join(t for t in row))

    result = sum(sum(1 for x in range(w) if states[y][x]) for y in range(h))

    return result


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    result = 0

    for y in range(h):
        result = max(result,
                     energize(self, input, (y,0,0)),
                     energize(self, input, (y,w-1,2))
                     )
    for x in range(w):
        result = max(result,
                     energize(self, input, (0,x,1)),
                     energize(self, input, (h-1,x,3))
                     )

    return result


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two
    energize = energize


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
