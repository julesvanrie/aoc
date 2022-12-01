import sys
from aochelper import get_data

lines = get_data(sys.argv)

lines = "\n".join(lines)
elves = lines.split("\n\n")

cals = [elf.split("\n") for elf in elves]

cals_sum = [sum(int(
    c) for c in cal) for cal in cals]

print(sum(sorted(cals_sum, reverse=True)[:3]))
