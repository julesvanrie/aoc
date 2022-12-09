import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')

    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')


    ##########
    # Part 1 #
    ##########

    visited = { (0,0): True}

    dirs = {'R': ( 0, 1),
            'L': ( 0,-1),
            'U': ( 1, 0),
            'D': (-1, 0),
            }

    posH = [0,0]
    posT = [0,0]
    for line in lines:
        # print(line)
        d, s = (line.split(' '))
        for i in range(int(s)):
            posH[0] = posH[0] + dirs[d][0]
            posH[1] = posH[1] + dirs[d][1]
            # print(posH)
            for j in range(2):
                k = (j+1)%2
                if posH[j] == posT[j]:
                    dist = posH[k] - posT[k]
                    if abs(dist) == 2:
                        posT[k] = posT[k] + int(dist / 2)

            dist = [posH[0] - posT[0], posH[1] - posT[1]]
            if abs(dist[0]) + abs(dist[1]) == 3:
                posT[0] = posT[0] + int(dist[0] / abs(dist[0]))
                posT[1] = posT[1] + int(dist[1] / abs(dist[1]))
            visited[tuple(posT)] =  True
            # print(posH, posT)


    result1 = len(visited)

    ##########
    # Part 2 #
    ##########

    def move(posH, posT):
        # print(posH, posT)
        for j in range(2):
            k = (j+1)%2
            if posH[j] == posT[j]:
                dist = posH[k] - posT[k]
                if abs(dist) == 2:
                    posT[k] = posT[k] + int(dist / 2)

        dist = [posH[0] - posT[0], posH[1] - posT[1]]
        if abs(dist[0]) + abs(dist[1]) >= 3:
            posT[0] = posT[0] + int(dist[0] / abs(dist[0]))
            posT[1] = posT[1] + int(dist[1] / abs(dist[1]))
        # print(posT)
        return None

    visited = { (0,0): True}

    pos = [[0,0] for i in range(10)]
    for line in lines:
        # print(line)
        d, s = (line.split(' '))
        for _ in range(int(s)):
            pos[0][0] = pos[0][0] + dirs[d][0]
            pos[0][1] = pos[0][1] + dirs[d][1]
            # print(posH)
            for i in range(9):
                # pos[i+1] =
                move(pos[i], pos[i+1])
            visited[tuple(pos[9])] =  True
            # for y in range(9,-1,-1):
            #     for x in range(10):
            #         there = False
            #         for p in range(10):
            #             if x == pos[p][1] and y == pos[p][0]:
            #                 print(p, end='')
            #                 there = True
            #                 break
            #         if not there:
            #             print('.', end='')
            #     print('')
            # print('')

    result2 = len(visited)

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
