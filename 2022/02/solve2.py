import sys
from aochelper import get_data

lines = get_data(sys.argv)

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
