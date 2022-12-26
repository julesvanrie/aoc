import sys
from aochelper import get_data

lines = get_data(sys.argv)

doubles = []

for i in range(int(len(lines) / 3)):
    group = lines[i*3:i*3+3]
    print(group)
    for char in group[0]:
        if char in group[1]:
            if char in group[2]:
                doubles.append(char)
                break

result = 0
for double in doubles:
    if double >= 'a':
        result += ord(double) - ord('a') + 1
    else:
        result += ord(double) - ord('A') + 27

print("The result is for part 2 is:", result)
