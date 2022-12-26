with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

movements = [line.split(' ') for line in lines]

aim = 0
horiz = 0
verti = 0

for movement in movements:
    move = movement[0]
    quant = int(movement[1])
    if move == "forward":
        horiz += quant
        verti += quant * aim
    elif move == "down":
        aim += quant
    elif move == "up":
        aim -= quant

result = horiz * verti

print(f"Result is {result}")
