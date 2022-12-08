import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')

    [print(line) for line in lines[:10]]

    ##########
    # Part 1 #
    ##########

    trees = [[t for t in line] for line in lines]
    height = len(trees)
    width = len(trees[0])
    visibilities = [[True for t in range(width)] for line in range(height)]

    # print(trees)

    for rind, r in enumerate(trees[1:-1], start=1):
        for cind, c in enumerate(r[1:-1], start=1):
            # print(rind, cind)
            visible = True
            col = [row[cind] for row in trees]
            if max(r[:cind]) >= c \
                and max(r[cind+1:]) >= c \
                and max(col[:rind]) >= c \
                and max(col[rind+1:]) >= c:
                    visible = False
            visibilities[rind][cind] = visible

    print(visibilities)
    result1 = sum(sum(v) for v in visibilities)

    ##########
    # Part 2 #
    ##########

    scenics = [[0 for t in range(width)] for line in range(height)]

    for rind, r in enumerate(trees):
        if rind == 0 or rind == width-1:
            scenics[rind][cind] = 0
            continue
        for cind, tree in enumerate(r):
            if cind == 0 or cind == width-1:
                scenics[rind][cind] = 0
                continue
            # print(rind, cind)
            # scenic = [1,1,1,1]
            scenic = [0,0,0,0]
            col = [row[cind] for row in trees]

            for i in range(cind-1,-1, -1):
                if r[i] < tree:
                    scenic[0] += 1
                if r[i] >= tree:
                    scenic[0] += 1
                    break
            for i in range(cind+1,width,1):
                if r[i] < tree:
                    scenic[1] += 1
                if r[i] >= tree:
                    scenic[1] += 1
                    break
            col = [row[cind] for row in trees]
            for i in range(rind-1, -1, -1):
                if col[i] < tree:
                    scenic[2] += 1
                if col[i] >= tree:
                    scenic[2] += 1
                    break
            for i in range(rind+1, height, 1):
                if col[i] < tree:
                    scenic[3] += 1
                if col[i] >= tree:
                    scenic[3] += 1
                    break

            print(rind+1, cind+1, scenic)

            scenics[rind][cind] = scenic[0] * scenic[1] * scenic[2] * scenic[3]

    # print(scenics)
    result2 = max(max(v) for v in scenics)

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
