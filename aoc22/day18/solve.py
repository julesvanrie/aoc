import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')

    coords = [[int(c) for c in line.split(',')] for line in lines]


    def surface(coords):
        # Start from assuming all coords are not connected
        # Each coord has surface 6 if they are not connected
        base = len(coords) * 6
        # Loop over all coords. If they have a common side, subtract 2
        for i, a in enumerate(coords):
            for b in coords[i+1:]:
                if (
                    a[0] == b[0] and a[1] == b[1] and abs(a[2] - b[2]) == 1
                    or a[0] == b[0] and a[2] == b[2] and abs(a[1] - b[1]) == 1
                    or a[1] == b[1] and a[2] == b[2] and abs(a[0] - b[0]) == 1
                    ):
                    base -= 2
        return base


    def bounds(coords):
        return [max(c[i] for c in coords) + 2 for i in [0,1,2]]


    def part2(coords):
        maxx, maxy, maxz = bounds(coords)
        matrix = [[[' ' for z in range(maxz)]
                        for y in range(maxy)]
                        for x in range(maxx)]
        # Point 0 is outside the block of lava
        matrix[0][0][0] = '.'
        # - Loop over all points to check if they are connected to point 0
        #   in which case they are also outside the block of lava.
        # - Repeat this a couple of times until number of holes converged.
        # - Reason is that we only do a one pixel deep search and thus we do
        #   not immediately catch all outside points.
        #      Outside points marked as '.'
        #      Inside points marked as  ' '
        #      Lava blocks marked as    '#'
        holes = []
        prev_holes = maxx * maxy * maxz
        while len(holes) != prev_holes:
            # Loop over all x, y, z in space (within the max bounds)
            for x in range(maxx):
                for y in range(maxy):
                    for z in range(maxz):
                        # Skip pixels inside the lava block, mark as #
                        if [x,y,z] in coords:
                            matrix[x][y][z] = '#'
                            continue
                        # Look in all six directions
                        for dir in [ [+1,0,0], [0,+1,0], [0,0,+1],
                                    [-1,0,0], [0,-1,0], [0,0,-1], ]:
                            # Make sure we're not looking outside of bounds
                            if (   x + dir[0] < 0 or x + dir[0] >= maxx
                                or y + dir[1] < 0 or y + dir[1] >= maxy
                                or z + dir[2] < 0 or z + dir[2] >= maxz
                                ):
                                continue
                            # If one direction is outside, then this point is outside
                            if matrix[x + dir[0]][y + dir[1]][z + dir[2]] == '.':
                                matrix[x][y][z] = '.'
                                break
            # Save length of previous run to check convergence in while condition
            prev_holes = len(holes)
            # Create list of new holes coordinates
            holes = []
            for x in range(maxx):
                for y in range(maxy):
                    for z in range(maxz):
                        if matrix[x][y][z] == ' ':
                            holes.append([x,y,z])

            # show(matrix)
        # Calculate surface as in part 1 and subtract surface of holes
        return surface(coords) - surface(holes)


    def show(matrix):
        for x in range(maxx):
            for y in range(maxy):
                for z in range(maxz):
                    print(matrix[x][y][z], end='')
                print('')
            print('')
        print('')


    result1 = surface(coords)
    result2 = part2(coords)

    print("The result is for part 1 is:", result1)
    print("The result is for part 2 is:", result2)

    return result1, result2

def time():
    with open(os.devnull, 'w') as out:
        sys.stdout = out
        number = 20
        timing = timeit.timeit(solve, number=number) / number
        sys.stdout = sys.__stdout__
    print(f"This took {timing:.6f} seconds")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1][:4] == "time":
        del sys.argv[1]
        time()
    else:
        solve()
