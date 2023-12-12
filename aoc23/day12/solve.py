import sys
from aocsolution.basesolution import BaseSolution

import re


# ???.### 1,1,3                    ....[#?]{1}...[#?]{1}...[#?]{3}...
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1


@BaseSolution.time_this
def solve_one(self):
    result = 0
    input = self.get_data()
    springs = [inp.split() for inp in input]

    for line, (text, counts) in enumerate(springs[:]):
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


        res = re.finditer(r"(?=([\.\?]*[#\?][\.\?]+[#\?][\.\?]+[#\?]{3}[\.\?]*))", text)
        res = re.findall(r"(?=[\.\?]*[#\?][\.\?]+[#\?][\.\?]+[#\?]{3}[\.\?]*)", text)
        # print(len(res))
        # print([r.group(1) for r in res])
        # nb = 0
        # for c in counts.split(','):
        #     pattern_sub = r"^[\.\?]*[#\?]{" + c + r"}[\.\?]+"
        #     pattern_find = r"(?=" + pattern_sub + r")"
        #     nb += len(re.findall(pattern_find, text))
        #     text = re.sub(pattern_sub, '', text, 1)
        #     print(nb, text)


    return result


@BaseSolution.time_this
def solve_two_bweurk(self):
    result = 0
    input = self.get_data()
    springs = [inp.split() for inp in input]

    for line, (text, counts) in enumerate(springs[:1]):
        print(line, len(input))
        counts = ','.join([counts]*5)
        pattern = r"^[\.\?]*"
        for c in counts.split(','):
            pattern += r"[\?\#]{" + c + r"}[\.\?]+"
        pattern += r"$"
        # print(pattern)
        text = '?'.join([text]*5) + '.'
        print('\n', text, counts)
        # possibilities = [text + '.']

        nb_pos = 0

        t = [c for c in text]

        questions = [0]*len(t)
        for i in range(len(t)):
            if t[i] == '?':
                questions[i] = 2

        print(''.join(str(q) for q in questions))
        i = 0
        history = [t for j in range(len(t))]
        while i < len(t):
            # print(history[i])
            print(i, ''.join(history[i]))
            # if not re.match(pattern, ''.join(t)):
                # print("here")
                # continue
            # print("not here")
            changed = False
            if questions[i] == 2 and not changed:
                # print("here")
                for j in range(i,len(t)):
                    history[j][i] = '#'
                questions[i] = 1
                changed = True
                # if re.match(pattern, ''.join(history[i])):
                    # i += 1
                    # continue
            if questions[i] == 1 and not changed:
                for j in range(i,len(t)):
                    history[j][i] = '.'
                questions[i] = 2
                changed = True
                # if re.match(pattern, ''.join(history[i])):
                    # i += 1
                    # continue
            if True or questions[i] == 0:
                # i += 1
                # continue
                # print(''.join(history[i]))
                if not re.search(r"\?", ''.join(history[i])):
                    print("somehwere")
                    if re.match(pattern, ''.join(history[i])):
                        print("somehwereelse")
                        nb_pos += 1
                    questions[i] = 2
                    for j in range(i,len(t)):
                        history[j][i] = '?'
                    i -= 1
                    # continue
                else:
                    i += 1
                # continue
                # if not re.match(pattern, ''.join(history[i])):
                #     i -= 1
            print(nb_pos)

    return

    if True:
        nb = 0
        idx = 0
        while idx < len(possibilities):
        # for idx, t in enumerate(possibilities):
            t = possibilities[idx]
            # print(t)
            for i in range(len(t)):
                if t[i] == '?':
                    for new in ['#', '.']:
                        t_new = t[:i] + new + t[i+1:]
                        if re.match(pattern, t_new):
                            # print('Appending', t_new)
                            possibilities.append(t_new)
                    # print(idx, possibilities)
                    del possibilities[idx]
                    idx -= 1
                    # print(possibilities)
                    break
            idx += 1
            # print(len(possibilities))
        result += (len(possibilities))



@BaseSolution.time_this
def solve_two_bweurk2(self):
    result = 0
    input = self.get_data()
    springs = [inp.split() for inp in input]

    for line, (text, counts) in enumerate(springs[:]):
        print(line, len(input))
        counts = ','.join([counts]*5)
        pattern = r"^[\.\?]*"
        for c in counts.split(','):
            pattern += r"[\?\#]{" + c + r"}[\.\?]+"
        pattern += r"$"
        pattern = re.compile(pattern)
        # print(pattern)
        text = '?'.join([text]*5) + '.'
        print('\n', text, counts)
        # possibilities = [text + '.']
        nb_broken = sum(int(c) for c in counts.split(','))
        nb_groups = len(counts.split(','))
        result += check(text, pattern, nb_broken, nb_groups)

    return result

def check_bweurk(text, pattern, nb_broken, nb_groups):
    qs = text.count('?')
    if not qs:
       if re.match(pattern, text):
           return 1
       return 0
    if len(text) < nb_broken + nb_groups - 1:
        return 0
    if qs + text.count('#') < nb_broken:
        return 0
    if not re.match(pattern, text):
        return 0
    # if len(re.findall(r"(?=[\#\?]+)", text)) < nb_groups:
    #     return 0
    return (
        check(text.replace('?', '#', 1), pattern, nb_broken, nb_groups)
        + check(text.replace('?', '.', 1), pattern, nb_broken, nb_groups)
    )

import functools
@functools.cache
def check(text, groups):
    if not groups and not text:
        return 1
    if not groups and not '#' in text:
        return 1
    if not groups and '#' in text:
        return 0

    if groups and not text:
        return 0
    if sum(groups) > text.count('#') + text.count('?'):
        return 0

    if text[0] == '.':
        return check(text[1:], groups)

    if text[0] == '?':
        if len(text) > 1:
            # import pdb; pdb.set_trace()
            # if not check('#'+text[1:], groups):
            #     print(text, groups)
            return check('.'+text[1:], groups) + check('#'+text[1:], groups)
        else:
            return 1
    if (
        groups
        and len(text) >= groups[0]
        and text[:groups[0]].replace('?', '#') == '#'*groups[0]
    ):
        if len(text) == groups[0]:
            return 1
        if text[groups[0]] == '#':
            return 0
        return check(text[groups[0]+1:], groups[1:])
    return 0


@BaseSolution.time_this
def solve_two(self):
    result = 0
    input = self.get_data()
    springs = [inp.split() for inp in input]

    for line, (text, counts) in enumerate(springs[:]):
        print(line, len(input), text, counts)
        counts = ','.join([counts]*5)
        text = '?'.join([text]*5) + '.'
        result += check(text, tuple(int(c) for c in counts.split(',')))

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
