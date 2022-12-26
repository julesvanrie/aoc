import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')


    def run(numbers, location, lookup):
        """One run of mixing
        """
        for i in range(length := len(numbers)):
            n = numbers[i]
            cur_loc = location[i]
            fut_loc = (cur_loc + n) % (length - 1)

            if fut_loc > cur_loc:
                rng = range(cur_loc+1, fut_loc+1)
                dir = -1
            else:
                rng = range(fut_loc, cur_loc)
                dir = 1
            for j in rng:
                location[lookup[j]] = (location[lookup[j]] + dir) % length
            location[i] = fut_loc

            lookup = {v: k for k, v in location.items()}

        return location, lookup


    def part(part):
        """Run for part 1 or 2
        """
        numbers = [*map(int, lines)]
        length = len(numbers)

        # Storing locations of original numbers. Key is original location
        location = {i: i for i in range(length)}
        # Lookup, basically the reverse lookup of location
        lookup = {i: i for i in range(length)}

        if part == 2:
            numbers = [n * 811589153 for n in numbers]

        for i in range(10 if part == 2 else 1, 0, -1):
            print("===", i-1 , "left after this round ===", end=('\n' if i == 1 else '\r'))
            location, lookup = run(numbers, location, lookup)

        new_order = [numbers[lookup[j]] for j in range(length)]

        results = [new_order[(new_order.index(0) + i*1000) % length] for i in [1,2,3]]

        return sum(results)

    result1 = part(1)
    print("The result for part 1 is:", result1)

    result2 = part(2)
    print("The result for part 2 is:", result2)

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
