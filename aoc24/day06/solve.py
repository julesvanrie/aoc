import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint
from collections import defaultdict


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    grid = [[c for c in line] for line in input]
    directions = { '^': 0, '>': 1, 'v': 2, '<': 3 }
    visited = set()

    start = None
    for y in range(h):
        for x in range(w):
            if grid[y][x] not in ['.', '#']:
                start = (y, x, directions[grid[y][x]])
                grid[y][x] = '.'
                break
        if start:
            break

    y, x = (start[0], start[1])
    direction = start[2]

    while True:
        if direction == 0:
            new_y, new_x = (y-1, x)
        elif direction == 1:
            new_y, new_x = (y, x+1)
        elif direction == 2:
            new_y, new_x = (y+1, x)
        elif direction == 3:
            new_y, new_x = (y, x-1)

        if new_y < 0 or new_x < 0 or new_y >= h or new_x >= w:
            break

        if grid[new_y][new_x] != '#':
            y = new_y
            x = new_x
        else:
            direction = (direction + 1) % 4

        visited.add((y, x))

    return len(visited)


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    grid = [[c for c in line] for line in input]
    directions = { '^': 0, '>': 1, 'v': 2, '<': 3 }

    result_two = 0

    start = None
    for y in range(h):
        for x in range(w):
            if grid[y][x] not in ['.', '#']:
                start = (y, x, directions[grid[y][x]])
                grid[y][x] = '.'
                break
        if start:
            break


    grid = [[c for c in line] for line in input]

    for block_y in range(h):
        for block_x in range(w):
            if (block_y, block_x) == (start[0], start[1]):
                continue
            if grid[block_y][block_x] == '#':
                continue
            grid[block_y][block_x] = '#'
            visited = defaultdict(list)
            y, x = (start[0], start[1])
            direction = start[2]
            while True:
                if direction == 0:
                    new_y, new_x = (y-1, x)
                elif direction == 1:
                    new_y, new_x = (y, x+1)
                elif direction == 2:
                    new_y, new_x = (y+1, x)
                elif direction == 3:
                    new_y, new_x = (y, x-1)

                if new_y < 0 or new_x < 0 or new_y >= h or new_x >= w:
                    grid[block_y][block_x] = '.'
                    break

                if grid[new_y][new_x] != '#':
                    visited[(y, x)].append(direction)
                    y = new_y
                    x = new_x
                else:
                    direction = (direction + 1) % 4

                if direction in visited[(y, x)]:
                    result_two += 1
                    grid[block_y][block_x] = '.'
                    break
            grid[block_y][block_x] = '.'


    return result_two


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
