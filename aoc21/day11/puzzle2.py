with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

lines = [[int(digit) for digit in list(line)] for line in lines]

length = len(lines)
width = len(lines[0])

flashes = 0
all_flashes = None

def flash(r, c):
    global flashes
    flashes += 1
    lines[r][c] = 0
    for i in range(max(0, r - 1), min(length, r + 2)):
        for j in range(max(0, c - 1), min(width, c + 2)):
            if (i != r or j != c) and lines[i][j]:
                lines[i][j] += 1
                if lines[i][j] > 9:
                    flash(i, j)


for step in range(1000):
    for r, line in enumerate(lines):
        for c, digit in enumerate(line):
            line[c] += 1

    for r, line in enumerate(lines):
        for c, digit in enumerate(line):
            if line[c] > 9:
                flash(r, c)

    if step == 99:
        result = flashes

    if sum([sum(line) for line in lines]) == 0:
        all_flashes = step + 1
        break

print(f"Number of flashes is {result}")
print(f"All flash in step {all_flashes}")
