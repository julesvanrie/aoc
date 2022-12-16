import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')

    flows = {}; connections = {}
    for line in lines:
        valve = line.split(' has ')[0].split(' ')[1]
        connections[valve] = line.replace('valves','valve').split(' valve ')[1].split(', ')
        flows[valve] = int(line.split(';')[0].split('=')[1])

    working = [k for k, v in flows.items() if v]
    # print(flows['DD'], connections['DD'])
    print(working)
    ##########
    # Part 1 #
    ##########


    paths = {}
    opened = working.copy()



    def shortest(head, tail, visited):
        # breakpoint()
        short = 2000
        if tail in connections[head]:
            return 1
        for step in connections[head]:
            if step in visited:
                continue
            new = shortest(step, tail, visited + [step]) + 1
            if new <= short:
                short = new
            if new == 2:
                return 2

        return short


    # print(shortest('AA','BB'))
    # print(shortest('AA','HH', []))

    distances = {}
    working_connections = {}
    for head in working + ['AA']:
        temp = []
        for tail in working:
            if head != tail:
                distances[(head, tail)] = shortest(head, tail, [])
                temp.append(tail)
        working_connections[head] = temp

    print(working_connections)

    # print(distances)

    states = {('AA', None, 1): 0}


    def add_states(state):
        new_states = {}
        # breakpoint()
        if not state[1]:
            opened = []
        else:
            opened = list(state[1])
            # print(opened)
        if set(opened) == set(working):
            # breakpoint()
            new_pressure = states[state] \
                         + sum(flows[op] for op in opened) * (31 - state[2])
            return {(state[0], tuple(opened), 31): new_pressure}
        if state[0] != 'AA' and state[0] not in opened:
            new_pressure = states[state] + sum(flows[op] for op in opened) #+ flows[state[0]]
            if not state[1]:
                new_opened = (state[0],)
            else:
                new_opened = tuple(opened + [state[0]])
            new_states[(state[0], new_opened, state[2] + 1)] = new_pressure
        if state[0] in opened:
            new_pressure = states[state] + sum(flows[op] for op in opened)
            new_states[(state[0], tuple(opened), state[2] + 1)] = new_pressure
        # print(state)
        for conn in working_connections[state[0]]:
            new_opened = tuple(opened)
            duration = min(distances[(state[0], conn)], 31-state[2])
            # breakpoint()
            new_minute = state[2] + duration
            new_pressure = states[state] + sum(flows[op] for op in opened) * (duration)
            new_states[(conn, new_opened, new_minute)] = new_pressure
        return new_states

    for m in range(1, 31, +1):
        print(m, len(states))
        # breakpoint()
        new_states = {}
        keep_states = {}
        for state in states:
            if state[2] != m:
                keep_states[state] =  states[state]
                continue
            for k, v in add_states(state).items():
                new_states[k] = v
        for k,v in keep_states.items():
            new_states[k] = v
        states = new_states


    # print(states)
    print(max(states.values()))


    result1 = None

    ##########
    # Part 2 #
    ##########



    result2 = None

    print("The result is for part 1 is:", result1)
    print("The result is for part 2 is:", result2)

    return result1, result2

def time():
    with open(os.devnull, 'w') as out:
        sys.stdout = out
        number = 1
        timing = timeit.timeit(solve, number=number) / number
        sys.stdout = sys.__stdout__
    print(f"This took {timing:.6f} seconds")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1][:4] == "time":
        del sys.argv[1]
        time()
    else:
        solve()
