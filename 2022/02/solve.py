import sys
from aochelper import get_data


def solve(lines):
    if not lines:
        lines = get_data(sys.argv)

    ##########
    # Part 1 #
    ##########

    shape = {'X': 1, 'Y': 2, 'Z': 3}
    winning = {
        'A X': 3,
        'A Y': 6,
        'A Z': 0,
        'B X': 0,
        'B Y': 3,
        'B Z': 6,
        'C X': 6,
        'C Y': 0,
        'C Z': 3,
        }

    shape_score = sum([shape[line[2]] for line in lines])
    winning_score = sum([winning[line] for line in lines])

    result1 = shape_score + winning_score

    print("The result is for part 1 is:", result1)



    ##########
    # Part 2 #
    ##########


    shape = {
        'A X': 3, # Rock wins : scissors
        'A Y': 1, # Rock
        'A Z': 2,
        'B X': 1,
        'B Y': 2,
        'B Z': 3,
        'C X': 2,
        'C Y': 3,
        'C Z': 1,
        }
    winning = {
        'X': 0,
        'Y': 3,
        'Z': 6,
        }

    shape_score = sum([shape[line] for line in lines])
    winning_score = sum([winning[line[2]] for line in lines])

    result2 = shape_score + winning_score

    print("The result is for part 2 is:", result2)

    return result1, result2
