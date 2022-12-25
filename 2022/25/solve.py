import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')


    mapfrom = {
        '2': 2,
        '1': 1,
        '0': 0,
        '-': -1,
        '=': -2,
    }
    mapto = {v: k for k, v in mapfrom.items()}


    def fromsnafu(snafu):
        return sum(mapfrom[c]*5**i for i, c in enumerate(snafu[::-1]))


    def tosnafu(number):
        snafu = []
        while number:
            if (number % 5) in [3,4]:
                rest = number % 5 - 5
                number = (number + 5) // 5
            else:
                rest = number % 5
                number = number // 5
            snafu.append(mapto[rest])
        return ''.join(snafu[::-1])


    result1 = tosnafu(sum(fromsnafu(line) for line in lines))
    print("The result is for part 1 is:", result1)


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
