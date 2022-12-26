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

    current_max = 0

    def find2(start='AA', minutes=26, opened=[], next=None, step=None, ref=0):
        nonlocal current_max

        if minutes == 0:
            return 0

        if len(opened) == len(working):
            # print('reached an end')
            return minutes * sum(flows[valve] for valve in opened)

        if ref + minutes * sum(flows[valve] for valve in working) < current_max:
            # print('reached an impossible end')
            return 0

        options = {}
        for valve in working:
            if valve not in opened:
                # if valve == start or valve == next:
                #     continue
                if valve == next:
                    if len(working) - len(opened) == 1:
                        base = min(step, minutes) * sum(flows[valve] for valve in opened)
                        options[(start, valve)] = base + find2(start=next,
                                             minutes=max(0,minutes-step),
                                             opened=opened+[next],
                                             next=None,
                                             step=None,
                                             ref=ref+base)
                    else:
                        continue
                if not next:
                    distance = 1 if start == valve else distances[(start, valve)] + 1
                    options[(start, valve)] = find2(start=start,
                                             minutes=minutes,
                                             opened=opened,
                                             next=valve,
                                             step=distance)
                else:
                    # if valve == next:
                    #     continue
                    distance = 1 if start == valve else distances[(start, valve)] + 1
                    # if distance == step:
                    #     base = min(distance, minutes) * sum(flows[valve] for valve in opened)
                    #     options[(valve, next)] = base + find2(start=valve,
                    #                          minutes=minutes-distance,
                    #                          opened=opened+[valve, next],
                    #                          next=next,
                    #                          step=0)
                    #     continue
                    # if distance == step:
                    #     continue
                    if distance < step:
                        next_step = step - distance
                        first_valve = valve
                        next_valve = next
                    else:
                        next_step = distance - step
                        distance = step
                        first_valve = next
                        next_valve = valve
                    base = min(distance, minutes) * sum(flows[valve] for valve in opened)
                    options[(first_valve, next_valve)] = base + find2(start=first_valve,
                                             minutes=max(0,minutes-distance),
                                             opened=opened+[first_valve],
                                             next=next_valve,
                                             step=next_step,
                                             ref=ref+base)
        result = max(options.values())
        if ref + result > current_max:
            current_max = ref + result
            print(current_max, end='\r')
        if options:
            return result
        else:
            return 0


    result2 = find2()

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
