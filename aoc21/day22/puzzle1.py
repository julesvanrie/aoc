with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

lines = [line.split(' ') for line in lines]
steps = []
for line in lines:
    tmp = line[1].split(',')
    x = [int(coord) for coord in tmp[0].split('=')[1].split('..')]
    y = [int(coord) for coord in tmp[1].split('=')[1].split('..')]
    z = [int(coord) for coord in tmp[2].split('=')[1].split('..')]
    steps.append([line[0], sorted(x), sorted(y), sorted(z)])

for step in steps:
    print(step)

size = 50
reactor = [[[0 for i in range(-size,size+1)] for j in range(-size,size+1)] for k in range(-size,size+1)]

def take_step(step):
    new_state = 1 if step[0] == 'on' else 0
    all_range = step[1:]
    x_range = step[1]
    y_range = step[2]
    z_range = step[3]
    if max(max(all_range)) > size or min(min(all_range)) < -size:
        # print("too large")
        return
    for x in range(x_range[0], x_range[1] + 1):
        for y in range(y_range[0], y_range[1] + 1):
            for z in range(z_range[0], z_range[1] + 1):
                if abs(x) <= size and abs(y) <= size and abs(z) <= size:
                    reactor[x+size][y+size][z+size] = new_state
    return

def count(reactor):
    return sum([sum([sum(line) for line in plane]) for plane in reactor])


# print(len(reactor))

# print(reactor[20+size][0+size][0+size])
for step in steps:
    take_step(step)
    # print(reactor[20+size][0+size][0+size])
    # print(count(reactor))

result = count(reactor)

print(f"Result for part 1 is {result}")
