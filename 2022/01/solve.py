import sys
from aochelper import get_data

def solve(lines):
    if not lines:
        lines = get_data(sys.argv)

    ##########
    # Part 1 #
    ##########


    lines = "\n".join(lines)
    elves = lines.split("\n\n")

    cals = [elf.split("\n") for elf in elves]

    cals_sum = [sum(int(c) for c in cal) for cal in cals]

    max_c = 0
    for i, c in enumerate(cals_sum):
        if c > max_c:
            max_c = c
            elf_max = i
            # print(elf_max)

    result1 = cals_sum[elf_max]
    print(result1)



    ##########
    # Part 2 #
    ##########

    result2 = sum(sorted(cals_sum, reverse=True)[:3])
    print(result2)

    return result1, result2
