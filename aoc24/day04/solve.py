import sys
from aocsolution.basesolution import BaseSolution


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    result = 0

    for y in range(h):
        # Horizontal
        line = input[y]
        result += count_xmas(line)
        # Diagonal 1
        line = ''.join(input[y+x][x] for x in range(0, h-y))
        result += count_xmas(line)
        # Diagonal 2
        line = ''.join(input[y+x][w-x] for x in range(0, h-y) if w - x < h)
        result += count_xmas(line)
    for x in range(w):
        # Vertical
        line = ''.join([input[y][x] for y in range(h)])
        result += count_xmas(line)
    for x in range(1,w):
        # Diagonal 1
        line = ''.join(input[y][x+y] for y in range(0, h) if x + y < w)
        result += count_xmas(line)
    for y in range(-h,0):
        # Diagonal 2
        line = ''.join(input[y+x][h-x] for x in range(0, h+1) if x + y >= 0)
        result += count_xmas(line)

    return result

def count_xmas(input):
    return input.count("XMAS") + input.count("SAMX")

@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    result = 0

    for y in range(1,h-1):
        for x in range(1,w-1):
            letters = ''.join([
                input[y-1][x-1],
                input[y-1][x+1],
                input[y][x],
                input[y+1][x-1],
                input[y+1][x+1]
            ])
            if letters in [
                'MSAMS',
                'SMASM',
                'MMASS',
                'SSAMM',
            ]:
                result += 1

    return result


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
