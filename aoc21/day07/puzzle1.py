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

for pos in range (min, max+1):
    fuel = sum([abs(crab - pos) for crab in crabs])
    if fuel_opt is None:
        fuel_opt = fuel
    else:
        if fuel < fuel_opt:
            fuel_opt = fuel
            pos_opt = pos

result = fuel_opt

print(f"Result is {result}")
