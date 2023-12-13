import sys
from aocsolution.basesolution import BaseSolution

import re
from pprint import pprint

# Valid connections for a given direction (y, x)
c = {
    (0, -1): ['-', 'F', 'L'], # left
    (0, +1): ['-', '7', 'J'], # right
    (-1, 0): ['|', 'F', '7'], # up
    (+1, 0): ['|', 'L', 'J'], # down
}

def find_loop(self, p):
    """Find the real loop
    p = input data
    returns d[y][x] = distances from start, or -1 if not on the loop
    """
    h = len(p)
    w = len(p[0])

    # Find start
    for y in range(h):
        if (x := p[y].find('S')) != -1:
            sx = x
            sy = y
            break

    # Distances initialisation to -1
    d = [[-1 for i in range(w)] for j in range(h)]
    d[sy][sx] = 0

    # Directions (y, x) to check for a connection
    # depending on what's on the given position
    dirs = {
        '|': [(-1, 0), (+1, 0)],
        '-': [(0, -1), (0, +1)],
        'J': [(0, -1), (-1, 0)],
        '7': [(0, -1), (+1, 0)],
        'L': [(0, +1), (-1, 0)],
        'F': [(0, +1), (+1, 0)],
        'S': c.keys()
    }

    # Keep track of next positions to check, starting from start
    n = [(sy, sx)]
    for y, x in n:
        # Check all directions depending on what's on the given position
        for dy, dx in dirs[p[y][x]]:
            ny = y + dy
            nx = x + dx
            if (
                ny>=0 and ny<h and             # If not beyond the border
                nx>=0 and nx<w and             #
                d[ny][nx] == -1 and            #    not checked before
                p[ny][nx] in c[(dy,dx)]        #    connected to previous one
            ):
                n.append((y+dy, x+dx))         # Add to next checks
                d[y+dy][x+dx] = d[y][x] + 1    # Calculate distance

    return d


@BaseSolution.time_this
def solve_one(self):
    p = self.get_data()
    d = self.find_loop(p)
    return max(max(r) for r in d)


@BaseSolution.time_this
def solve_two(self):
    p = self.get_data()

    # Add dummy rows '-' and columns '|' to allow gliding in between pipes
    p = ['-'.join(r) for r in p]
    p = [p[i//2] if not i % 2 else '|'*len(p[0]) for i in range(len(p)*2)]

    d = self.find_loop(p)
    h = len(p)
    w = len(p[0])

    # Keep track of I for nests, O for outside loop, # for on the loop
    nests = [['.' for i in range(w)] for j in range(h)]
    # Keep track of next positions to check
    n = []
    for y in range(h):
        # Left and right border: if not on the loop they are outside
        for x in [0, w-1]:
            if d[y][x] == -1:
                nests[y][x] = 'O'
                n.append((y, x))
        # The loop
        for x in range(w):
            if d[y][x] >= 0:
                nests[y][x] = '#'
    # Top and bottom border: if not on the loop they are outside
    for x in range(w):
        for y in [0, h-1]:
            if d[y][x] == -1:
                nests[y][x] = 'O'
                n.append((y, x))

    # Points to check: neighbours connected to this point are outside if not on the loop
    for y, x in n:
        # Check all directions
        for dy, dx in c.keys():
            ny = y + dy
            nx = x + dx
            if (
                ny>=0 and ny<h and    # If not beyond the border
                nx>=0 and nx<w and    #
                nests[ny][nx] == '.'  #    not checked before, not on the loop
            ):
                nests[ny][nx] = 'O'   # Point is outside
                n.append((ny, nx))    # Add point to points to check next

    # Count the remaining dots. But first remove the dummy rows
    result = 0
    for r in nests[::2]:
        # print(''.join(r[::2]))
        result += r[::2].count('.')
    return result


class Solution(BaseSolution):
    find_loop = find_loop
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
