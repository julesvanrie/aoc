with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

folds = [line[11:].split('=') for line in lines if len(line) > 10]
lines = [[int(coord) for coord in line.split(',')] for line in lines if len(line) >= 3 and len(line) < 10]

height = 0
width = 0
for line in lines:
    if line[0] > width:
        width = line[0]
    if line[1] > height:
        height = line[1]

dots = [[0 for i in range(height+1)] for j in range(width+1)]
for line in lines:
    dots[line[0]][line[1]] = 1

first = dots
for fold in folds[:1]:
    split = int(fold[1])
    if fold[0] == 'x':
        # width = len(dots)
        second = list(reversed(first[split+1:]))
        first = first[:split]
    if fold[0] == 'y':
        # height = len(dots[0])
        second = [list(reversed(line[split + 1:])) for line in first]
        first = [line[:split] for line in first]
    for i in range(len(first)):
        for j in range(len(first[0])):
            first[i][j] += second[i][j]

count = 0
for line in first:
    for dot in line:
        if dot > 0:
            count +=1


# print(first)

# print(len(lines))
# print(lines[0])

result = count

print(f"Number of dots is {result}")
