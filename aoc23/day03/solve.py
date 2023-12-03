import sys
from aocsolution.basesolution import BaseSolution

import re

class Solution(BaseSolution):

    @BaseSolution.time_this
    def solve_one(self):
        result = 0
        input = self.get_data()
        length = len(input[0])
        for i, line in enumerate(input):
            numbers = re.finditer(r"\d+", line)
            for n in numbers:
                # Put everything in the surrounding area in a string
                # and we'll check that it only has dots.
                surround = ""
                left = max(n.start()-1, 0)
                right = min(n.end()+1, length-1)
                if i > 0:                           # Look up
                    surround += input[i-1][left:right]
                if i < length-1:                    # Look down
                    surround += input[i+1][left:right]
                if n.start() > 0:                   # Look left
                    surround += line[n.start()-1]
                if n.end() < length - 1:            # Look right
                    surround += line[n.end()]
                # And now check
                if surround.replace('.', ''):
                    result += int(n.group())
        return result

    @BaseSolution.time_this
    def solve_two(self):
        result = 0
        input = self.get_data()
        length = len(input[0])
        for i, line in enumerate(input):
            # Find every gear, and then get the numbers around it
            gears = re.finditer(r"\*", line)
            for g in gears:
                pos = g.start()
                surround = []
                if pos < length:         # Look right
                    if number := re.match(r"\d+", line[pos+1:]):
                        surround.append(number.group())
                if pos > 0:              # Look left (and match on reverse)
                    if number := re.match(r"\d+", line[pos-1::-1]):
                        surround.append(number.group()[::-1])
                if i > 0:                # Look up
                    # Find all numbers and check their position
                    numbers = re.finditer(r"\d+", input[i-1])
                    for n in numbers:
                        if n.start() <= pos+1 and n.end() > pos-1:
                            surround.append(n.group())
                if i < len(input) - 1:   # Look down
                    numbers = re.finditer(r"\d+", input[i+1])
                    for n in numbers:
                        if n.start() <= pos+1 and n.end() > pos-1:
                            surround.append(n.group())
                # Check there's two and do the math
                if len(surround) == 2:
                    result += int(surround[0]) * int(surround[1])
        return result

if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
