with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

fish = [[int(f) for f in lines[0].split(',')]]

print(fish)
print(fish[-1])
for day in range(80):
    count_new_fish = sum([1 for f in fish[-1] if f == 0])
    fish.append([f - 1 if f != 0 else 6 for f in fish[-1]])
    fish[-1].extend([8] * count_new_fish)

result = len(fish[-1])

print(f"Result is {result}")
