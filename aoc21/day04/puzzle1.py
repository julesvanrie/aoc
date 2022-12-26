with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

numbers = [int(nb) for nb in lines.pop(0).split(',')]
lines.pop(0)

dim = 5
lines = [[int(el) for el in line.split(' ') if el != '']
         for line in lines if line != '']

boards = [lines[i:i+dim] for i in range(0, len(lines), dim)]
nb_boards = len(boards)

results = [[[1 for _ in range(dim)] for _ in range(dim)] for _ in range(nb_boards)]

winning = None
win_number = None

for number in numbers:
    for bn, board in enumerate(boards):
        for rn, row in enumerate(board):
            for cn, item in enumerate(row):
                if item == number:
                    results[bn][rn][cn] = 0

        sum_columns = [0] * dim
        for rn, row in enumerate(results[bn]):
            if sum(row) == 0:
                winning = bn
                win_number = number
            for cn in range(dim):
                sum_columns[cn] += row[cn]
        for cn in range(dim):
            if sum_columns[cn] == 0:
                winning = bn
                win_number = number

    if winning:
        break

# Calculate score
score = 0
for r in range(dim):
    for c in range(dim):
        score += boards[winning][r][c] * results[winning][r][c]
score *= win_number

print(f"SCORE: {score}")
