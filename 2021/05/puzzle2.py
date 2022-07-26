with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

# Get all coordinates
lines = [[[int(coord) for coord in point.split(',')] for point in line.split(' -> ')] for line in lines]

# dict to store vent locations
vent_coords = {}
for line in lines:
    x_0 = line[0][0]
    x_1 = line[1][0]
    y_0 = line[0][1]
    y_1 = line[1][1]
    # Is it a diagonal vent?
    d = not(y_0 == y_1 or x_0 == x_1)
    # Steps x and y to go from one to the other point
    step_x = 1 if x_1 >= x_0 else -1
    step_y = 1 if y_1 >= y_0 else -1
    # Loop from beginning to end point
    for x in range(x_0, x_1+step_x, step_x):
        for y in range(y_0, y_1+step_y, step_y):
            # Check if we already had the x in the vents dict
            existing = vent_coords.get(x, None)
            if existing:
                # Check if we already had the y for this x, then increase
                count = existing.get(y, 0)
                vent_coords[x][y] = count + 1
            else:
                # If it's a new x, create it's dict with one value for our y
                vent_coords[x] = {y: 1}
            # If it's a diagonal, we don't have to loop over other y's
            if d:
                break
        # If it's a diagonal, in the next loop we don't have to start
        # at y_0, we can immediately go to the next one
        if d:
            y_0 = y_0 + step_y

# Now let's loop through the dict and get >=0
overlaps = 0
x_s = vent_coords.keys()
for x in x_s:
    y_s = vent_coords[x].keys()
    for y in y_s:
        if vent_coords[x][y] >= 2:
            overlaps += 1

print(overlaps)
