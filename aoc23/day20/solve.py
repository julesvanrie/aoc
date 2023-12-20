import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint
from types import SimpleNamespace

# broadcaster -> a, b, c
# %a -> b
# %b -> c
# %c -> inv
# &inv -> a

@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    modules = {}
    starts = []
    for r in input:
        id, outs = r.split(' -> ')
        if id == 'broadcaster':
            starts = outs.split(', ')
        else:
            modules[id[1:]] = SimpleNamespace(
                id=id[1:],
                type=0 if id[0] == '%' else 1,
                on=False if id[0] == '%' else True,
                pulsed=False,
                outs=outs.split(', '),
                states={}
            )
        modules['output'] =  SimpleNamespace(
            id='output',
            type=2,
            on=True,
            pulsed=False,
            outs=[],
            states={}
        )

    for id, m in modules.items():
        # if m.type == 0:
        #     m.states = {m.id: False}
        for out in m.outs:
            if out not in modules:
                continue
            if modules[out].type == 0:
                modules[out].states[id] = False
            if modules[out].type == 1:
                modules[out].states[id] = False

    for id, m in modules.items():
        print(m)
    print()

    lows = 0
    highs = 0

    for i in range(1):
        print(i)
        lows += 1
        for s in starts:
            lows += 1
            m = modules[s]
            m.on = True
            for out in m.outs:
                if out in modules:
                    modules[out].states[m.id] = False
                    # if modules[out].type == 1:
                    modules[out].pulsed = True
                    print("Pulsed", out, True)
                highs += 1

        # for id, m in modules.items():
        #     print(m)
        # print()
        while any(m.pulsed for m in modules.values()):
        # for i in range(7):
            print()
            for id, m in modules.items():
                print(m)
            for m in modules.values():
                m.old_states = m.states.copy()
                m.old_pulsed = m.pulsed
                m.pulsed = False
            for m in modules.values():
                # print(m.id, m.old_states.values())
                if m.old_pulsed:
                    if m.type == 0:
                        if any(m.old_states.values()):
                            print(m.id, "switches to", not m.on)
                            for out in m.outs:
                                if out in modules:
                                    modules[out].states[m.id] = m.on
                                    modules[out].pulsed = True
                                    print("Pulsed", out, True)
                                if m.on:
                                    lows += 1
                                else:
                                    highs += 1
                            m.on = not m.on
                    if m.type == 1:
                        send_low = not any(m.old_states.values())
                        for out in m.outs:
                            if out in modules:
                                modules[out].states[m.id] = send_low
                                modules[out].pulsed = True
                                print("Pulsed", out, send_low)
                            if send_low:
                                lows += 1
                            else:
                                highs += 1

            # print()

    result = lows * highs

    return result, lows, highs


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
