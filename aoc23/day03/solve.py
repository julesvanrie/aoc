import sys
from aocsolution.basesolution import BaseSolution

import re

class Solution(BaseSolution):

    @BaseSolution.time_this
    def solve_one(self):
        result = 0
        input = self.get_data()
        # Add some padding to remove some (literal) edge cases
        length = len(input[0])
        input = ['.'*length] + input + ['.'*length]
        input = ['.' + row + '.' for row in input]
        for i, line in enumerate(input[1:-1], 1):
            for n in re.finditer(r"\d+", line):   # Loop over all the numbers
                # Put everything in the surrounding area in a string
                # and check that it only has dots.
                surround = line[n.start()-1] + line[n.end()]   # Left and right
                for row in [i-1,i+1]:                          # Up and down
                    surround += input[row][n.start()-1:n.end()+1]
                if surround.replace('.', ''):   # Result not empty,
                    result += int(n.group())    # so it's a part
        return result

    @BaseSolution.time_this
    def solve_two(self):
        result = 0
        input = self.get_data()
        # Add some padding to remove some (literal) edge cases
        length = len(input[0])
        input = ['.'*length] + input + ['.'*length]
        input = ['.' + row + '.' for row in input]
        for i, line in enumerate(input[1:-1], 1):
            # Find every gear, and then get the numbers around it
            for g in re.finditer(r"\*", line):   # Loop over all the *s
                pos = g.start()
                surround = []
                for dir in [-1, +1]:             # Left and right dir(ection)
                    if number := re.match(r"\d+", line[pos+dir::dir]):
                        surround.append(number.group()[::dir])
                for row in [i-1, i+1]:           # Up and down
                    for n in re.finditer(r"\d+", input[row]):   # All numbers
                        if n.start() <= pos+1 and n.end() > pos-1:
                            surround.append(n.group())
                if len(surround) == 2:           # If there are two parts
                    result += int(surround[0]) * int(surround[1])
        return result

if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
