import sys
from aocsolution.basesolution import BaseSolution

from itertools import product

dirs = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}

@BaseSolution.time_this
def solve_one(self):
    input = self.get_data(split=False)
    state, moves = input.split("\n\n")

    state = [[c for c in row[1:-1]] for row in state.split("\n")[1:-1]]
    moves = moves.replace("\n", "")

    h = len(state)
    w = len(state[0])

    for y, x in product(range(h), range(w)):
        if state[y][x] == "@":
            starty = y
            startx = x
            state[y][x] = "."
            break

    y = starty
    x = startx
    for move in moves:

        # Print intermediary states

        # print(y, x)
        # print("#" * (w+2))
        # for yd in range(h):
        #     # if yd == y:
        #     #     print("#" + "".join(state[yd][:x]) + "@" + "".join(state[yd][x+1:]) + "#")
        #     # else:
        #         print("#" + "".join(state[yd]) + "#")
        # print("#" * (w+2))
        # print()
        # print(move)

        try:
            dy, dx = dirs[move]
            if y + dy < 0 or y + dy >= h or x + dx < 0 or x + dx >= w:
                raise Exception
            if state[y + dy][x + dx] == "#":
                raise Exception
            if state[y + dy][x + dx] == ".":
                y += dy
                x += dx
                continue
            for i in range(1, h):
                if y + i*dy < 0 or y + i*dy >= h or x + i*dx < 0 or x + i*dx >= w:
                    raise Exception
                next = state[y + i*dy][x + i*dx]
                if next == ".":
                    state[y + i*dy][x + i*dx] = "O"
                    state[y][x] = "."
                    y += dy
                    x += dx
                    break
                if next == "#":
                    raise Exception
                if next == "0":
                    if state[y + (i+1)*dy][x + (i+1)*dx] == "#":
                        raise Exception
                    state[y + (i+1)*dy][x + (i+1)*dx] = "O"
                    state[y + i*dy][x + i*dx] = state[y+ (i-1)*dy][x + (i-1)*dx]
            state[y][x] = "."
        except:
            state[y][x] = "."

    result = 0
    for y, x in product(range(h), range(w)):
        if state[y][x] == "O":
            result += (y+1) * 100 + (x+1)

    # Print final state
    print("#" * (w+2))
    for yd in range(h):
            print("#" + "".join(state[yd]) + "#")
    print("#" * (w+2))

    return result


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data(split=False)
    state, moves = input.split("\n\n")

    state = [[c for c in row[1:-1]] for row in state.split("\n")[1:-1]]
    state = [[c for c in ".".join(row)] + ["."] for row in state]

    moves = moves.replace("\n", "")

    h = len(state)
    w = len(state[0])

    for y, x in product(range(h), range(w)):
        if state[y][x] == "@":
            starty = y
            startx = x
            state[y][x] = "."
            break

    y = starty
    x = startx
    for move in moves[:]:

        # Print intermediary states
        # print(y, x)
        # print("#" * (w+4))
        # for yd in range(h):
        #     line = "".join(state[yd])
        #     line = line.replace("O.", "[]")
        #     line = line.replace("#.", "##")
        #     if yd == y:
        #         print("##" + line[:x] + "@" + line[x+1:] + "##")
        #     else:
        #         print("##" + line + "##")
        #     if 'O' in line:
        #         return
        # print("#" * (w+4))
        # print()
        # print(move)

        try:
            dy, dx = dirs[move]
            if y + dy < 0 or y + dy >= h or x + dx < 0 or x + dx >= w:
                raise Exception
            if state[y + dy][x + dx] == "#" or state[y + dy][x + dx - 1] == "#":
                raise Exception
            if dx == 1 and state[y][x + 1] == ".":
                y += dy
                x += dx
                continue
            if dx == -1:
                if x == 1 and state[y][0] == ".":
                    y += dy
                    x += dx
                    continue
                if state[y][x - 2] == "." and state[y][x - 1] == ".":
                    y += dy
                    x += dx
                    continue
            if dy and state[y + dy][x] == "." and state[y + dy][x - 1] == ".":
                y += dy
                x += dx
                continue
            # We have a box
            if dy:
                if state[y + dy][x] == "O":
                    if can_move(y + dy, x, dy, dx, state):
                        move_it(y + dy, x, dy, dx, state)
                    else:
                        raise Exception
                else:
                    if can_move(y + dy, x-1, dy, dx, state):
                        move_it(y + dy, x-1, dy, dx, state)
                    else:
                        raise Exception
                y += dy
            elif dx == 1: # Moving right
                if can_move(y, x + 1, dy, dx, state):
                    move_it(y, x + 1, dy, dx, state)
                    x += dx
                else:
                    raise Exception
            else: # Moving left
                if x > 1 and can_move(y , x - 2, dy, dx, state):
                    move_it(y, x - 2, dy, dx, state)
                    x += dx
                else:
                    raise Exception

            state[y][x] = "."
        except Exception as E:
            state[y][x] = "."

    result = 0
    for ys, xs in product(range(h), range(w)):
        if state[ys][xs] == "O":
            y_dist = ys+1
            x_dist = xs + 2
            result += y_dist * 100 + x_dist

    # Print final state
    print("#" * (w+4))
    for yd in range(h):
        line = "".join(state[yd])
        line = line.replace("O.", "[]")
        line = line.replace("#.", "##")
        if yd == y:
            print("##" + line[:x] + "@" + line[x+1:] + "##")
        else:
            print("##" + line + "##")
    print("#" * (w+4))

    return result


def can_move(y, x, dy, dx, grid):
    # Vertical
    if dy:
        if y == 0 or y == len(grid):
            return False
        if '#' in grid[y + dy][x-1:x+2]:
            return False
        nexts = []
        if grid[y + dy][x] == 'O':
            nexts = [x]
        if grid[y + dy][x + 1] == 'O':
            nexts.append(x + 1)
        if grid[y + dy][x - 1] == 'O':
            nexts.append(x - 1)
        return all(map(lambda x: can_move(y + dy, x, dy, dx, grid), nexts))
    # Horizontal
    else:
        if x == 0 or x == len(grid[0]):
            return False
        if dx == -1 and x >= 1 and grid[y][x-1] == '#':
            return False
        if dx == 1 and grid[y][x+2] == '#':
            return False
        if x+2*dx >= 0 and grid[y][x+2*dx] == 'O':
            return can_move(y, x + 2*dx, dy, dx, grid)
        if x+2*dx >= 0 and grid[y][x+2*dx] == '.':
            return True
        if x == 1 and grid[y][0] == '.':
            return True


def move_it(y, x, dy, dx, grid):
    # Vertical
    if dy:
        if '#' in grid[y + dy][x:x+2]:
            return
        nexts = []
        if grid[y + dy][x] == 'O':
            nexts.append(x)
        if grid[y + dy][x + 1] == 'O':
            nexts.append(x + 1)
        if grid[y + dy][x - 1] == 'O':
            nexts.append(x - 1)
        if not nexts:
            print("Moving", y, x, dy, dx)
            grid[y + dy][x] = 'O'
            grid[y][x] = '.'
            return
        for next in nexts:
            move_it(y + dy, next, dy, dx, grid)
        move_it(y, x, dy, dx, grid)
    # Horizontal
    else:
        if dx == 1:
            if grid[y][x+2] == 'O':
                move_it(y, x + 2, dy, dx, grid)
            grid[y][x+1] = 'O'
            grid[y][x+2] = '.'
        else:
            if x - 2 > 0 and grid[y][x-2] == 'O':
                move_it(y, x - 2, dy, dx, grid)
            grid[y][x-1] = 'O'
            grid[y][x] = '.'
        grid[y][x] = '.'


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
