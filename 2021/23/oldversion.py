from copy import deepcopy
from termcolor import colored

with open('test.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

height = len(lines)
width = max([len(line) for line in lines])

initial = [[d for d in line] for line in lines]
for line in initial:
    for space in range(len(line), width):
        line.append(' ')


costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

target = {
        3: 'A',
        5: 'B',
        7: 'C',
        9: 'D'
}

target_rev = {
    'A': 3,
    'B': 5,
    'C': 7,
    'D': 9
}

min_costs = [2**64]

def hallway_free(spaces, x1, x2):
    if x1 < x2:
        min_x = x1 + 1
        max_x = x2 + 1
    if x1 > x2:
        min_x = x2
        max_x = x1
    return all([spot == '.' for spot in spaces[1][min_x:max_x]])

def can_go_into_room(spaces, x1, y1, x2, y2):
    if y1 > 2:
        if spaces[y1-1][x1] != '.':
            return False
    if hallway_free(spaces, x1, x2):
        if spaces[y2-1][x2] == '.':
            if spaces[y2][x2] == '.':
                return True
    return False

def list_potential_moves(spaces, previous_spaces):
    moves = []
    # loop through sideroom and push into other sideroom
    for x in [3,5,7,9]:
        for y in [3,2]:
            point = spaces[y][x]
            if point in ['#', '.', ' ']:
                continue
            if y == 3:
                if spaces[3][x] == target[x]:
                    continue
                if spaces[2][x] != '.':
                    continue
            elif spaces[2][x] == target[x]:
                if spaces[3][x] == target[x]:
                    continue
            # if not locked yet
            # if locks[y][x]:
            #     continue
            # if not a letter
            # if surrounded:
            # surroundings = [spaces[y][x-1], spaces[y][x+1], spaces[y-1][x], spaces[y+1][x]]
            # if '.' not in surroundings:
            #     continue
            # if in hallway
            # if in a room
            for y_ in [3,2]:
                x_ = target_rev[point]
                if x_ != x:
                    if can_go_into_room(spaces, x, y, x_, y_):
                        moves.append((point, x, y, x_, y_))
                        return moves
    # then try to empty hallway
    y = 1
    for x in range(1, width-1):
        point = spaces[y][x]
        if point in ['#', '.', ' ']:
            continue
        # if surrounded:
        # surroundings = [spaces[y][x-1], spaces[y][x+1], spaces[y-1][x], spaces[y+1][x]]
        # if '.' in surroundings:
        x_ = target_rev[point]
        for y_ in [3,2]:
            if can_go_into_room(spaces, x, y, x_, y_, previous_spaces):
                moves.append((point, x, y, x_, y_))
                return moves
                break # only go to deepest spot
    # loop through siderooms and push into hallway
    for x in [3,5,7,9]:
        for y in [3,2]:
            point = spaces[y][x]
            if point in ['#', '.', ' ']:
                continue
            if y == 3:
                if spaces[2][x] != '.':
                    continue
                if spaces[3][x] == target[x]:
                    continue
            elif spaces[2][x] == target[x]:
                if spaces[3][x] == target[x]:
                    continue
            # if not locked yet
            # if locks[y][x]:
            #     continue
            # if not a letter
            # if surrounded:
            # surroundings = [spaces[y][x-1], spaces[y][x+1], spaces[y-1][x], spaces[y+1][x]]
            # if '.' not in surroundings:
            #     continue
            # if in hallway
            # if in a room
            # to hallway but not above
            y_ = 1
            for x_ in range(1, width-1):
                if x_ in [3,5,7,9]:
                    continue
                if spaces[y_][x_] != '.':
                    continue
                if hallway_free(spaces, x, x_):
                    moves.append((point, x, y, x_, y_))
                    return moves
    return moves

def make_move(spaces, move):
    new_spaces = deepcopy(spaces)
    new_spaces[move[2]][move[1]] = '.'
    new_spaces[move[4]][move[3]] = move[0]
    # if move[4] != 1:
    #     new_locks[move[4]][move[3]] = True
    return new_spaces

def cost_move(move):
    unit_cost = costs[move[0]]
    # cost of lateral
    units = abs(move[3]-move[1])
    # cost of vertical
    units += abs(move[2]-1)
    units += abs(move[4]-1)
    return units * unit_cost

def all_valid(spaces):
    for x in [3,5,7,9]:
        if spaces[2][x] == '.':
            return False
        if spaces[2][x] != spaces[3][x]:
            return False
    return True

def find_solution(previous_state, cost_start = 0):
    # costs = [2**64]
    # print('-----------------')
    # global depth_reached
    # print(depth)
    # if depth > depth_reached:
    #     depth_reached = depth
    # if depth > max_depth:
    #     return
    spaces = deepcopy(previous_state)
    moves = list_potential_moves(spaces, previous_state)
    # print(moves)
    # print('')
    if not moves:
        return
    for move in moves:
        # global steps
        # steps += 1
        # if steps > max_steps:
        #     return
        cost = cost_start + cost_move(move)
        if cost > min(min_costs):
            continue
        # print(depth, move, cost)
        # if cost > min_cost:
        #     continue
        spaces_new = make_move(spaces, move)
        # print(min(min_costs))
        # for line in spaces_new:
        #     print(''.join(line))
        # for line in locks_new:
        #     print(''.join(['#' if d else '.' for d in line]))
        if all_valid(spaces_new):
            # global successes
            # successes += 1
            if cost < min(min_costs):
                min_costs.append(cost)
            # min_cost = cost
            print(colored("found one", 'green'), cost)
            break
            # break
            # quit()
            # account for total cost
            # save path as tried
            # try something else
        else:
            # depth += 1
            find_solution(spaces_new, cost)
            # depth -= 1
            # if new_cost:
            #     min_cost = cost + new_cost
            # else:
            #     continue
    return

find_solution(initial)



# print(successes)
# print(max_depth)
# print(steps)
result = min(min_costs)

print(f"Result for part 1 is {result}")
