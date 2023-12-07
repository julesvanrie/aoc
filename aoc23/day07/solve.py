import sys
from aocsolution.basesolution import BaseSolution

import re

@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    decks = []
    for inp in input:
        deck, bid = inp.split(" ")
        deck = deck.replace("T", "a") \
                   .replace("J", "b") \
                   .replace("Q", "c") \
                   .replace("K", "d") \
                   .replace("A", "e")
        counts = {c: deck.count(c) for c in "0123456789abcde"}
        if 5 in counts.values():
            hand = "z"               # 5 of a kind
        elif 4 in counts.values():
            hand = "y"               # 4 of a kind
        elif 3 in counts.values() and 2 in counts.values():
            hand = "x"               # Full house
        elif 3 in counts.values():
            hand = "t"               # 3 of a kind
        elif list(counts.values()).count(2) == 2:
            hand = "s"               # 2 pairs
        elif 2 in counts.values():
            hand = "r"               # 1 pair
        else:
            hand = "q"               # High card
        decks.append(hand + deck + " " + bid)

    return sum([rank * int(deck.split(' ')[1])
                for rank, deck in enumerate(sorted(decks), 1)])


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    decks = []
    for inp in input:
        deck, bid = inp.split(" ")
        deck = deck.replace("T", "a") \
                   .replace("J", "0") \
                   .replace("Q", "c") \
                   .replace("K", "d") \
                   .replace("A", "e")
        counts = {c: deck.count(c) for c in "023456789abcde"}
        if (         # 5 of a kind
            5 in counts.values()
            or 4 in counts.values() and counts["0"] == 1
            or 3 in counts.values() and counts["0"] == 2
            or 2 in counts.values() and counts["0"] == 3
            or 1 in counts.values() and counts["0"] == 4
        ):
            hand = "z"
        elif (       # 4 of a kind
            4 in counts.values()
            or 3 in counts.values() and counts["0"] == 1
            or list(counts.values()).count(2) == 2 and counts["0"] == 2
            or counts["0"] == 3
        ):
            hand = "y"
        elif (       # Full house
            3 in counts.values() and 2 in counts.values()
            or list(counts.values()).count(2) == 2 and counts["0"] == 1
        ):
            hand = "x"
        elif (       # 3 of a kind
            3 in counts.values()
            or 2 in counts.values() and counts["0"] == 1
            or 1 in counts.values() and counts["0"] == 2
        ):
            hand = "t"
        elif (       # 2 pairs
            list(counts.values()).count(2) == 2
        ):
            hand = "s"
        elif (       # 1 pair
            2 in counts.values()
            or counts["0"] == 1
        ):
            hand = "r"
        else:       # High card
            hand = "q"
        decks.append(hand + deck + " " + bid)

    return sum([rank * int(deck.split(' ')[1])
                for rank, deck in enumerate(sorted(decks), 1)])


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
