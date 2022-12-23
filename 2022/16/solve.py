import os, sys, timeit
from aochelper import get_data
from datetime import datetime

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

    ##########
    # Part 1 #
    ##########

    def shortest(head, tail, visited):
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


    # Distances key is head, tail. Value is shortest distance.
    distances = {}
    for head in working + ['AA']:
        for tail in working:
            if head != tail:
                if (tail,head) in distances:
                    distances[(head, tail)] = distances[(tail, head)]
                else:
                    distances[(head, tail)] = shortest(head, tail, [])


    def find(start='AA', minutes=30, opened=[], part=1):
        if minutes <= 0:
            return 0

        if len(opened) == len(working):
            return minutes * sum(flows[valve] for valve in opened)

        options = {}
        for valve in working:
            if valve not in opened:
                distance = 1 if start == valve else distances[(start, valve)] + 1
                base = min(distance, minutes) * sum(flows[valve] for valve in opened)
                options[valve] = base + find(start=valve,
                                             minutes=minutes-distance,
                                             opened=opened+[valve])
        return max(options.values())


    result1 = find('AA')
    print("The result is for part 1 is:", result1)


    ##########
    # Part 2 #
    ##########


    result2 = None

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
