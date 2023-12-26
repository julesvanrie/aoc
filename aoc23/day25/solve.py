import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint
from random import choice


def index_of_v(V, v):
    for i, vs in enumerate(V):
        if v in vs:
            return i

def remove_e(V, E, old_e):
    # Contract old_e right (old_v) into old_e left (new_v)
    l_v, r_v = old_e
    l_i = index_of_v(V, l_v)
    r_i = index_of_v(V, r_v)
    if l_i == r_i:
        return V, E
    # Remove old vertex
    # new_V = [v for v in V if v != old_v]
    new_V = V.copy()
    new_V[l_i] = new_V[l_i] + new_V[r_i]
    del new_V[r_i]
    # Remove old edge
    new_E = [e for e in E if e != old_e]
    # Redirect all edges from right vertex to left vertex
    # new_E = [e for e in new_E if old_v not in e]
    # new_E = [(e[0], new_v) if e[1] == old_v else e for e in new_E]
    # Remove duplicate edges:
    for e_l, e_r in new_E:
        if index_of_v(new_V, e_l) == index_of_v(new_V, e_r):
            new_E.remove((e_l, e_r))
    # print("V", new_V, "E", new_E)
    return new_V, new_E

def min_cut(V, E, start_e):
    e = start_e
    new_V = V.copy()
    new_E = E.copy()
    # print(start_e)
    min_v = len(V) + 1
    while len(new_V) < min_v and len(new_V) > 2:
        # pprint(new_V)
        # pprint(new_E)
        # print(min_v, new_V)
        min_v = len(new_V)
        # print("next e", e)
        print(len(new_V), end='\r')
        new_V, new_E = remove_e(new_V, new_E, e)
        e = choice(list(new_E))
        e_tried = []
        while e in e_tried:
            e = choice(list(new_E))
        e_tried.append(start_e)
        e = choice(new_E)
    # print(new_E)
    print()
    print(new_E)
    return [e for e in new_E if e[0] != e[1]], new_V


# def split(V, E, splits):
#     print(len(E))
#     print(splits)
#     pprint(E)
#     E = [e for e in E if e not in splits and (e[1], e[0]) not in splits]
#     print(len(E))
#     # for v in [v[o] for v in V]:
#     v = V[0][0]
#     V1 = []
#     for

@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    h = len(input)

    V = set()
    E = set()

    for line in input:
        src, dests = line.split(': ')
        V.add(src)
        for dest in dests.split(' '):
            V.add(dest)
            E.add((src, dest))

    V = [[v] for v in V]

    # breakpoint()
    min_E = E
    while len(min_E) != 3:
        start_e_tried = []
        while len(start_e_tried) != len(E):
            start_e = choice(list(E))
            while start_e in start_e_tried:
                start_e = choice(list(E))
            start_e_tried.append(start_e)
            min_E, Vs = min_cut(V, E, start_e)
            print("start_e", start_e, "tried", len(start_e_tried), "min_E", len(min_E))
            # print("min_E", min_E)
            if len(min_E) == 3:
                break

    # V1, V2 = split(V, E, min_E)
    return len(Vs[0]) * len(Vs[1])

    # # pprint(V)
    # # print()
    # # pprint(E)

    # result = 0

    # return result


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    h = len(input)
    w = len(input[0])

    result = 0

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
