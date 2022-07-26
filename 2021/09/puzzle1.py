with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

lines = [[int(letter) for letter in list(line)] for line in lines]

length = len(lines)
width = len(lines[0])

count = 0
for i, line in enumerate(lines):
    for j, digit in enumerate(line):
        lowest = True
        if i > 0:
            if lines[i-1][j] <= digit:
                lowest = False
        if i < length - 1:
            if lines[i+1][j] <= digit:
                lowest = False
        if j > 0:
            if line[j-1] <= digit:
                lowest = False
        if j < width - 1:
            if line[j+1] <= digit:
                lowest = False
        if lowest:
            count += digit + 1

result = count
print(f"Result is {result}")
