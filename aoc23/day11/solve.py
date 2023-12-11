import sys
from aocsolution.basesolution import BaseSolution

@BaseSolution.time_this
def solve(input, expansion):
    h = len(input)
    w = len(input[0])

    # Store a list of (y, x) for the galaxies
    galaxies = []
    # Store an array (size = input) and all 1s,
    # unless it's an empty row or column,
    # then it contains the expansion (e.g. 2)
    space = []
    # Check the rows for galaxies
    # If no galaxy, expand
    # If a galaxy, store its coordinates
    for y, line in enumerate(input):
        if '#' in line:
            # A galaxy on the line, so space is 1
            space.append([1]*len(line))
            for x, c in enumerate(line):
                if c == '#':
                    # A galaxy, store its (y,x)
                    galaxies.append((y,x))
        else:  # No galaxy, so expand (store expansion i.o. 1)
            space.append([expansion] * w)

    # Check the columns for galaxies
    # If no galaxy, expand
    for x in range(w):
        if not '#' in [input[y][x] for y in range(h)]:
            # Replace the existing 1 by expansion
            for y in range(h):
                space[y][x] = expansion

    # For every combination of 2 galaxies, store distance
    # Distances are actually simple Manhattan distances
    # At least if we take the expansion (i.o. 1) where needed
    distances = []
    for gay, gax in galaxies:
        for gby, gbx in galaxies:
            # Horizontal distance
            if gax == gbx:
                dx = 0
            else:
                # Sum all the spaces horizontally between the
                # columns of the two galaxies
                dir = int((gbx-gax)/abs(gbx-gax))
                dx = sum(space[gay][gax:gbx:dir])
            # Vertical distance
            if gay == gby:
                dy = 0
            else:
                # Sum all the spaces vertically between the
                # rows of the two galaxies
                dir = int((gby-gay)/abs(gby-gay))
                dy = sum(space[y][gax] for y in range(gay,gby,dir))
            distances.append(dx + dy)

    # We just double counted all pairs of galaxies
    # So sum them up, but divide by 2
    return sum(distances) // 2

@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    return solve(input=input, expansion=2)


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    return solve(input=input, expansion=1_000_000)


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
