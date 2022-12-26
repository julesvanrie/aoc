with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

lines = [line.split(' ') for line in lines]
steps = []
for line in lines:
    action = 1 if line[0] == 'on' else 0
    tmp = line[1].split(',')
    x = [int(coord) for coord in tmp[0].split('=')[1].split('..')]
    y = [int(coord) for coord in tmp[1].split('=')[1].split('..')]
    z = [int(coord) for coord in tmp[2].split('=')[1].split('..')]
    steps.append([action, sorted(x), sorted(y), sorted(z)])

count = 0

def count_cuboid(coords):
    return (abs(coords[0][1]-coords[0][0]) + 1) \
         * (abs(coords[1][1]-coords[1][0]) + 1) \
         * (abs(coords[2][1]-coords[2][0]) + 1)

steps_result = []

def constrain(cuboid, constraints):
    # Check if cuboid within constraints, if not return None
    if  (cuboid[0][0] > constraints[0][1] or \
         cuboid[0][1] < constraints[0][0] or \
         cuboid[1][0] > constraints[1][1] or \
         cuboid[1][1] < constraints[1][0] or \
         cuboid[2][0] > constraints[2][1] or \
         cuboid[2][1] < constraints[2][0]):
        return None
    # Now constrain:
    result = [[
        max([cuboid[0][0], constraints[0][0]]),
        min([cuboid[0][1], constraints[0][1]]),
    ],
     [
         max([cuboid[1][0], constraints[1][0]]),
         min([cuboid[1][1], constraints[1][1]]),
     ],
     [
         max([cuboid[2][0], constraints[2][0]]),
         min([cuboid[2][1], constraints[2][1]]),
     ]]
    return result


def take_step(i, constraints=None):
    action = steps[i][0]
    cuboid = steps[i][1:]
    if constraints:
        cuboid_constrained = constrain(cuboid, constraints)
    else:
        cuboid_constrained = cuboid
    prior = 0
    add = 0
    overlap = 0
    if cuboid_constrained and action == 1:
        add = count_cuboid(cuboid_constrained)
    if i != 0:
        prior = take_step(i-1, constraints=constraints)
        if cuboid_constrained:
            overlap = take_step(i-1, constraints=cuboid_constrained)
    total = prior + add - overlap
    return total

result = take_step(len(steps) - 1)

# result = sum(steps_result)

print(f"Result for part 2 is {result}")
