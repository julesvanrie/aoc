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

    def next_blizzards(blizzards):
        return { ( (blizzard[0] + dir[0]) % height,
                        (blizzard[1] + dir[1]) % width,
                        blizzard[2] ) : dir
                      for blizzard, dir in blizzards.items()}


    def trial(start, end, minute, blizzards):
        states = {start}
        while True:
            new_states = set()
            next_blizz_pos = set((b[0],b[1]) for b in next_blizzards(blizzards))
            for state in states:
                for dir in list(mapping.values()) + [(0,0)]:
                    new = (state[0] + dir[0], state[1] + dir[1])
                    if new == end:
                        return minute+1, next_blizzards(blizzards)
                    if (new == start or                       # Start position or
                        (new not in next_blizz_pos and not    # (not in blizzard and
                         (new[0] < 0 or new[0] >= height or   # not in walls)
                          new[1] < 0 or new[1] >= width))):
                        new_states.add(new)
            blizzards = next_blizzards(blizzards)
            states = new_states
            minute += 1

    start = (-1,0)
    end = (height,width-1)

    result1, blizzards = trial(start, end, minute=0, blizzards=blizzards)
    print("The result is for part 1 is:", result1)

    back, blizzards = trial(end, start, result1, blizzards)
    result2, _ = trial(start, end, back, blizzards)
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
