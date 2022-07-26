with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

movements = [line.split(' ') for line in lines]

forward = sum(
    [int(movement[1]) for movement in movements if movement[0] == "forward"])

down = sum(
    [int(movement[1]) for movement in movements if movement[0] == "down"])

up = sum(
    [int(movement[1]) for movement in movements if movement[0] == "up"])

depth = down - up

result = forward * depth

print(f"Result is {result}")
