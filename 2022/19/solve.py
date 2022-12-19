import os, sys, timeit
from aochelper import get_data
import re
from collections import namedtuple
from pprint import pprint

MiningTuple = namedtuple('MiningTuple', ['ore','clay','obsidian','geode'])

MiningTuple.__add__ = lambda left, right: \
    MiningTuple(*[left[i] + right[i] for i in range(len(left))])

MiningTuple.__sub__ = lambda left, right: \
    MiningTuple(*[left[i] - right[i] for i in range(len(left))])

MiningTuple.__gt__ = lambda left, right: \
    all(left[i] >= right[i] for i in range(len(left))) and \
    any(left[i] > right[i] for i in range(len(left)))

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')

    # Parsing blueprints
    blueprints = []
    for line in [line.strip(' .').split('. ') for line in lines]:
        blueprint = {}
        for robot in line:
            type = re.findall(r"(?<=Each )\w*(?= robot)", robot)[0]
            costs = re.findall(r"(\d\d*) (\w*)", robot)
            costs = {c[1]: int(c[0]) for c in costs}
            blueprint[type] = MiningTuple(**{f: costs[f] if f in costs else 0 for f in MiningTuple._fields})
        blueprints.append(MiningTuple(**blueprint))


    def birth(type, robots, resources, blueprint=0):
        cost = blueprints[blueprint][type]
        if all(resources[i] >= cost[i] for i in range(4)):
            resources = resources - cost
            robots = robots + MiningTuple(*[1 if i == type else 0 for i in range(len(robots))])
            return robots, resources
        return False


    def run(bpnmbr, times):
        robots = MiningTuple(1,0,0,0)

        resources = (0,0,0,0)


        bp = blueprints[bpnmbr]

        states = {(robots, resources): 0}

        # We'll keep track of earlier visited states
        visited = set()
        max_costs = MiningTuple(*[max([bp[j][i] for j in range(4)]) for i in range(4)])

        for m in range(1,times):
            print('====== blueprint', bpnmbr, '======', m, '============', end='\r')
            possible = list(range(len(robots)))
            new_states = {}
            # if m >= 1:
            #     breakpoint()
            current_max = max(states.values())
            # if not len(states):
            #     breakpoint()
            for state in states:
                if state in visited:
                    continue
                robots, resources = state
                resources = MiningTuple(resources[0], resources[1], resources[2], states[state])

                # Collect resources
                # for i, res in enumerate(robots):
                #     resources[i] += robots[i]

                created_one = False

                # Try building different robots
                # At a certain time, stop building the basic bots
                # (9 minutes before the end worked for me)
                if m < times - 9:
                    cands = [3,2,1,0,-1]
                else:
                    cands = [3,2,-1]

                for cand in cands:
                    new_robots, new_resources = MiningTuple(*list(robots)), MiningTuple(*list(resources))
                    if cand >= 0 and (cand == 3 or robots[cand] < max_costs[cand]):
                        # Update robots and resources
                        if result := birth(cand, robots, resources, blueprint=bpnmbr):
                            new_robots, new_resources = result


                    new_resources = new_resources + robots
                    # MiningTuple(*[res + robots[i] for i, res in enumerate(new_resources)])
                    # if getattr(resources,'geode') < current_max:
                    #     continue

                    # Skip if we're far behind best so far
                    if new_resources.geode < current_max - 3:
                        continue

                    # Add new state
                    new_state = (new_robots, (new_resources[0], new_resources[1], new_resources[2], new_resources[3]))
                    choice = 'new'
                    if new_state in new_states:
                        if new_states[new_state] > getattr(new_resources,'geode'):
                            choice = 'current'
                    if prev_state := states.get(state, False):
                        if prev_state >= getattr(new_resources,'geode'):
                            choice = 'old'
                    if choice == 'new':
                        new_states[new_state] = getattr(new_resources,'geode')

                    if result:
                        created_one = True
                    # Some heuristics:
                    # - If a bot was created, don't go down the path of not creating one
                    # - If a geode or obsidian bot can be made, do so
                    if created_one and cand in [3,0]:
                        break

                visited.add(state)

            states = new_states
        print(max(states.values()))
        return max(states.values())


    ##########
    # Part 1 #
    ##########

    results = []
    for i in range(len(blueprints)):
        # breakpoint()
        results.append((i+1)*run(i, 25))

    result1 = sum(results)

    print("The result is for part 1 is:", result1)


    ##########
    # Part 2 #
    ##########

    results = []
    result2 = 1
    for i in range(min(3, len(blueprints))):
        # breakpoint()
        tmp = run(i, 33)
        results.append(tmp)
        result2 *= tmp

    print("The result is for part 2 is:", result2)

    return result1, result2


def time():
    with open(os.devnull, 'w') as out:
        sys.stdout = out
        number = 20
        timing = timeit.timeit(solve, number=number) / number
        sys.stdout = sys.__stdout__
    print(f"This took {timing:.6f} seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1][:4] == "time":
        del sys.argv[1]
        time()
    else:
        solve()
