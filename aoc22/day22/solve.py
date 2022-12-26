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


    def run(part):
        # Directions
        facings = ((0,1), # right
                (1,0), # down
                (0,-1), # left
                (-1,0),) # up

        # transformation = {
        #     ('left','top'): -2,
        #     ('top','left'): -2,
        #     ('top','back'): +1,
        #     ('back','top'): +1,
        #     ('front','left'): -1,
        #     ('left','front'): -1,
        #     ('bottom','right'): -2,
        #     ('right','bottom'): -2,
        #     ('bottom','back'): -1,
        #     ('back','bottom'): -1,
        #     ('back','right'): 0,
        #     ('right','back'): 0,
        #     ('right','front'): -1,
        #     ('front','right'): -1,

        #     ('right','top'): 0,
        #     ('top','right'): 0,
        #     ('top','front'): 0,
        #     ('front','top'): 0,
        #     ('front','bottom'): 0,
        #     ('bottom','front'): 0,
        #     ('bottom','left'): 0,
        #     ('left','bottom'): 0,
        #     ('left','back'): 0,
        #     ('back','left'): 0,
        # }

        # For test input
        transformation = {
            ('left','top'): -1,
            ('top','left'): -1,
            ('top','back'): +2,
            ('back','top'): +2,
            ('front','left'): 0,
            ('left','front'): 0,
            ('bottom','right'): 0,
            ('right','bottom'): 0,
            ('bottom','back'): -2,
            ('back','bottom'): -2,
            ('back','right'): -1,
            ('right','back'): -11,
            ('right','front'): -1,
            ('front','right'): -1,

            ('right','top'): -2,
            ('top','right'): -2,
            ('top','front'): 0,
            ('front','top'): 0,
            ('front','bottom'): 0,
            ('bottom','front'): 0,
            ('bottom','left'): -1,
            ('left','bottom'): -1,
            ('left','back'): 0,
            ('back','left'): 0,
        }

        starts = {
            'top': (0,50),
            'front': (50,50),
            'bottom': (100,50),
            'left': (100,0),
            'back': (150,0),
            'right': (0,100),
        }

        # For test: y, x, dir y, dir x, facing
        # y, x is those where in new coords closest to 0 for x, y, or z
        # In new: x points right, y points forward, z points downward
        # Directions indicate what pos movement originally means in new
        # Facing indicates how much steps to change facing
        starts = {
            'top': (8,0,1,1),
            'front': (8,8,1,1),
            'bottom': (8,8,-1,0),
            'left': (4,4,1,1),
            'back': (4,0,1,-1),
            'right': (8,12,1,-1),
        }

        # Start position (0 based)
        y = 0
        x = lines[0].index('.')
        facing = 0


        cube = [[['' for x in range(dim+2)] for y in z range(dim+2)] for z in range(dim+2)]

        # # Top and bottom
        # # for start, pos in starts.items():
        # for a in range(0,dim):
        #     for b in range(0,dim):
        #         posy = pos[0] + dim if pos[2] == -1
        #         posx = pos[1] + dim if pos[3] == -1
        #         diry = pos[2]
        #         dirx = pos[3]
        #         # Top
        #         cube[dim+1][b][a] = lines[posy + diry*b][posx + dirx*b]
        #         # Bottom
        #         cube[0][b][a] = lines[posy + diry*b][posx + dirx*b]
        #         # Front
        #         cube[a][dim+1][a] = lines[posy + diry*b][posx + dirx*b]
        #         # Back
        #         cube[b][0][a] = lines[posy + diry*b][posx + dirx*b]
        #         # Left
        #         cube[b][a][0] = lines[posy + diry*b][posx + dirx*b]
        #         # Right
        #         cube[b][a][dim+1] = lines[posy + diry*b][posx + dirx*b]






        def transition(y, x, dir):
            for start, pos in starts.items():
                if (y in range(pos[0], pos[0]+dim) and
                    x in range(pos[1], pos[1]+dim)):
                    origin = start



        # Loop over the instructions
        # Each pass takes a move (number) and a turn (L, R)
        while path:
            # Move
            instr = path.pop(0)
            for _ in range(instr):
                ny = (y + facings[facing][0]) % height
                nx = (x + facings[facing][1]) % width
                if lines[ny][nx] == ' '
                    if part == 1:
                        while lines[ny][nx] == ' ':
                            ny = (ny + facings[facing][0]) % height
                            nx = (nx + facings[facing][1]) % width
                    elif part == 2:

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
        return 1000 * (y+1) + 4 * (x+1) + facing

    # for line in lines:
    #     print(''.join(line))

    result1 = run(1)

    ##########
    # Part 2 #
    ##########



    result2 = run(2)

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
