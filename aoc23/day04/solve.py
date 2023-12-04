import sys
from aocsolution.basesolution import BaseSolution

import re

@BaseSolution.time_this
def solve_one(self):
    result = 0
    input = self.get_data()
    for line in input:
        valids = re.findall(r"\d+", line.split(" | ")[0].split(": ")[1])
        mine = re.findall(r"\d+", line.split(" | ")[1])
        matches = [el for el in mine if el in valids]
        result += int(2**(len(matches)-1))    # int brings 2**-1 = 0.5 to 0
    return result


@BaseSolution.time_this
def solve_two(self):
    result_one, result_two = 0, 0
    input = self.get_data()
    templates = []     # Stores number of new cards that a card generates
    for line in input:
        valids = re.findall(r"\d+", line.split(" | ")[0].split(": ")[1])
        mine = re.findall(r"\d+", line.split(" | ")[1])
        matches = [el for el in mine if el in valids]
        result_one += int(2**(len(matches)-1))    # int brings 2**-1 = 0.5 to 0
        templates.append(len(matches))

    cards_count = [1 for i in range(len(templates))] # Initialize count cards to 1

    def go_deep(card_numbers):
        for n in card_numbers:
            new_cards = [n+1+i for i in range(templates[n])
                               if n+1+i < len(templates)]
            for c in new_cards:
                cards_count[c] += 1
            go_deep(new_cards)

    go_deep(range(len(templates)))  # Start with the first cards
    result_two = sum(cards_count)
    return result_one, result_two


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
