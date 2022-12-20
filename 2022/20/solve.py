import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')

    numbers = [*map(int, lines)]

    ##########
    # Part 1 #
    ##########

    length = len(numbers)
    # Storing locations of original numbers. Key is original location
    location = {i: i for i in range(length)}
    # Lookup, basically the reverse lookup of location
    lookup = {i: i for i in range(length)}

    def modu(number, div):
        """Sort of a custom made modulo operation to determine new location.
        A number equal to lenght doesn't wrap around to exactly the same location."""
        if number > div:
            return (number + number // div) % div
        elif number > 0:
            return number % div
        else:
            return (number - abs(number) // div - 1) % div

    if length <10:
        print(numbers)

    for i in range(length):

        n = numbers[i]

        cur_loc = location[i]
        fut_loc = modu(cur_loc + n, length)

        if fut_loc > cur_loc:
            rng = range(cur_loc+1, fut_loc+1)
            dir = -1
        else:
            rng = range(fut_loc, cur_loc)
            dir = 1
        for j in rng:
            location[lookup[j]] = (location[lookup[j]] + dir) % length
        location[i] = modu((location[i] + n), length)



        lookup = {v: k for k, v in location.items()}

        if length <10:
            new = [numbers[lookup[j]] for j in range(length)]
            print(i, min(lookup.keys()), max(lookup.keys()), len(lookup), new)



    new = [numbers[lookup[j]] for j in range(length)]

    results = [new[(new.index(0) + i*1000) % len(new)] for i in [1,2,3]]

    result1 = sum(results)

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
