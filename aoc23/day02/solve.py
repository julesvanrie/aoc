import sys
from aocsolution.basesolution import BaseSolution

class Solution(BaseSolution):

    @BaseSolution.time_this
    def solve_one(self):
        result = 0
        limits = {'red': 12, 'green': 13, 'blue': 14}
        input = self.get_data()
        games = [inp.split(": ")[1] for inp in input]

        # Make a list with the outcomes for each game
        # Each outcome will be a dict with numbers for each color in this game
        outcomes = []
        for game in games:
            outcome = {
                'red': [],
                'green': [],
                'blue': []
            }
            # Add the numbers of each set to the appropriate color
            for set in game.split("; "):
                for color in set.split(", "):
                    number, col = color.split(" ")
                    outcome[col].append(int(number))
            outcomes.append(outcome)

        # Loop over the outcomes
        # If it's a valid game, add the id to the result
        for id, outcome in enumerate(outcomes, 1):
            valid = True
            for color, limit in limits.items():
                if max(outcome[color]) > limit:
                    valid = False
                    continue
            if valid:
                result += id

        return result

    @BaseSolution.time_this
    def solve_two(self):
        result = [0, 0]
        limits = {'red': 12, 'green': 13, 'blue': 14}
        input = self.get_data()
        games = [inp.split(": ")[1] for inp in input]

        # Make a list with the outcomes for each game
        # Each outcome will be a dict with numbers for each color in this game
        outcomes = []
        for game in games:
            outcome = {
                'red': [],
                'green': [],
                'blue': []
            }
            # Add the numbers of each set to the appropriate color
            for set in game.split("; "):
                for color in set.split(", "):
                    number, col = color.split(" ")
                    outcome[col].append(int(number))
            outcomes.append(outcome)

        # Loop over the outcomes
        # If it's a valid game, add the id to the result
        # At the same time calculate the power based on the max number
        for id, outcome in enumerate(outcomes, 1):
            power = 1
            valid = True
            for color, limit in limits.items():
                if max(outcome[color]) > limit:
                    valid = False
                power *= max(outcome[color])
            result[1] += power
            if valid:
                result[0] += id

        return result


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
