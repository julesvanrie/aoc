import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')

    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')

    x = 1
    strength = 0
    i = 0
    cycles = 1
    crt = ['.' for i in range(240)]
    while i < len(lines):
        if (cycles-1) % 40 in [x-1,x,x+1]:
            crt[(cycles-1) % 240] = '#'
        if not (cycles + 20) % 40:
            strength += cycles*x
        if lines[i][:4] == 'addx':
            cycles += 1
            if (cycles-1) % 40 in [x-1,x,x+1]:
                crt[(cycles-1) % 240] = '#'
            if not (cycles + 20) % 40:
                strength += cycles*x
            x += int(lines[i][5:])
        i += 1
        cycles  += 1


    result1 = strength
    result2 = ''.join(''.join(crt[l*40:(l+1)*40]) + '\n' for l in range(6))

    print("The result is for part 1 is:", result1)
    print("The result is for part 2 is:\n\n", result2, "\nWhat letters can you read?", sep='')

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
