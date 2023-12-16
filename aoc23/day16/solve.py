import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint

viz = {
    (0,+1): '>',
    (0,-1): '<',
    (+1,0): 'v',
    (-1,0): '^',
}

def deviate(direction, tile):
    if tile == '.':
        return [direction]
    if tile == '-':
        if direction[1]:
            return [direction]
        else:
            return [(0,+1),(0,-1)]
    if tile == '|':
        if direction[0]:
            return [direction]
        else:
            return [(+1,0),(-1,0)]
    if tile == '\\':
        return [(direction[1], direction[0])]
    if tile == '/':
        return [(-direction[1], -direction[0])]


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    initial = ((0,0),(0,+1))
    return self.energize(input, initial)

def energize(self, input, initial):
    h = len(input)
    w = len(input[0])

    states = [initial]

    tiles = [[input[y][x] for x in range(w)] for y in range(h)]


    for state in states:
        # breakpoint()
        y = state[0][0]
        x = state[0][1]
        tile = input[y][x]
        new = deviate(state[1], tile)
        for n in new:
            yn = y + n[0]
            xn = x + n[1]
            if yn >= h or yn < 0 or xn >= w or xn < 0:
                continue
            new_state = ((yn,xn), n)
            if tiles[yn][xn] == '.':
                tiles[yn][xn] = viz[n]
            # print(state, tile, new_state)
            if new_state not in states:
                states.append(new_state)

    # for row in tiles:
    #     print(''.join(t for t in row))

    result = len(set(state[0] for state in states))

    return result


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    potential = []

    for y in range(h):
        for x in range(w):
            dirs = []
            if y == 0:
                dirs.append((+1,0))
            if y == h-1:
                dirs.append((-1,0))
            if x == 0:
                dirs.append((0,+1))
            if x == w-1:
                dirs.append((0,-1))

            for d in dirs:
                initial = ((y,x),d)
                print(initial)
                potential.append(energize(self, input, initial))


    result = max(potential)

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
