import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')
    test_mode = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    lines = [lines] if len(lines) > 10 else lines

    for line in lines:
        result1 = 0; result2 = 0
        for i in range(len(line)):
            if not result1 and len(set(line[i:i+4])) == 4:
                result1 = i
            if not result2 and len(set(line[i:i+14])) == 14:
                result2 = i
        result1 += 4; result2 += 14
        print("Part 1:", result1, "Part 2:", result2) if test_mode else print('')

    if not test_mode:
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
