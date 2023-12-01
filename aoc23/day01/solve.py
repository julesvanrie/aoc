import sys
from aocsolution.basesolution import BaseSolution

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
        for line in input:
            letters = ['one', 'two', 'three', 'four', 'five',
                       'six', 'seven', 'eight', 'nine']
            number = ''

            for i in range(len(line)):
                if line[i].isdigit():
                    number += line[i]
                    break
                for n, ntxt in enumerate(letters, 1):
                    if line[i:].startswith(ntxt):
                        number += str(n)
                        break
                if number:
                    break

            for i in range(len(line)-1, -1, -1):
                if line[i].isdigit():
                    number += line[i]
                    break
                for n, ntxt in enumerate(letters, 1):
                    if line[:i+1].endswith(ntxt):
                        number += str(n)
                        break
                if len(number) > 1:
                    break

            result += int(number)
        return result

if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
