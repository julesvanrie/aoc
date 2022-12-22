import os, sys, timeit
from aochelper import get_data
import re

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')
    text = lines if lines else get_data(sys.argv)
    lines, path = text.split('\n\n')
    lines = lines.split('\n')
    height = len(lines)
    width = max(len(line) for line in lines)
    dim = max(height, width) / 4
    lines = [[line[i] if i < len(line) else ' ' for i in range(width)] for line in lines]
    path = [p if p in ['L','R'] else int(p) for p in re.findall(r"\d+|[LR]", path)]


    ##########
    # Part 1 #
    ##########

    # Directions
    facings = ((0,1), # right
            (1,0), # down
            (0,-1), # left
            (-1,0),) # up

    # Start position (0 based)
    y = 0
    x = lines[0].index('.')
    facing = 0

    # Loop over the instructions
    # Each pass takes a move (number) and a turn (L, R)
    while path:
        # Move
        instr = path.pop(0)
        for _ in range(instr):
            ny = (y + facings[facing][0]) % height
            nx = (x + facings[facing][1]) % width
            while lines[ny][nx] == ' ':
                ny = (ny + facings[facing][0]) % height
                nx = (nx + facings[facing][1]) % width
            if lines[ny][nx] == '.':
                # lines[ny][nx] = 'O'
                y = ny
                x = nx
            elif lines[ny][nx] == '#':
                break
            else:
                print("Something strange happened", lines[ny][nx])
        # Turn
        if len(path):
            instr = path.pop(0)
            # print('turn', instr)
            facing += 1 if instr == 'R' else -1
            facing %= 4

    # for line in lines:
    #     print(''.join(line))

    result1 = None
    result1 = 1000 * (y+1) + 4 * (x+1) + facing

    ##########
    # Part 2 #
    ##########



    result2 = None

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
