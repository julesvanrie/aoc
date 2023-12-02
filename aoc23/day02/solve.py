import sys
from aocsolution.basesolution import BaseSolution

class Solution(BaseSolution):

    @BaseSolution.time_this
    def solve_one(self):
        result = 0
        limits = {'red': 12, 'green': 13, 'blue': 14}
        input = self.get_data()
        games = [inp.split(": ")[1] for inp in input]
        outcomes = []
        for game in games:
            outcome = {
                'red': [],
                'green': [],
                'blue': []
            }
            for set in game.split("; "):
                for color in set.split(", "):
                    outcome[color.split(" ")[1]].append(int(color.split(" ")[0]))
            outcomes.append(outcome)

        for id, outcome in enumerate(outcomes, 1):
            valid = True
            for key, value in limits.items():
                if max(outcome[key]) > value:
                    valid = False
            if valid:
                result += id

        return result

    @BaseSolution.time_this
    def solve_two(self):
        result = 0
        limits = {'red': 12, 'green': 13, 'blue': 14}
        input = self.get_data()
        games = [inp.split(": ")[1] for inp in input]
        outcomes = []
        for game in games:
            outcome = {
                'red': [],
                'green': [],
                'blue': []
            }
            for set in game.split("; "):
                for color in set.split(", "):
                    outcome[color.split(" ")[1]].append(int(color.split(" ")[0]))
            outcomes.append(outcome)
            print(outcome)

        for id, outcome in enumerate(outcomes, 1):
            power = 1
            for key, value in limits.items():
                power *= max(outcome[key])
            result += power

        return result


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
