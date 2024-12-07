import sys
from aocsolution.basesolution import BaseSolution

from collections import defaultdict


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    self.grid = [[c for c in line] for line in input]
    self.directions = { '^': 0, '>': 1, 'v': 2, '<': 3 }
    self.visited = set()

    self.start = None
    for y in range(h):
        for x in range(w):
            if self.grid[y][x] not in ['.', '#']:
                self.start = (y, x, self.directions[self.grid[y][x]])
                self.grid[y][x] = '.'
                break
        if self.start:
            break

    y, x = (self.start[0], self.start[1])
    direction = self.start[2]

    while True:
        new_y, new_x = next_pos(y, x, direction)

        if new_y < 0 or new_x < 0 or new_y >= h or new_x >= w:
            break

        if self.grid[new_y][new_x] != '#':
            y = new_y
            x = new_x
        else:
            direction = (direction + 1) % 4

        self.visited.add((y, x))

    return len(self.visited)


@BaseSolution.time_this
def solve_two(self):
    result_two = 0

    h = len(self.grid)
    w = len(self.grid[0])

    for obstacle_y, obstacle_x in self.visited:
        # Can skip start and existing obstacles, but doesn't impact performance much
        # if (obstacle_y, obstacle_x) == (self.start[0], self.start[1]):
        #     continue
        # if self.grid[obstacle_y][obstacle_x] == '#':
        #     continue
        self.grid[obstacle_y][obstacle_x] = '#'
        visited = defaultdict(list)
        y, x, direction = (self.start[0], self.start[1], self.start[2])

        while True:
            new_y, new_x = next_pos(y, x, direction)

            if new_y < 0 or new_x < 0 or new_y >= h or new_x >= w:
                self.grid[obstacle_y][obstacle_x] = '.'
                break

            if self.grid[new_y][new_x] != '#':
                visited[(y, x)].append(direction)
                y = new_y
                x = new_x
            else:
                direction = (direction + 1) % 4

            if direction in visited[(y, x)]:
                result_two += 1
                self.grid[obstacle_y][obstacle_x] = '.'
                break

        self.grid[obstacle_y][obstacle_x] = '.'

    return result_two


def next_pos(y, x, direction):
    if direction == 0:
        return (y-1, x)
    elif direction == 1:
        return (y, x+1)
    elif direction == 2:
        return (y+1, x)
    elif direction == 3:
        return (y, x-1)


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
