import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')

    height = len(lines) - 2
    width = len(lines[0]) - 2

    mapping = {
        'v': (1,0),
        '>': (0,1),
        '<': (0,-1),
        '^': (-1,0),
    }

    r_mapping = {v: k for k, v in mapping.items()}

    blizzards = {(y, x, lines[y+1][x+1]): mapping[lines[y+1][x+1]]
                 for x in range(width)
                 for y in range(height)
                 if lines[y+1][x+1] != '.'}


    def show():
        for y in range(height):
            for x in range(width):
                current = []
                for dir in mapping:
                    if (b := (y,x,dir)) in blizzards:
                        current.append(b)
                if (nbr := len(current)) == 1:
                    print(current[0][2], end='')
                elif nbr > 1:
                    print(nbr, end='')
                else:
                    print('.', end='')
            print('')
        print('')

    ##########
    # Part 1 #
    ##########


    def next_blizzards(blizzards):
        return { ( (blizzard[0] + dir[0]) % height,
                        (blizzard[1] + dir[1]) % width,
                        blizzard[2] ) : dir
                      for blizzard, dir in blizzards.items()}

    states = []
    current_min = 990

    def trial(start=(-1,0), minute=0, blizzards=blizzards):
        nonlocal current_min
        if minute >= current_min:
            return
        if (start, minute) in states:
            return
        # print(start,end='\r')
        for dir in mapping.values():
            new = (start[0] + dir[0], start[1] + dir[1])
            if new == (height, width-1):
                if minute < current_min:
                    current_min = minute
                    print(minute, end='\r')
                # states.append((new, minute))
                return
            if new[0] < 0 or new[0] >= height or \
                new[1] < 0 or new[1] >= width:
                continue
            can_move = True
            for d in mapping:
                if (new[0],new[1],d) in next_blizzards(blizzards):
                    can_move = False
                    break
            if can_move:
                trial(new, minute=minute+1, blizzards=next_blizzards(blizzards))
        can_stay = True
        for d in mapping:
            if (start[0],start[1],d) in next_blizzards(blizzards):
                can_stay = False
                break
        if can_stay:
            trial(start, minute=minute+1,  blizzards=next_blizzards(blizzards))
        states.append((start, minute))


    trial(start=(-1,0), minute=0, blizzards=blizzards)


    result1 = current_min + 1
    print("The result is for part 1 is:", result1)

    ##########
    # Part 2 #
    ##########


    result2 = None
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
