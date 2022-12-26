with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

lines = [[int(letter) for letter in list(line)] for line in lines]

length = len(lines)
width = len(lines[0])

basins = [[0 for j in range(width)] for i in range(length)]

def spread(i, j):
    # print("spread called", i, j)
    if j < width - 1:
        if lines[i][j + 1] != 9 and basins[i][j + 1] == 0:
            basins[i][j + 1] = basins[i][j]
            spread(i, j + 1)
    if j > 0:
        if lines[i][j - 1] != 9 and basins[i][j - 1] == 0:
            basins[i][j - 1] = basins[i][j]
            spread(i, j - 1)
    if i < length - 1:
        if lines[i + 1][j] != 9 and basins[i + 1][j] == 0:
            basins[i + 1][j] = basins[i][j]
            spread(i + 1,j)
    if i > 0:
        if lines[i - 1][j] != 9 and basins[i - 1][j] == 0:
            basins[i - 1][j] = basins[i][j]
            spread(i - 1, j)


    # for l in range(j+1, min(j+2,width)):
    #     if k == i and l == j:
    #         continue
    #     if lines[k][l] != 9:
    #         basins[k][l] = basins[i][j]
    #         spread(k, l)
    #     else:
    #         break
    # for l in range(j, max(j-1,0), -1):
    #     if k == i and l == j:
    #         continue
    #     if lines[k][l] != 9:
    #         basins[k][l] = basins[i][j]
    #         spread(k, l)
    #     else:
    #         break


basin_id = 1

for i, line in enumerate(lines):
    for j, digit in enumerate(line):
        if digit != 9:
            # basins[i, j] = count
            if basins[i][j] == 0:
                basins[i][j] = basin_id
                spread(i,j)
                basin_id += 1
                # if i > 0:
                #     neighbour = basins[i-1][j]
                #     if neighbour != 0:
                #         basins[i][j] = neighbour
                # if i < length - 1:
                #     neighbour = basins[i + 1][j]
                #     if neighbour != 0:
                #         basins[i][j] = neighbour
                # if j > 0:
                #     neighbour = basins[i][j - 1]
                #     if neighbour != 0:
                #         basins[i][j] = neighbour
                # if j < width - 1:
                #     neighbour = basins[i][j + 1]
                #     if neighbour != 0:
                #         basins[i][j] = neighbour
                # if basins[i][j] == 0:
                #     basins[i][j] = basin_id
                #     basin_id += 1
                # if basins[i][j] == 3:
                #     print(basins)

top_basin_sizes = {}

for i, line in enumerate(basins):
    # print(line)
    for j, basin in enumerate(line):
        if basin != 0:
            # print(i, j, basin)
            top_basin_sizes[basin] = top_basin_sizes.get(basin, 0) + 1

# print(basins)
# print(top_basin_sizes)

top = sorted(top_basin_sizes.values())

result = top[-1] * top[-2] * top[-3]

print(f"Result is {result}")
