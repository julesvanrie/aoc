with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

scanners = []
tmp = []
for line in lines:
    if line[:3] != "---":
        if line != "":
            parsed = [int(coord) for coord in line.split(',')]
            tmp.append(tuple(parsed))
        else:
            scanners.append(set(tmp))
            tmp = []
scanners.append(tmp)

def roll(point):
    return point[0], point[2], -point[1]

def turn_cw(point):
    return -point[1], point[0], point[2]

def turn_ccw(point):
    return point[1], -point[0], point[2]

def rotate_all(scanner):
    # Create list with all 24 rotations of a scanner
    rotations = []
    for roll_index in range(6):
        scanner = [roll(point) for point in scanner]
        rotations.append(set(scanner))
        for turn_index in range(3):
            if roll_index % 2 == 0:
                scanner = [turn_cw(point) for point in scanner]
            else:
                scanner = [turn_ccw(point) for point in scanner]
            rotations.append(set(scanner))
    return rotations

def move(scanner, x, y, z):
    return set([(point[0] + x, point[1] + y, point[2] + z) for point in scanner])

def compare(scanner_fixed, scanner_two):
    for rotation in rotate_all(scanner_two):
        for point_fix in scanner_fixed:
            for point_float in rotation:
                x = point_fix[0] - point_float[0]
                y = point_fix[1] - point_float[1]
                z = point_fix[2] - point_float[2]
                scanner_two_moved = move(rotation, x, y, z)
                # print(scanner_two_moved)
                # print(fixed)
                intersect = scanner_fixed.intersection(scanner_two_moved)
                # if len(intersect) > 5:
                #     print(intersect)
                if len(intersect) >= 6:
                    return scanner_two_moved, (x, y, z)
    return None


scanners_abs = [scanners[0]]
scanner_locations = [(0,0,0)]
scanners_linked = [0]
while len(scanners_abs) < len(scanners):
    for i, scanner in enumerate(scanners):
        if i in scanners_linked:
            continue
        found = None
        for fixed in scanners_abs:
            found = compare(fixed, scanner)
            if found:
                scanners_abs.append(found[0])
                scanner_locations.append(found[1])
                scanners_linked.append(i)
                break
        if found:
            continue

beacons = set()
for scanner in scanners_abs:
    beacons = beacons.union(scanner)


# print(len(set(beacons)))
# print(len(s))
# print(len(s[2]))
# print(len(s[2][0]))

result = len(beacons)

print(f"Result for part 1 is {result}")


def manhattan(one, two):
    return abs(one[0] - two[0]) + abs(one[1] - two[1]) + abs(one[2] - two[2])

max_distance = 0
for i, one in enumerate(scanner_locations):
    for j, two in enumerate(scanner_locations):
        if manhattan(one, two) > max_distance:
            max_distance = manhattan(one, two)

for scanner in scanner_locations:
    print(scanner)

print(f"Result for part 2 is {max_distance}")
