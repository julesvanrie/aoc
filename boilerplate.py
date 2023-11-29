import sys
from aocsolution.basesolution import BaseSolution

class Solution(BaseSolution):

    @BaseSolution.time_this
    def solve_one(self):
        result = None
        return result

    @BaseSolution.time_this
    def solve_two(self):
        result = None
        return result

if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
