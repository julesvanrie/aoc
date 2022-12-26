with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

risk_levels = [[int(d) for d in line] for line in lines]

length = len(risk_levels)
width = len(risk_levels[0])

risk = [[0 for i in range(width)] for j in range(length)]
risk[0][0] = risk_levels[0][0]


def find_lowest(x, y, all_dirs=False):
    risks_around = []
    search = [(x, y - 1), (x - 1, y)]
    if all_dirs:
        risks_around = [risk[y][x] - risk_levels[y][x]]
        search.extend([(x, y + 1), (x + 1, y)])
    for x_c, y_c in search:
        if (x_c < width and y_c < length and x_c >= 0 and y_c >= 0):
            risks_around.append(risk[y_c][x_c])
    risk_old = min(risks_around)
    risk[y][x] = risk_old + risk_levels[y][x]
    return

for y in range(length):
    for x in range(width):
        if not((x == 0) and (y == 0)):
            find_lowest(x, y)

changed = True
while changed:
    changed = False
    for y in range(length):
        for x in range(width):
            old = risk[y][x]
            find_lowest(x, y, all_dirs=True)
            if risk[y][x] < old:
                changed = True

result = risk[-1][-1] - risk_levels[0][0]

print(f"Result is {result}")
