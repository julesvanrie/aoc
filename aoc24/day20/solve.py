"""Pure Python. About 1.6 seconds for part 2

1. Calculate the base path. Return the total distance, the path and the grid with the distances instead of the dots.
2. For each point on the track that is still far enough from the end:
   - Calculate the potential cheats
   - Check that the cheat brings us to a farther point on the track
   - Calculate the gain and if high enough, result +1

To calculate the potential cheats: a basic for loop in both y and x in all directions, as long as the total is less than the maximum cheat time.
"""

import sys
from aocsolution.basesolution import BaseSolution

from itertools import product


dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))


@BaseSolution.time_this
def solve_one(self):
    return self.solve(100, 2)


@BaseSolution.time_this
def solve_two(self):
    return self.solve(100, 20)


def solve(self, target, max_cheat):
    input = self.get_data()
    grid = [list(row) for row in input]
    return cheat(grid, target, max_cheat)


def cheat(grid, target, max_cheat):
    # Calculate the base track
    base_dist, path, grid = get_base_track(grid)

    result = 0

    for y, x in path:
        # If we are too close to the target we can't make the necessary gain
        if base_dist - grid[y][x] >= target:
            # Find all the potential cheats at this point (different directions)
            # Each cheat will be a destination point (with y and x coords)
            for (cheat_y, cheat_x) in find_cheats(grid, y, x, max_cheat):
                # Calculate the time our cheat will take
                cheat_dist = abs(cheat_y - y) \
                           + abs(cheat_x - x)
                # Gain = new position - old position - cheat time)
                gain = grid[cheat_y][cheat_x] \
                     - grid[y][x] \
                     - cheat_dist
                if gain >= target:
                    result += 1

    return result


def get_base_track(grid):
    '''Calculates the base track and returns:
    - The total distance from start to end
    - The path from start to end
    - The grid with the base track distance instead of dots
    '''
    sy, sx, ey, ex = get_start_and_end(grid)
    grid[sy][sx] = 0
    y, x = sy, sx
    path = [(sy, sx)]
    while (y, x) != (ey, ex):
        for dy, dx in dirs:
            ny, nx = y + dy, x + dx
            if grid[ny][nx] in ['.', 'E']:
                grid[ny][nx] = grid[y][x] + 1
                y, x = ny, nx
                path.append((y, x))
                break

    return grid[ey][ex], path, grid


def get_start_and_end(grid):
    h = len(grid)
    w = len(grid[0])

    for y, x in product(range(h), range(w)):
        if grid[y][x] == 'S':
            sy = y
            sx = x
        elif grid[y][x] == 'E':
            ey = y
            ex = x

    return sy, sx, ey, ex


def find_cheats(grid, y, x, max_cheat):
    '''Finds all potential cheats at a given point and within the max_cheat time'''
    cheats = []
    for i, j in product(range(-max_cheat, max_cheat+1),
                        range(-max_cheat, max_cheat+1)):
        if abs(i) + abs(j) <= max_cheat:
            endy, endx = y + i, x + j
            # If we end up on the track
            if (0 < endy < len(grid) - 1 and
                0 < endx < len(grid[0]) - 1 and
                grid[endy][endx] != '#'
            ):
                cheat = (endy, endx)
                cheats.append(cheat)
    return cheats


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
