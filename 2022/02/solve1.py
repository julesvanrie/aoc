import sys
from aochelper import get_data

lines = get_data(sys.argv)

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
