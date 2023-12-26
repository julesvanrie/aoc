import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint
from heapq import *


dirs = {
    (+1,0): 'v',
    (0,+1): '>',
    (-1,0): '^',
    (0,-1): '<'
}


@BaseSolution.time_this
def solve_one(self, minstraights=1, maxstraights=3):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    maxd = 2**63
    straights = maxstraights + 1

    # Weights = inputs with some padding to remove edge cases
    weights = [[maxd for i in range(w+2)]] \
            + [[maxd] + [int(c) for c in r] + [maxd] for r in input] \
            + [[maxd for i in range(w+2)]]

    # # Visited is False, except for the padding at the borders
    # visited = [[{d: [False]*straights for d in dirs.keys()} for c in r] for r in weights]
    # visited[0] = [{d: [True]*straights for d in dirs.keys()} for c in range(w+2)]
    # visited[h+1] = [{d: [True]*straights for d in dirs.keys()} for c in range(w+2)]
    # for y in range(h+2):
    #     visited[y][0] =  {d: [True]*straights for d in dirs.keys()}
    #     visited[y][w+1] =  {d: [True]*straights for d in dirs.keys()}

    distances = [[{d: [maxd]*straights for d in dirs.keys()} for c in r] for r in weights]
    parents = [[{d: [None]*straights for d in dirs.keys()} for c in r] for r in weights]

    nexts = [(0, (1, 1, d, 0)) for d in [(0,+1),(+1,0)]]
    # heapify(nexts)
    while nexts:
        dist, (y, x, d, c) = heappop(nexts)
        # if visited[y][x][d][c]:
        #     continue
        # Reached the goal
        if y == h and x == w: # and c >= (minstraights - 1):
            print(min(distances[h][w][(+1,0)]), c)
            print(min(distances[h][w][(0,+1)]), c)
            # return dist

        # visited[y][x][d][c] = True

        for nd in dirs.keys():
            oy, ox = d
            dy, dx = nd
            ny = y + dy
            nx = x + dx
            # print(y, x, d, c, nd)
            # if visited[ny][nx][nd][c]:
            #     continue
            # # Check no reverse
            if (dy == -oy) and (dx == -ox):
                continue
            # Check direction change
            same_dir = ((dy == oy) and (dx == ox))
            if c == maxstraights: # and ny != h and nx != w:
            # # if same_dir and (c >= (maxstraights-1)):
            #     # print(c)
                continue
            if (not same_dir) and (c < (minstraights - 1)):
                continue
            nc = (c + 1) if same_dir else 0
            # print('   check ', (y, x), nc)
            if (
                (dy == 1 and ((nc + h - ny + 1) < minstraights))
                or (dx == 1 and ((nc + w - nx + 1) < minstraights))
            ):
                continue
            if (
                (dy == -1 and ((nc + ny - 1) <= minstraights))
                or (dx == -1 and ((nc + nx - 1) <= minstraights))
            ):
                if nc != 0:
                    print('   continue ', (y, x), (nd), nc)
                continue
            old = distances[ny][nx][nd][nc]
            new = dist + weights[ny][nx]
            if new < old:
                distances[ny][nx][nd][nc] = new
                parents[ny][nx][nd][nc] = (y, x, d, c)
                heappush(nexts, (new, (ny, nx, nd, nc)))

    return min((min(distances[h][w][(0,+1)])), min(distances[h][w][(+1,0)]))



@BaseSolution.time_this
def solve_two(self):
    return self.solve_one(4, 10)


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
