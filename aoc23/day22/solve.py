import sys
from aocsolution.basesolution import BaseSolution

import re
from collections import deque
from copy import deepcopy
from pprint import pprint

def let_it_all_fall(input):
    blocks = [[[int(s) for s in c.split(',')] for c in r.split('~')] for r in input]
    ids = range(len(input))
    w = max(max(block[i][0] for i in [0,1]) for block in blocks) + 1
    d = max(max(block[i][1] for i in [0,1]) for block in blocks) + 1
    h = max(max(block[i][2] for i in [0,1]) for block in blocks) + 1

    # Sort by lowest z coordinate
    blocks = sorted(blocks, key=lambda b: b[0][2])

    # Build an empty stack
    stack = [[['.' for z in range(h)] for y in range(d)] for x in range(w)]

    # For each block, keep track of which other blocks are supporting it
    supports = {}
    for id, (s, e) in zip(ids, blocks):
        # Determine to which z the block can fall
        for sz in range(h-1,0,-1):
            if not all(stack[sx][sy][sz] == '.' for sx in range(s[0], e[0]+1) for sy in range(s[1], e[1]+1)):
                break
        support = set()
        for x in range(s[0], e[0]+1):
            for y in range(s[1], e[1]+1):
                # Check on which blocks it is now resting
                if (sup := stack[x][y][sz]) != '.':
                    support.add(sup)
                # Add the block to the stack
                for z in range(e[2] - s[2] +1):
                    stack[x][y][sz+1+z] = id
        # Save the results
        supports[id] = support

    # vizx(stack, d, w, h)
    # print()
    # vizy(stack, d, w, h)
    return supports


def safe_remove(supports):
    safe_remove = []
    for id in supports:
        can_remove = True
        for sup in supports.values():
            if id in sup:
                if len(sup) == 1:
                    can_remove = False
        if can_remove:
            safe_remove.append(id)

    return safe_remove


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    supports = let_it_all_fall(input)
    safe_removes = safe_remove(supports)
    return len(safe_removes)


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()
    supports = let_it_all_fall(input)
    safe_removes = safe_remove(supports)

    result = 0
    for id in supports:
        if id in safe_removes:
            continue
        falls = []
        nexts = deque([id])
        while nexts:
            nextfall = nexts.popleft()
            if nextfall in falls:
                continue
            falls.append(nextfall)
            for block, sups in supports.items():
                nbfell = 0
                for sup in sups:
                    if sup in falls + [id]:
                        nbfell += 1
                    if nbfell == len(sups):
                        nexts.append(block)
                        falls.append(block)
        result += len(set(falls)) - 1

    return result


def vizx(stack, w, d, h):
    mapping =  ['A','B','C','D','E','F','G']
    for z in range(h-1,0,-1):
        for x in range(w):
            b = '.'
            for y in range(d):
                if (nb := stack[x][y][z]) != '.':
                    b = nb
            print(b, end='')
        print()


def vizy(stack, w, d, h):
    for z in range(h-1,0,-1):
        for y in range(d):
            b = '.'
            for x in range(w):
                if (nb := stack[x][y][z]) != '.':
                    b = nb
            print(b, end='')
        print()


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
