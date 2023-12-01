import sys
from aocsolution.basesolution import BaseSolution

import re

class Solution(BaseSolution):

    @BaseSolution.time_this
    def solve_one(self):
        result = 0
        input = self.get_data()
        for line in input:
            number = ''

            for letter in line:
                if letter.isdigit():
                    number += letter
                    break

            for letter in line[::-1]:
                if letter.isdigit():
                    number += letter
                    break

            result += int(number)
        return result

    @BaseSolution.time_this
    def solve_two(self):
        result = 0
        input = self.get_data()

        pattern = "one|two|three|four|five|six|seven|eight|nine"

        numbers = {txt: n for txt, n in zip(pattern.split('|'), range(1,10))}

        pattern_left = r"\d|" + pattern
        pattern_right = r"\d|" + pattern[::-1]

        for line in input:
            left = re.search(pattern_left, line).group()
            right = re.search(pattern_right, line[::-1]).group()
            result += 10 * int(numbers.get(left, left)) \
                     + 1 * int(numbers.get(right[::-1], right))

        return result

if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
