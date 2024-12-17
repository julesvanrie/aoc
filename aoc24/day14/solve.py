import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    h = 7 if self.test else 103
    w = 11 if self.test else 101
    it = 100

    result = 0

    pattern = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")

    robots = [[int(el) for el in pattern.findall(line)[0]] for line in input]

    # pprint(robots)

    final = [((robot[0] + robot[2] * it) % w,
              (robot[1] + robot[3] * it) % h)
             for robot in robots]

    # pprint(final)


    # grid = [[0 for _ in range(w)] for _ in range(h)]

    # for robot in final:
    #     grid[robot[1]][robot[0]] += 1

    # for y in range(h):
    #     for x in range(w):
    #         if p := grid[y][x]:
    #             print(grid[y][x], end="")
    #         else:
    #             print(".", end="")
    #     print()

    one, two, three, four = 0, 0, 0, 0



    for robot in final:
        if robot[0] < w // 2:
            if robot[1] < h // 2:
                one += 1
                # print(1, robot)
            elif robot[1] > h // 2:
                three += 1
                # print(3, robot)
            else:
                pass
                # print(0, robot)
        elif robot[0] > w // 2:
            if robot[1] < h // 2:
                two += 1
                # print(2, robot)
            elif robot[1] > h // 2:
                four += 1
                # print(4, robot)
            else:
                # print(0, robot)
                pass
        else:
            # print(0, robot)
            pass

    return one * two * three * four

# 100379268 too low
# 230686500


@BaseSolution.time_this
def solve_two(self):
    inp = self.get_data()
    h = 7 if self.test else 103
    w = 11 if self.test else 101
    it = 0

    result = 0

    pattern = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")

    robots = [[int(el) for el in pattern.findall(line)[0]] for line in inp]


    while True:

        final = [((robot[0] + robot[2] * it) % w,
                (robot[1] + robot[3] * it) % h)
                for robot in robots]


        grid = [[0 for _ in range(w)] for _ in range(h)]

        for robot in final:
            grid[robot[1]][robot[0]] += 1

        # print(it, end='\r')

        for y in range(h):
            for x in range(w):
                if (grid[y//2+0][x//2+0] and
                    grid[y//2-1][x//2+0] and
                    grid[y//2+1][x//2+0] and
                    grid[y//2+1][x//2+1] and
                    grid[y//2+0][x//2+1] and
                    grid[y//2-1][x//2+1] and
                    grid[y//2+1][x//2-1] and
                    grid[y//2+0][x//2-1] and
                    grid[y//2-1][x//2-1]):

                    # print()
                    for y in range(h):
                        for x in range(w):
                            if p := grid[y][x]:
                                print(grid[y][x], end="")
                            else:
                                print(".", end="")
                        print()


                    return it
        it += 1




class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
