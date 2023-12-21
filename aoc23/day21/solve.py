import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint
from collections import deque


dirs = [
    (0, +1),
    (+1, 0),
    (0, -1),
    (-1, 0),
]

@BaseSolution.time_this
def solve_ones(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    nb = 64 if h > 100 else 6

    field = ['#'*w] + input + ['#'*w]
    field = ['#' + f + '#' for f in field]
    field = [list(f) for f in field]

    # pprint(field)

    start = ()
    for y, r in enumerate(field):
        for x, c in enumerate(r):
            if c == 'S':
                start = (y,x)

    states = deque([(start[0], start[1], 0)])

    result = 0

    visited = []

    # for y, x, c in states:
    while states:
        y, x, c = states.popleft()
        visited.append((y, x, c))
        for dy, dx in dirs:
            ny = y + dy
            nx = x + dx
            if (ny, nx, c+1) not in visited and field[ny][nx] != '#':
                if c+1 == nb:# and field[ny][nx] != 'O':
                    result += 1
                    print(result, end='\r')
                    field[ny][nx] = 'O'
                    visited.append((ny, nx, c+1))
                else:
                    states.appendleft((ny, nx, c+1))



    # pprint([''.join(f) for f in field])

    return result

def solve_one(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    # Number of steps (real or test)
    nb = 64 if h > 100 else 6

    # Adding some # around as padding
    # (removes the need to check boundaries)
    field = ['#'*w] + input + ['#'*w]
    field = ['#' + f + '#' for f in field]
    field = [list(f) for f in field]

    # Find the start
    start = ()
    for y, r in enumerate(field):
        for x, c in enumerate(r):
            if c == 'S':
                start = (y, x, 0)
                field[y][x] = 0

    result = 1

    # Saving next spots to explore
    nexts = deque([start])
    while nexts:
        y, x, c = nexts.popleft()
        for dy, dx in dirs:
            ny = y + dy
            nx = x + dx
            # If we hit a rock
            if field[ny][nx] == '#':
                continue
            # If we haven't been here
            if field[ny][nx] == '.':
                field[ny][nx] = c+1
                if c % 2:
                    result += 1
            # If we have been here before,
            # but needed more steps
            elif field[ny][nx] > c+1:
                field[ny][nx] = c+1
            else:
                continue
            # If we didn't run out of steps
            if c + 1 < nb:
                nexts.append((ny, nx, c+1))

    return result


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    result = 0

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
