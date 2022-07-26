from copy import deepcopy
from termcolor import colored

with open('test.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

height = len(lines)
width = max([len(line) for line in lines])


max_depth = 32

initial = [[d for d in line] for line in lines]
for line in initial:
    for space in range(len(line), width):
        line.append(' ')


tried = []

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

close_hallway = {
    'A': [2,1,4,6,8,10,11],
    'B': [4,2,1,6,8,10,11],
    'C': [6,8,10,11,4,2,1],
    'D': [10,11,8,6,4,2,1]
}

min_cost = 30_000

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

def list_potential_moves(spaces):
    moves = []
    # loop through sideroom and push into other sideroom
    for x in [9,7,5,3]:
        if spaces[3][x] == target[x]:
            if spaces[2][x] == target[x]:
                continue
            else:
                y_s = [2]
        else:
            y_s = [3, 2]
        for y in y_s:
            point = spaces[y][x]
            if point == '.':
                continue
            if y == 3:
                if spaces[2][x] != '.':
                    continue
            for y_ in [3,2]:
                x_ = target_rev[point]
                if x_ != x:
                    if can_go_into_room(spaces, x, y, x_, y_):
                        moves.append((point, x, y, x_, y_))
                        break # only go to deepest spot
    # then try to empty hallway
    y = 1
    for x in [6,4,8,2,10,1,11]:
        point = spaces[y][x]
        if point == '.':
            continue
        x_ = target_rev[point]
        for y_ in [3,2]:
            if can_go_into_room(spaces, x, y, x_, y_):
                moves.append((point, x, y, x_, y_))
                break # only go to deepest spot
    # loop through siderooms and push into hallway
    for x in [9,7,5,3]:
        if spaces[3][x] == target[x]:
            if spaces[2][x] == target[x]:
                continue
            else:
                y_s = [2]
        else:
            y_s = [2, 3]
        for y in y_s:
            point = spaces[y][x]
            if point == '.':
                continue
            if y == 3:
                if spaces[2][x] != '.':
                    continue
            y_ = 1
            for x_ in close_hallway[point]:
                if spaces[y_][x_] != '.':
                    continue
                if hallway_free(spaces, x, x_):
                    moves.append((point, x, y, x_, y_))
    return moves

def make_move(spaces, move):
    new_spaces = deepcopy(spaces)
    new_spaces[move[2]][move[1]] = '.'
    new_spaces[move[4]][move[3]] = move[0]
    return new_spaces

def encoded(spaces, move):
    tmp = ''
    for x in range(1, width-1):
        tmp += spaces[1][x]
    for x in [3,5,7,9]:
        for y in [2,3]:
            tmp += spaces[y][x]
    tmp += ''.join([str(m) for m in move])
    return tmp


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
        if spaces[2][x] != target[x]:
            return False
        if spaces[3][x] != target[x]:
            return False
    return True

def find_solution(previous_state, cost_start = 0, depth=0):
    # costs = [2**64]
    # print('-----------------')
    # global depth_reached
    # print(depth)
    # if depth > depth_reached:
    #     depth_reached = depth
    # if depth > max_depth:
    #     return
    global min_cost
    global max_depth
    if depth > max_depth:
        return
    global tried
    if cost_start > min_cost:
        return
    spaces = deepcopy(previous_state)
    moves = list_potential_moves(spaces)
    if not moves:
        return
    for move in moves:
        # global steps
        # steps += 1
        # if steps > max_steps:
        #     return
        # path_new = deepcopy(path)
        # path_new.append(move)
        # if path_new in tried:
        #     continue
        # print(colored('path: ', 'red'), path_new)
        # print(colored('tried: ', 'green'), tried)
        spaces_new = make_move(spaces, move)
        cost = cost_start + cost_move(move)
        if (spaces_new, cost) in tried:
            continue
        if cost > min_cost:
            tried.append((spaces_new, cost))
            continue
        # print(depth, move, cost)
        # if cost > min_cost:
        #     continue
        # enc = encoded(spaces_new, move)
        # if enc in tried:
        #     continue
        # tried.append(enc)
        # for line in spaces_new:
        #     print(''.join(line))
        # print(enc)
        # print(min(min_costs))
        # for line in locks_new:
        #     print(''.join(['#' if d else '.' for d in line]))
        if all_valid(spaces_new):
            # global successes
            # successes += 1
            if cost < min_cost:
                min_cost = cost
            print(colored("found one", 'green'), cost)
            tried.append((spaces_new, cost))
            break
        else:
            # depth += 1
            find_solution(spaces_new, cost, depth+1)
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
result = min_cost

print(f"Result for part 1 is {result}")
