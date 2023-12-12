import sys
from aocsolution.basesolution import BaseSolution

import re
import functools


@BaseSolution.time_this
def solve_one(self):
    """This was my initial attempt.
    It worked. But then it failed big time for part 2.
    But it was some interesting regex though :-)
    """
    result = 0
    input = self.get_data()
    springs = [inp.split() for inp in input]

    for text, counts in springs[:]:
        pattern = r"^[\.\?]*"
        for c in counts.split(','):
            pattern += r"[\?\#]{" + c + r"}[\.\?]+"
        pattern += r"$"
        possibilities = [text + '.']

        idx = 0
        while idx < len(possibilities):
            t = possibilities[idx]
            for i in range(len(t)):
                if t[i] == '?':
                    for new in ['#', '.']:
                        t_new = t[:i] + new + t[i+1:]
                        if re.match(pattern, t_new):
                            possibilities.append(t_new)
                    del possibilities[idx]
                    idx -= 1
                    break
            idx += 1

        result += (len(possibilities))

    return result


@functools.cache
def check(text, groups):
    if not groups:
        if not text or not '#' in text:
            return 1
        if '#' in text:
            return 0
    if groups and not text:
        return 0
    # The next one is optional but speeds up a lot
    if len(text) < sum(groups) + len(groups) - 1:
        return 0

    if text[0] == '.':
        return check(text[1:], groups)

    if text[0] == '?':
        return check('.'+text[1:], groups) + check('#'+text[1:], groups)

    #  text[0] == '#'
    if text[:groups[0]].replace('?', '#') == '#'*groups[0]:
        if len(text) == groups[0]:
            # Matches and nothing else left
            return 1
        if text[groups[0]] == '#':
            # A broken one too much
            return 0
        # In all other cases, go check the next group
        return check(text[groups[0]+1:], groups[1:])
    return 0


@BaseSolution.time_this
def solve_two(self, repeats):
    result = 0
    input = self.get_data()
    springs = [inp.split() for inp in input]

    for text, counts in springs[:]:
        counts = tuple(int(c) for c in counts.split(',')) * repeats
        text = '?'.join([text]*repeats) + '.'
        result += check(text, counts)

    return result


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one(), "(the stupid way)")
    print("The result for part 1 is:", solution.solve_two(1))
    print("The result for part 2 is:", solution.solve_two(5))
