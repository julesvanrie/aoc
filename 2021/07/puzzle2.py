with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

crabs = [int(f) for f in lines[0].split(',')]

min = 1e6
max = 0
for crab in crabs:
    if crab < min:
        min = crab
    if crab > max:
        max = crab

pos_opt = None
fuel_opt = None

def fuel(crab, pos):
    # step = 1 if pos >= crab else -1
    fuels = []
    for i in range(1, abs(crab-pos)+1,1):
        fuels.append(i)
    return sum(fuels)

for pos in range(min, max + 1):
    fuel_sum = sum([fuel(crab,pos) for crab in crabs])
    if fuel_opt is None:
        fuel_opt = fuel_sum
    else:
        if fuel_sum < fuel_opt:
            fuel_opt = fuel_sum
            pos_opt = pos

result = fuel_opt

print(f"Result is {result}")
