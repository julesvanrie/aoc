import sys
from aochelper import get_data

lines = get_data(sys.argv)

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

print(cals_sum[elf_max])
