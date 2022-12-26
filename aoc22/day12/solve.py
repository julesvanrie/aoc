import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')

    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')
    lines = [list(line) for line in lines]

    # Initiate height and width
    h = len(lines)
    w = len(lines[0])

    # Find start and end
    S = [None, None]
    E = [None, None]
    for i, line in enumerate(lines):
        try:
            S[1] = line.index('S',)
            S[0] = i
            E[1] = line.index('E')
            E[0] = i
        except:
            try:
                E[1] = line.index('E')
                E[0] = i
            except:
                continue

    # Set elevation of start and end
    lines[S[0]][S[1]] = 'a'
    lines[E[0]][E[1]] = 'z'

    # Search directions right, left, down, up
    dirs = [(0,1),(0,-1),(1,0),(-1,0),]

    # The Dijkstra
    def the_dijkstra(part):
        # Initiating distances and (un)visited
        distances = [[2**63 for _ in range(w)] for _ in range(h)]
        distances[E[0]][E[1]] = 0
        visited = [[False for _ in range(w)] for _ in range(h)]
        unvisited = [[y, x] for x in range(w) for y in range(h)]

        distance = 2**63   # Set distance to infinity (or something like it)
        found = False
        while not found:
            # Start with unvisited with shortest distance so far
            pos = sorted(unvisited, key=lambda c: distances[c[0]][c[1]])[0]
            for dir in dirs:    # Look in all directions
                y = pos[0] + dir[0]
                x = pos[1] + dir[1]
                # Check if within limits
                if x >= 0 and y >= 0 and x < w and y < h:
                    if visited[y][x]:
                        continue   # If already visited
                    # Check if direction is allowed
                    new = lines[y][x]
                    current = lines[pos[0]][pos[1]]
                    current_dist = distances[pos[0]][pos[1]]
                    if ord(new) >= ord(current) -1:
                        # Check if distance is lower than previously recorded
                        if distances[y][x] > current_dist + 1:
                            distances[y][x] = current_dist + 1
                        # If found we can stop
                        if part == 1:
                            if y == S[0] and x == S[1]:
                                found = True
                        if part == 2:
                            if lines[y][x] == 'a':
                                found = True
                        if found:
                            distance = distances[y][x]
                            break
            if found:
                break
            # If all directions investigated, this position has been fully visited
            unvisited.remove(pos)
            visited[pos[0]][pos[1]] = True

        return distance

    result1 = the_dijkstra(part=1)
    result2 = the_dijkstra(part=2)

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
