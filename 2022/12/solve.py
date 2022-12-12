import os, sys, timeit
from aochelper import get_data

sys.setrecursionlimit(2000)

def solve(lines=None):
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')

    h = len(lines)
    w = len(lines[0])
    S = [None, None]
    E = [None, None]


    for i, line in enumerate(lines):
        try:
            S[1] = line.index('S',)
            S[0] = i
            E[1] = line.index('E')
            E[0] = i
        except:
            try:
                E[1] = line.index('E')
                E[0] = i
            except:
                continue

    print('Start:', S, 'End:', E)
    lines = [list(line) for line in lines]

    lines[S[0]][S[1]] = 'a'
    lines[E[0]][E[1]] = 'z'

    dirs = [(0,1),(0,-1),(1,0),(-1,0),]


    ##########
    # Part 1 #
    ##########

    # Initiating distances and visited and candidates
    distances = [[2**63 for _ in range(w)] for _ in range(h)]
    distances[S[0]][S[1]] = 0
    visited = [[False for _ in range(w)] for _ in range(h)]
    unvisited = []
    for y in range(h):
        for x in range(w):
            unvisited.append([y, x])

    distance = 2**63
    found = False
    while not found:
        # print(unvisited)
        pos = sorted(unvisited, key=lambda c: distances[c[0]][c[1]])[0]
        for dir in dirs:
            y = pos[0] + dir[0]
            x = pos[1] + dir[1]
            if x >= 0 and y >= 0 and x < w and y < h:
                if visited[y][x]:
                    continue
                current = lines[pos[0]][pos[1]]
                current_dist = distances[pos[0]][pos[1]]
                new = lines[y][x]
                if ord(new) <= ord(current) + 1:
                    if distances[y][x] > current_dist + 1:
                        distances[y][x] = current_dist + 1
                    if y == E[0] and x == E[1]:
                        found = True
                        distance = distances[y][x]
                        break
        if found:
            break
        unvisited.remove(pos)
        visited[pos[0]][pos[1]] = True



    result1 = distance
    # [print(*distance) for distance in distances]

    # largest = 0
    # location = [0,0]
    # for i in range(h):
    #     for j in range(w):
    #         if visited[i][j]:
    #             print(lines[i][j], end='')
    #             if distances[i][j] > largest:
    #                 largest = distances[i][j]
    #                 location[0] = i
    #                 location[1] = j
    #         else:
    #             print(' ', end='')
    #     print('')


    # for i in range(15, 26):
    #     for j in range(110, 130):
    #         if visited[i][j]:
    #             print(lines[i][j], distances[i][j], end=' ')
    #         else:
    #             print('    ', end='')
    #     print('')

    # print(lines[location[0]][location[1]])

    ##########
    # Part 2 #
    ##########

    # Initiating distances and visited and candidates
    distances = [[2**63 for _ in range(w)] for _ in range(h)]
    distances[E[0]][E[1]] = 0
    visited = [[False for _ in range(w)] for _ in range(h)]
    unvisited = []
    for y in range(h):
        for x in range(w):
            unvisited.append([y, x])

    distance = 2**63
    found = False
    while not found:
        # print(unvisited)
        pos = sorted(unvisited, key=lambda c: distances[c[0]][c[1]])[0]
        for dir in dirs:
            y = pos[0] + dir[0]
            x = pos[1] + dir[1]
            if x >= 0 and y >= 0 and x < w and y < h:
                if visited[y][x]:
                    continue
                current = lines[pos[0]][pos[1]]
                current_dist = distances[pos[0]][pos[1]]
                new = lines[y][x]
                if ord(new) >= ord(current) - 1:
                    if distances[y][x] > current_dist + 1:
                        distances[y][x] = current_dist + 1
                    if lines[y][x] == 'a':
                        found = True
                        distance = distances[y][x]
                        break
        if found:
            break
        unvisited.remove(pos)
        visited[pos[0]][pos[1]] = True


    # def next(pos, steps, previous):
    #     if not pos:
    #         return None
    #     nonlocal shortest
    #     nonlocal visited
    #     print(shortest, pos, steps, lines[pos[0]][pos[1]])
    #     if steps >= shortest:
    #         return None
    #     if lines[pos[0]][pos[1]] == chr(ord('a')-1):
    #         shortest = steps
    #         print(shortest)
    #         return steps
    #     best = shortest
    #     for dir in dirs:
    #         y = pos[0] + dir[0]
    #         x = pos[1] + dir[1]
    #         if x >= 0 and y >= 0 and x < w and y < h:
    #             trial = [y, x]
    #             # path = previous.copy().append(trial)
    #             # if path in visited:
    #             #     continue
    #             # visited.append(path)
    #             # print(visited)
    #             current = lines[pos[0]][pos[1]]
    #             new = lines[trial[0]][trial[1]]
    #
    #                 result = next(trial, steps + 1, pos)
    #                 if result and result < best:
    #                     best = result
    #     # if best <= shortest:
    #     return best
    #     # return None

    result2 = distance

    print("The result is for part 1 is:", result1)
    print("The result is for part 2 is:", result2)

    return result1, result2

def time():
    with open(os.devnull, 'w') as out:
        sys.stdout = out
        number = 20
        timing = timeit.timeit(solve, number=number) / number
        sys.stdout = sys.__stdout__
    print(f"This took {timing:.6f} seconds")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1][:4] == "time":
        del sys.argv[1]
        time()
    else:
        solve()
