import sys
from aocsolution.basesolution import BaseSolution

import re

@BaseSolution.time_this
def solve_one(self):
    result = 0
    input = self.get_data(split=False)
    inputs = input.split('\n\n')
    seeds = [int(i) for i in inputs[0].split(': ')[1].split(' ')]
    maps = [i.split('\n')[1:] for i in inputs[1:]]

    def mapping(source, map):
        for m in map:
            d, s, r = m.split(' ')
            if source >= int(s) and source < (int(s) + int(r)):
                return source - int(s) + int(d)
        return source

    locations = {}
    for seed in seeds:
        # print("\nseed", seed, end=' ')
        dest = seed
        for map in maps:
            dest = mapping(dest, map)
            # print(dest, end=' ')
        locations[seed] = dest

    return min(locations.values())


@BaseSolution.time_this
def solve_two(self):
    result = 0
    input = self.get_data(split=False)
    inputs = input.split('\n\n')
    seeds = [int(i) for i in inputs[0].split(': ')[1].split(' ')]
    maps = [i.split('\n')[1:] for i in inputs[1:]]

    ranges = []
    for i in range(0, len(seeds), 2):
        ranges.append((seeds[i], seeds[i]+seeds[i+1]-1))

    def mapping(ranges, map):
        new = []
        for range in ranges:
            start = range[0]
            end = range[1]
            initial_new_length = len(new)
            for m in map:
                d, s, r = m.split(' ')
                if start >= (int(s) + int(r)):
                    continue
                if start >= int(s):
                    new_start = start - int(s) + int(d)
                    if end < (int(s) + int(r)):
                        new_end = end - int(s) + int(d)
                        new.append([new_start, new_end])
                    else:
                        new_end = int(d) + int(r) - 1
                        new.append([new_start, new_end])
                        ranges.append([int(s) + int(r), end])
                    continue
                if end < int(s):
                    continue
                if end < (int(s) + int(r)):
                    new_start = int(d)
                    new_end = end - int(s) + int(d)
                    new.append([new_start, new_end])
                    ranges.append([start, int(s)-1])
                else:
                    new_start = int(d)
                    new_end = int(d) + int(r) - 1
                    new.append([new_start, new_end])
                continue
            if initial_new_length == len(new):
                new.append(range)
        return new

    dest = ranges
    print(dest)
    for map in maps:
        dest = mapping(dest, map)
        # print(dest)
    result = min(d[0] for d in dest)

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
