import sys
from aocsolution.basesolution import BaseSolution

from heapq import heappush, heappop

dirs = [(0,1), (0,-1), (1,0), (-1,0)]

@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    stop = 1024 if len(input) > 1024 else 12
    return solve(input, stop)

def solve(input, stop):
    h = 71 if len(input) > 1024 else 7
    w = 71 if len(input) > 1024 else 7

    result = 0

    corrupts = [line.split(',') for line in input]
    corrupts = [(int(y), int(x)) for x, y in corrupts]

    # Display the grid
    # for y in range(h):
    #     print(''.join('.' if (y,x) not in corrupts[:stop] else '#' for x in range(w)))

    cands = []
    heappush(cands, (0, (0,0)))
    visited = []

    while cands:
        print(len(cands), end='\r')
        cost, (y, x) = heappop(cands)
        visited.append((y,x))
        for dy, dx in dirs:
            if (0 <= y+dy < h and
                0 <= x+dx < w and
                (y+dy, x+dx) not in visited and
                (y+dy, x+dx) not in corrupts[:stop]
                ):
                if (y+dy, x+dx) == (h-1, w-1):
                    result = cost + 1
                    return result
                if (new := (cost+1, (y+dy, x+dx))) not in cands:
                    heappush(cands, new)


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()

    for stop in range(len(input)-1, 0, -1):
        if solve(input, stop):
            print("Blocked after", stop, "of bytes")
            return input[stop]


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
