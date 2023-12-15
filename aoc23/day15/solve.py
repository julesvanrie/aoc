import sys
from aocsolution.basesolution import BaseSolution

import re

@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()[0].strip().split(',')

    result = 0
    for step in input:
        temp = 0
        for c in step:
            temp += ord(c)
            temp *= 17
            temp %= 256
        result += temp

    return result


def hash(step):
    temp = 0
    for c in step:
        temp += ord(c)
        temp *= 17
        temp %= 256
    return temp


@BaseSolution.time_this
def solve_one_comp(self):
    input = self.get_data()[0].strip().split(',')
    return sum(hash(step) for step in input)



@BaseSolution.time_this
def solve_one_func(self):
    from functools import reduce
    from operator import add

    return reduce(
        add,
        map(
            lambda step:
            reduce(
                lambda init, c: (init + ord(c)) * 17 % 256,
                step,
                0
            ),
            self.get_data()[0].strip().split(',')
        )
    )


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()[0].strip().split(',')

    boxes = [{} for i in range(256)]

    for step in input:
        label = step.split('=')[0].split('-')[0]
        box = boxes[hash(label)]
        if step[-1] == '-':
            if label in box:
                del box[label]
        else:
            box[label] = int(step.split('=')[1])

    return sum(
        sum(
            idx * slot * focal
            for slot, focal in enumerate(box.values(), 1)
        )
        for idx, box in enumerate(boxes, 1)
    )


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two
    solve_one_comp = solve_one_comp
    solve_one_func = solve_one_func


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 classic is:", solution.solve_one())
    print("The result for part 1 list comprehension is:", solution.solve_one_comp())
    print("The result for part 1 functional is:", solution.solve_one_func())
    print("The result for part 2 is:", solution.solve_two())
