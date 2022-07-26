with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

fish = [int(f) for f in lines[0].split(',')]

print(fish)

f_class = {}

for f in fish:
    f_class[f] = f_class.get(f, 0) + 1

print(f_class)
for day in range(256):
    count_new_fish = f_class.get(0, 0)
    for f in range(8):
        if f == 6:
            f_class[f] = count_new_fish + f_class.get(f+1,0)
        else:
            f_class[f] = f_class.get(f + 1, 0)
    f_class[8] = count_new_fish
    print(f_class)

result = sum(f_class.values())

print(f"Result is {result}")
