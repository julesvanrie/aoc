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
    0: (0,+1), # East
    1: (+1,0), # South
    2: (0,-1), # West
    3: (-1,0), # South
}

def deviate(d, tile):
    if tile == '-' and d in [1,3]:
        return [0,2]
    if tile == '|' and d in [0,2]:
        return [1,3]
    if tile == '\\':
        return [(d - 1) % 4] if d % 2 else [(d + 1) % 4]
    if tile == '/':
        return [(d + 1) % 4] if d % 2 else [(d - 1) % 4]
    return [d]


def energize(self, input, initial):
    h = len(input)
    w = len(input[0])

    # Create a states array with a binary representation of directions
    states = [[0 for x in range(w)] for y in range(h)]
    # viz = [[input[y][x] for x in range(w)] for y in range(h)]

    next_up = [initial]
    while next_up:
        y, x, d = next_up.pop()
        # Bitwise adding direction to the state
        states[y][x] |= 2**d
        new = deviate(d, input[y][x])
        for dn in new:
            yn = y + dirs[dn][0]
            xn = x + dirs[dn][1]
            if not (
                yn >= h or yn < 0           # Vertical out of bounds
                or xn >= w or xn < 0        # Horizontal out of bounds
                or states[yn][xn] & 2**dn   # Already been here
            ):
                next_up.append((yn,xn,dn))
            # if viz[yn][xn] == '.':
            #     viz[yn][xn] = vizs[dn]
            # print(state, tile, new_state)

    # for row in viz:
    #     print(''.join(t for t in row))

    return sum(sum(1 for x in range(w) if states[y][x]) for y in range(h))


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    initial = (0,0,0)
    return self.energize(input, initial)


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
