import sys
from aocsolution.basesolution import BaseSolution

from itertools import product
from functools import cache

num_locs = {
    '7': (0, 0), '8': (0, 1), '9': (0, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
    '0': (3, 1), 'A': (3, 2),
}
num_locs_rev = {v: k for k, v in num_locs.items()}

dirs = {(-1,  0): '^', ( 0, +1): '>', (+1,  0): 'v', ( 0, -1): '<'}
dirs_rev = {v: k for k, v in dirs.items()}

def get_moves(s, e):
    ''''Returns all potential moves between two buttons on a numeric keypad

    Recursive: moves first to a button in the direction of the target button.
    If not at the target button, it then calls itself to move to the next button.
    '''
    if s == e:
        return [['']]

    start = num_locs[s]
    end = num_locs[e]

    # Determine the directions to move into.
    # Only go in the direction of the target button. Going in the opposite direction
    # will only be suboptimal.
    pot_dirs = []
    if start[0] < end[0]:
        pot_dirs.append(dirs_rev['v'])
    elif start[0] > end[0]:
        pot_dirs.append(dirs_rev['^'])
    if start[1] < end[1]:
        pot_dirs.append(dirs_rev['>'])
    elif start[1] > end[1]:
        pot_dirs.append(dirs_rev['<'])

    y, x = start

    # Explore each of the candidates
    paths = []
    for dy, dx in pot_dirs:
        ny, nx = y + dy, x + dx
        # Skip if out of bounds or on the forbidden button
        if (ny < 0 or nx < 0 or
            ny > 3 or nx > 2 or
            (ny, nx) == (3, 0)
            ):
            continue
        # If we are at the target button, append the move
        # Else call the function recursively to move to the next button
        if num_locs_rev[(ny, nx)] == e:
            paths.append([(dy, dx)])
        else:
            paths.extend([[(dy, dx)] + move for move in get_moves(num_locs_rev[(ny, nx)], e)]) #, so_far + [(dy, dx)]))

    return paths

def get_all_moves():
    '''Returns all potential moves between all buttons on a numeric keypad.
    Returns as a dictionary with keys as the start and end buttons and values as a list of potential moves.
    The moves are a string of directions.
    '''
    moves_coord = {(s, e): get_moves(s, e)
            for s, e in product(num_locs.keys(), repeat=2) if s != e}
    return {k: [''.join(dirs[d] for d in path) for path in paths]
            for k, paths in moves_coord.items()}

# All potential moves between all buttons on a numeric keypad
all_moves = get_all_moves()

# All potential moves between all buttons on a directional keypad
# Hardcoded seemed easier than trying to figure out a general solution
robot_moves = {
    ('A', 'A'): [''],
    ('^', '^'): [''],
    ('v', 'v'): [''],
    ('>', '>'): [''],
    ('<', '<'): [''],
    ('A', '^'): ['<'],
    ('A', '>'): ['v'],
    ('A', 'v'): ['<v', 'v<'],
    ('A', '<'): ['v<<', '<v<'],
    ('^', 'A'): ['>'],
    ('^', 'v'): ['v'],
    ('^', '>'): ['v>', '>v'],
    ('^', '<'): ['v<'],
    ('v', 'A'): ['>^', '^>'],
    ('v', '^'): ['^'],
    ('v', '<'): ['<'],
    ('v', '>'): ['>'],
    ('>', 'A'): ['^'],
    ('>', '<'): ['<<'],
    ('>', '^'): ['^<', '<^'],
    ('>', 'v'): ['<'],
    ('<', 'A'): ['>>^', '>^>'],
    ('<', '>'): ['>>'],
    ('<', 'v'): ['>'],
    ('<', '^'): ['>^'],
}


@BaseSolution.time_this
def solve_one(self):
    return self.solve(2)


@BaseSolution.time_this
def solve_two(self):
    return self.solve(25)


def solve(self, nb_iters):
    input = self.get_data()

    result = 0

    for line in input:
        # Get the first directional level. Adding 'A' because that's where we start from.
        # This returns a list of all potential paths to form the numeric code.
        paths = get_nexts('A' + line)
        shortest = 2**63
        for path in paths:
            # Adding 'A' because that's where we start from
            full = 'A' + path
            # Calculate the length of the path:
            # - Get the distance between each button in the first directional path
            #   To do that: call the recursive function get_dist
            # - Sum those up
            length = sum(get_dist(full[i], full[i + 1], nb_iters) for i in range(len(full) - 1))
            if length < shortest:
                shortest = length
        complexity = shortest * int(line[:3])

        result += complexity

    return result


@cache
def get_nexts(path):
    '''Starting from a numeric code, returns all potential directional paths to
    form the code.

    Recursive function that moves from one button to the next, and then calls
    itself for the remainder of the code.

    '''
    if len(path) == 1:
        return ['']
    paths = []
    # Figure out the potential moves from the first button to the second
    for move in all_moves[(path[0], path[1])]:
        # For each of these moves, call the function recursively and find all
        # potential paths from the second button to the end of the code
        paths.extend([
            move + 'A' + new_move for new_move in get_nexts(path[1:])
        ])
    return paths


@cache
def get_dist(s, e, level):
    '''Returns the distance between two buttons on a directional keypad at a given level.

    Recursive function that determines the potential paths on this level, and then
    calls itself for each move in the path to get the distance at the next level.

    Returns the shortest distance between the two buttons.

    If at level 0, the lenght is just one key press.
    '''
    if level == 0:
        return 1
    lengths = []
    paths = robot_moves[(s, e)]
    for path in paths:
        # Adding 'A' because on a directional pad we should always go from 'A' to 'A'
        full = 'A' + path + 'A'
        length = sum(get_dist(full[i], full[i + 1], level - 1) for i in range(len(full) - 1))
        lengths.append(length)
    return min(lengths)


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two
    solve = solve


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
