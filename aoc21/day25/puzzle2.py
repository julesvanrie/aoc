with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

initial = [[d for d in line] for line in lines]
height = len(initial)
width = len(initial[0])

step_count = 0


def can_move(direction, state):
    moves = []
    for x in range(width):
        for y in range(height):
            if state[y][x] == '.':
                continue
            if direction == 'west':
                cucumber = '>'
                new_x = x + 1 if x < width - 1 else 0
                new_y = y
            elif direction == 'south':
                cucumber = 'v'
                new_x = x
                new_y = y + 1 if y < height - 1 else 0
            if state[y][x] == cucumber:
                if state[new_y][new_x] == '.':
                    moves.append((x, y))
    # print(moves)
    return moves


def move(direction, state, moves):
    for move in moves:
        x = move[0]
        y = move[1]
        if direction == 'west':
            new_x = x + 1 if x < width - 1 else 0
            new_y = y
        elif direction == 'south':
            new_x = x
            new_y = y + 1 if y < height - 1 else 0
        state[new_y][new_x] = state[y][x]
        state[y][x] = '.'
    return state


def step(state, max_step=None):
    has_moved = False
    for direction in ['west', 'south']:
        moves = can_move(direction, state)
        if len(moves) > 0:
            state = move(direction, state, moves)
            has_moved = True
    global step_count
    step_count += 1
    if has_moved:
        # print('')
        # for line in state:
        #     print(''.join(line))
        if max_step is None or step_count < max_step:
            step(state, max_step)
    return


# for line in initial:
#     print(''.join(line))

step(initial)

result = step_count

print(f"Result for part 1 is {result}")
