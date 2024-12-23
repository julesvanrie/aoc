import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint
from collections import defaultdict
from itertools import permutations


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()

    conns = {(k, v) for k, v in [row.split('-') for row in input]}
    conns_rev = {(v, k) for k, v in conns}

    conns |= conns_rev

    conns_lists = defaultdict(list)

    for conn in conns:
        conns_lists[conn[0]].append(conn[1])

    trios = set()

    for k, conns_list in conns_lists.items():
        for conn in conns_list:
            for k2 in conns_lists[conn]:
                if k in conns_lists[k2]:
                    trio = tuple(sorted([k, conn, k2]))
                    if trio[0].startswith('t') or trio[1].startswith('t') or trio[2].startswith('t'):
                        trios.add(trio)

    return len(trios)


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()

    conns = {(k, v) for k, v in [row.split('-') for row in input]}
    conns_rev = {(v, k) for k, v in conns}

    conns |= conns_rev

    computers = {k for k, v in conns}

    networks = [{comp} for comp in computers]

    for network in networks:
        for comp in computers:
            if all((comp, net_comp) in conns for net_comp in network):
                network.add(comp)

    result = max(len(net) for net in networks)

    return [','.join(sorted(list(net))) for net in networks if len(net) == result][0]


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
