import sys
from aocsolution.basesolution import BaseSolution

import re

@BaseSolution.time_this
def solve_one(self):
    result = 0
    input = self.get_data()[0].strip().split(',')

    for step in input:
        temp = 0
        for c in step:
            temp += ord(c)
            temp *= 17
            temp %= 256
        result += temp

    return result


@BaseSolution.time_this
def solve_two(self):
    result = 0
    input = self.get_data()[0].strip().split(',')

    boxes = [{} for i in range(256)]

    for step in input:
        label = step.split('=')[0].split('-')[0]
        nb = 0
        for c in label:
            nb += ord(c)
            nb *= 17
            nb %= 256
        box = boxes[nb]
        if step[-1] == '-':
            try:
                del box[label]
            except:
                pass
        else:
            box[label] =  int(step.split('=')[1])

    for idx, box in enumerate(boxes, 1):
        for slot, focal in enumerate(box.values(), 1):
            result += idx * slot * focal

    return result


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
