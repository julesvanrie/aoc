import os, sys, timeit
from aochelper import get_data

def solve(lines):
    if not lines:
        lines = get_data(sys.argv)

    [print(line) for line in lines[:20]]

    ##########
    # Part 1 #
    ##########


    result1 = None

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
