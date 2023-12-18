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


# def find_next(distances, visited):
#     min = 2**63
#     miny = None
#     minx = None
#     mind = None
#     minc = None
#     for y in range(1, len(distances)-1):
#         for x in range(1,len(distances[y])-1):
#             for d in dirs.keys():
#                 for c in [0, 1, 2, 3]: #[3, 2, 1, 0]:
#                     # penalized_distance = distances[y][x][d][c] #+ prev_dir_counts[y][x][d]
#                     if (not visited[y][x][d][c]
#                         and min > distances[y][x][d][c]):# + prev_dir_counts[y][x][d]):
#                         min = distances[y][x][d][c]
#                         miny = y
#                         minx = x
#                         mind = d
#                         minc = c
#     return miny, minx, mind, minc


# def not_finished(visited):
#     return sum(sum(sum(d.values()) for d in vis) for vis in visited)


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    maxd = 2**63 #(w+h)*10
    # maxd = h*10+w*10

    weights = [[maxd for i in range(w+2)]] \
            + [[maxd] + [int(c) for c in r] + [maxd] for r in input] \
            + [[maxd for i in range(w+2)]]
    # print(len(weights))
    # print(len([weights[0]]))
    # print(weights)
    visited = [[{d: [False, False, False, False] for d in dirs.keys()} for c in r] for r in weights]
    visited[0] = [{d: [True, True, True, True] for d in dirs.keys()} for c in range(w+2)]
    visited[h+1] = [{d: [True, True, True, True] for d in dirs.keys()} for c in range(w+2)]
    for y in range(h+2):
        visited[y][0] =  {d: [True, True, True, True] for d in dirs.keys()}
        visited[y][w+1] =  {d: [True, True, True, True] for d in dirs.keys()}

    distances = [[{d: [maxd, maxd, maxd, maxd] for d in dirs.keys()} for c in r] for r in weights]
    # prev_dir = [[{d: (0,0) for d in dirs.keys()} for c in r] for r in weights]
    # prev_dir_counts = [[{d: [0, 0, 0, 0] for d in dirs.keys()} for c in r] for r in weights]
    parents = [[{d: [None, None, None, None] for d in dirs.keys()} for c in r] for r in weights]

    for d in dirs.keys():
        distances[1][1][d] = [0, 2**63, 2**63, 2**63]

    nexts = [(0, (1, 1, d, 0)) for d in [(0,+1),(+1,0)]]

    heapify(nexts)

    i = 0
    # while i < 5:
    while nexts:
        # not_finished(visited): # and i < 30:
        dist, (y, x, d, c) = heappop(nexts)
        if visited[y][x][d][c]:
            continue

        # if y == h and x == w:
        #     break
        # print(y,x,d,c)
        if y is None:
            break

        visited[y][x][d][c] = True

        # if distances[y][x][d][c] + (h-y) + (w-y) > maxd:
        #     continue


        for nd in dirs.keys():
            # Old dirs and check not reversign
            oy, ox = d #prev_dir[y][x][d]
            dy, dx = (nd[0], nd[1])
            if (dx and dx == -ox
                or dy and dy == -oy):
                continue

            ny = y + dy
            nx = x + dx
            # nd = (dy, dx)
            # print(ny, nx, nd)
            if visited[ny][nx][nd][c]:
                continue
            # Check direction change
            # c = prev_dir_counts[y][x][d]
            same_dir = (dy == oy and dx == ox)
            # reverse_dir = (dx and dx == -ox
            #                or dy and dy == -oy)
            # print(change_dir, dy, dx, prev_dir[y][x])
            if same_dir and c == 2:
                continue
            nc = c + 1 if same_dir else 0
            # else:
            #     print(d, nd)
            # print(ny, nx)
            old = distances[ny][nx][nd][c]
            # new = distances[y][x][d][c] + weights[ny][nx]
            new = dist + weights[ny][nx]
            if new < old:
                distances[ny][nx][nd][nc] = new
                parents[ny][nx][nd][nc] = (y, x, d, c)
                heappush(nexts, (new, (ny, nx, nd, nc)))
                # prev_dir[ny][nx][nd] = d
                # prev_dir_counts[ny][nx][nd] = c + 1 if same_dir else 0
                # print((h*w), sum(sum(sum(d.values()) for d in vis) for vis in visited)-h-h-w-w+4)

        # if not i % 1000:
        #     print(i, y, x, d, c) #, sum(sum(sum(d.values()) for d in vis) for vis in visited)-h-h-w-w+4)
        # i += 1

    # for r in weights:
    #     print(' '.join(f"{c:3}" for c in r))
    # print()
    # for r in distances:
    #     print(' '.join(f"{c:3}" for c in r))
    # print()
    # for r in prev_dir_counts:
    #     print(' '.join(f"{c:3}" for c in r))

    # pprint(parents)

    path = [[c for c in r] for r in weights]

    # pprint(distances[1:-1])

    pprint(distances[h-1][w])
    print()
    pprint(distances[h][w-1])
    print()
    print(distances[h][w][(0, 1)])
    print(distances[h][w][(1, 0)])

    end = 2**63
    end_d = None
    end_c = None
    for d in [(0,+1),(+1,0)]:
        for c in [0, 1, 2, 3]:
            if distances[h][w][d][c] < end:
                end = distances[h][w][d][c]
                end_d = d
                end_c = c

    pos = (h, w, end_d, end_c)
    print(pos)
    while (pos[0], pos[1]) != (1, 1):
        # print(pos)
        y = pos[0]
        x = pos[1]
        d = pos[2]
        c = pos[3]
        # print(y, x, d, c)
        # print(y, x, d, parents[y][x][d])
        oy, ox, od, oc = parents[y][x][d][c]
        path[y][x] = dirs[d] #prev_dir[y][x][d]]
        pos = parents[y][x][d][c] # (oy, ox, od)

    for r in path[1:-1]:
        print(''.join(f"{c}" for c in r[1:-1]))


    result = end

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
