import sys
from aochelper import get_data

lines = get_data(sys.argv)

doubles = []
for line in lines:
    left = line[:int(len(line)/2)]
    right = line[int(len(line)/2):]
    for char in right:
        if char in left:
            doubles.append(char)
            break


result = 0
for double in doubles:
    if double >= 'a':
        result += ord(double) - ord('a') + 1
    else:
        result += ord(double) - ord('A') + 27

print("The result is for part 1 is:", result)
