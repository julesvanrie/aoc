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
    print(flows['DD'], connections['DD'])
    print(working)
    ##########
    # Part 1 #
    ##########


    paths = {}
    closed = working.copy()

    def search(valve='AA', minutes=30, pressure=0, closed=None, path=None):
        if closed is None:
            closed = working.copy()
        if len(closed) == 0 or minutes == 0:
            # return [], minutes, pressure
            paths[tuple(path)] = pressure
            return minutes, pressure
        if path is None:
            path = []
        candidates = connections[valve].copy()
        candidates.append(valve)
        for cand in candidates:
            if cand in working and cand in closed:
                if cand == valve:
                    closed.pop(cand)
                    minutes -= 1
                    pressure += minutes * flows[cand]
                    return minutes, pressure
                else:
                    path.append(cand)
                    m, p =  search(valve=cand, minutes=minutes-1, pressure=pressure, closed=closed, path=path)
                    return minutes + m, pressure + m


    def search(valve='AA', minutes=30, flow=0, closed=None, path=None):
        if closed is None:
            closed = working.copy()
        if minutes == 0:
            return 0
        if len(closed) == 0:
            return minutes * flow
        candidates = connections[valve].copy()
        candidates.append(valve)
        temp = []
        for cand in candidates:
            if cand in working and cand in closed:
                if cand == valve:
                    closed.pop(cand)
                    nexts = connections[valve].copy()
                    minutes -= 1
                    flow += flows[cand]
                    rest = search(val)
                    temp.append(flow * minutes + rest)
                else:
                    path.append(cand)
                    m, p =  search(valve=cand, minutes=minutes-1, flow=flow, closed=closed, path=path)
                    return minutes + m, pressure + m


    def search(path, pressure=0, minutes=30, closed=None):
        # breakpoint()
        if len(paths) > 100:
            print(paths)
            exit()
        if not closed:
            return
        current_closed = closed.copy()
        if not minutes:
            paths[tuple(path)] = pressure
            return
        if not connections[path[-1]]:
            if path[-1] in closed:
                minutes -= 1
                paths[tuple(path)] = pressure + minutes * flows[path[-1]]
            else:
                paths[tuple(path)] =  pressure
            return
        if path[-1] in closed:
            for conn in connections[path[-1]]:
                temp_closed = current_closed.copy()
                temp_closed.remove(path[-1])
                search(path + [conn],
                       pressure = pressure + flows[path[-1]] * (minutes - 2),
                       closed = temp_closed)
        for conn in connections[path[-1]]:
            search(path+[conn], pressure=pressure, minutes=minutes-1, closed=current_closed)


    states = {(('AA',), tuple(closed.copy()), 0): 0}


    def add_states(state):
        new_states = {}
        # breakpoint()
        if not closed:
            return new_states

        new_one = state[0][-1]
        if new_one in closed:
            new_path = tuple(list(state[0]) + [new_one])
            new_closed = list(closed)
            new_closed.remove(new_one)
            new_minute = state[2] + 1
            new_pressure = states[state] + flows[state[0][-1]] *  (30 - new_minute)
            new_state = (new_path, tuple(new_closed), new_minute)
            if new_states.get(new_state, 0) <= new_pressure:
                new_states[new_state] =  new_pressure
        # print(state)
        for conn in connections[state[0][-1]]:
            # print(conn)
            new_path =  tuple(list(state[0]) + [conn])
            new_closed = tuple(list(closed))
            new_minute = state[2] + 1
            new_pressure = states[state]
            new_state = (new_path, new_closed, new_minute)
            if new_states.get(new_state, 0) <= new_pressure:
                new_states[new_state] =  new_pressure

        return new_states

    for m in range(30, 0, -1):
        print(m, end='\r')
        # breakpoint()
        temp = {state: pressure for state, pressure in states.items() if state[1]}
        new_states = {}
        max_pressure = 0
        highest_state = None
        for state in temp:
            if not closed:
                this_pressure = states[state]
                if this_pressure > max_pressure:
                    max_pressure = this_pressure
                    highest_state = None
                continue
            new_ones = add_states(state)
            for k, v in new_ones.items():
                new_states[k] = v
        if highest_state:
            new_states[highest_state] = max_pressure
        states = new_states

    # print(search(['AA'], closed=closed))
    print(states)



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
