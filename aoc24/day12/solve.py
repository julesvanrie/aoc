import sys
from aocsolution.basesolution import BaseSolution

from itertools import product

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
diags = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

@BaseSolution.time_this
def solve_one(self):
    """Rather straightforward filling algorithm:
        1. Loop over all the spots (skip if visited before).
        2. Start with a new list of candidates (starting with only the start spot in the list).
        3. Repeat for each candidate:
            1. Add to list of visited spots
            2. Add neighbours with the same plants to candidates if they haven't been checked before
            3. Count number of neighbours with the same plant.
        4. Add 1 to area, and 4 minus number of neighbours to the perimeter.
        5. Back to 1.
    """
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    visited = [[False for _ in range(w)] for _ in range(h)]

    result = 0

    for y, x in product(range(h), range(w)):
        if visited[y][x]:
            continue
        a = 0; p = 0
        cands = {(y, x)}
        while cands:
            y, x = cands.pop()
            visited[y][x] = True
            neighbors = 0
            for dir in dirs:
                ny, nx = y + dir[0], x + dir[1]
                if (0 <= ny < h and 0 <= nx < w
                    and input[ny][nx] == input[y][x]
                    ):
                    neighbors += 1
                    if not visited[ny][nx]:
                        cands.add((ny, nx))
            a += 1
            p += 4 - neighbors

        result += a * p

    return result


@BaseSolution.time_this
def solve_two(self):
    """Putting a hedge around the farm is always a good idea

    Building on the previous solution, with some tweaks:
    - Extend our input with a border of '#'
      This avoids checking for out of bounds, but more importantly, it will make it easier to check for corners.
    - Add a part to check for corners: every corner adds 1 to the sides.
    """
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    area = [['#' for _ in range(w+2)] for _ in range(h+2)]
    for y, x in product(range(1, h+1), range(1,w+1)):
        area[y][x] = input[y-1][x-1]

    visited = [[False for _ in range(w+2)] for _ in range(h+2)]

    result_one = 0; result_two = 0

    for y, x in product(range(1, h+1), range(1,w+1)):
        if visited[y][x]:
            continue
        a = 0; p = 0; s = 0
        cands = {(y, x)}
        while cands:
            y, x = cands.pop()
            visited[y][x] = True
            neighbors = 0
            for dir in dirs:
                ny, nx = y + dir[0], x + dir[1]
                if (area[ny][nx] == area[y][x]
                    ):
                    neighbors += 1
                    if not visited[ny][nx]:
                        cands.add((ny, nx))
            # This is the new part, checking for corners
            for diag in diags:
                ny, nx = y + diag[0], x + diag[1]
                # Outside corner (base case for sides)
                if (area[ny][nx] != area[y][x]
                    and area[ny][x] != area[y][x]
                    and area[y][nx] != area[y][x]
                    ):
                    s += 1
                # Inside corner (add one extra side, the other side will be
                # counted because we'll have an extra outside corner)
                if (area[ny][nx] != area[y][x]
                    and area[ny][x] == area[y][x]
                    and area[y][nx] == area[y][x]
                    ):
                    s += 1
                # The diagonal case
                if (area[ny][nx] == area[y][x]
                    and area[ny][x] != area[y][x]
                    and area[y][nx] != area[y][x]
                    ):
                    s += 1

            a += 1
            p += 4 - neighbors

        result_one += a * p
        result_two += a * s

    return result_one, result_two


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 1 is:", solution.solve_two()[0])
    print("The result for part 2 is:", solution.solve_two()[1])
