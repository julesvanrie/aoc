import sys
from aochelper import get_data


def solve(lines=None):
    text = lines if lines else get_data(sys.argv)

    elves = text.split("\n\n")

    cals = [elf.split("\n") for elf in elves]

    cals_sum = [sum(int(c) for c in cal) for cal in cals]

    max_c = 0
    for i, c in enumerate(cals_sum):
        if c > max_c:
            max_c = c
            elf_max = i
            # print(elf_max)

    result1 = cals_sum[elf_max]
    result2 = sum(sorted(cals_sum, reverse=True)[:3])

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
