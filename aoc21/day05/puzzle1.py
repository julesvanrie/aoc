with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]


lines = [[[int(coord) for coord in point.split(',')] for point in line.split(' -> ')] for line in lines]

horiz = [line for line in lines if line[0][1] == line[1][1]]
verti = [line for line in lines if line[0][0] == line[1][0]]


vent_coords = {}

for line in verti:
    x = line[0][0]
    y_0 = line[0][1]
    y_1 = line[1][1]
    step = 1 if y_1 > y_0 else -1
    for y in range(y_0, y_1+step, step):
        existing = vent_coords.get(x, None)
        if existing:
            count = existing.get(y, 0)
            vent_coords[x][y] = count + 1
        else:
            vent_coords[x] = {y: 1}

for line in horiz:
    x_0 = line[0][0]
    x_1 = line[1][0]
    y = line[0][1]
    step = 1 if x_1 > x_0 else -1
    for x in range(x_0, x_1+step, step):
        existing = vent_coords.get(x, None)
        if existing:
            count = existing.get(y, 0)
            vent_coords[x][y] = count + 1
        else:
            vent_coords[x] = {y: 1}

overlaps = 0

x_s = vent_coords.keys()
for x in x_s:
    y_s = vent_coords[x].keys()
    for y in y_s:
        if vent_coords[x][y] >= 2:
            overlaps += 1

print(overlaps)
