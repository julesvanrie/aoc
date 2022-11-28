import sys

# Default file to open is inputX.txt with X same as this file
if len(sys.argv) > 1:
    filename = f"{sys.argv[1]}.txt"
else:
    filename = f"input{__file__.split('.')[0][-1]}.txt"

# Read input file
with open(filename, "r") as fo:
    lines = [line.strip('\n') for line in fo.readlines()]

[print(line) for line in lines]
