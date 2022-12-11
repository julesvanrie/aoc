import os, sys, timeit
from aochelper import get_data
from pprint import pprint

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')

    text = lines if lines else get_data(sys.argv)
    monkey_text = text.split('\n\n')

    ##########
    # Part 1 #
    ##########

    monkeys = []
    for t in monkey_text:
        i = t.split('\n')
        monkeys.append({
            'start': [int(item) for item in i[1].split(': ')[1].split(', ')],
            'items': [],
            'operation': i[2].split(' = ')[1],
            'op': i[2].split(' ')[-2],
            'nb': i[2].split(' ')[-1],
            'test': int(i[3].split(' by ')[1]),
            'true': int(i[4].split('monkey ')[1]),
            'false': int(i[5].split('monkey ')[1]),
        })

    dividors = [monkey['test'] for monkey in monkeys]
    for monkey in monkeys:
        for item in monkey['start']:
            monkey['items'].append({d: item % d for d in dividors})


    print(monkeys[0])
    # breakpoint()
    # while sum(len(i['items']) for i in monkeys):
    insp = [0 for i in range(len(monkeys))]
    for round in range(10000):
        # if print(round, end='\r')
        # breakpoint()
        for i, monkey in enumerate(monkeys):
            insp[i] += len(monkey['items'])
            for _ in range(len(monkey['items'])):
                olditems = monkey['items'].pop(0)
                new = {k: eval(monkey['operation']) % k for k, old in olditems.items()}
                # nb = monkey['nb']
                # if monkey['op'] == '+':
                #     new = {k: (o + int(nb)) % k for k, o in old.items()}
                # else:
                #     new = old
                # new = new // 3
                if new[monkey['test']]:
                    monkeys[monkey['false']]['items'].append(new)
                else:
                    monkeys[monkey['true']]['items'].append(new)
        # pprint(monkeys)

    # pprint([monkey['items'] for monkey in monkeys])

    print(insp)

    result1 = sorted(insp)[-1] * sorted(insp)[-2]
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
