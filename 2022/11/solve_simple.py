import os, sys, timeit
from aochelper import get_data
from pprint import pprint

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')

    text = lines if lines else get_data(sys.argv)
    monkey_text = text.split('\n\n')

    def solve_part(part):
        monkeys = []
        for t in monkey_text:
            i = t.split('\n')
            monkeys.append({
                'items': [int(item) for item in i[1].split(': ')[1].split(', ')],
                'operation': i[2].split(' = ')[1],
                'test': int(i[3].split(' by ')[1]),
                'true': int(i[4].split('monkey ')[1]),
                'false': int(i[5].split('monkey ')[1]),
            })

        divisors = [monkey['test'] for monkey in monkeys]
        multiple = 1
        for divisor in divisors:
            multiple *= divisor

        insp = [0 for i in range(len(monkeys))]
        for round in range(20 if part == 1 else 10000):
            for i, monkey in enumerate(monkeys):
                insp[i] += len(monkey['items'])
                for _ in range(len(monkey['items'])):
                    old = monkey['items'].pop(0)
                    if part == 1:
                        new = eval(monkey['operation']) // 3
                    else:
                        new = eval(monkey['operation']) % multiple
                    if new % monkey['test']:
                        monkeys[monkey['false']]['items'].append(new)
                    else:
                        monkeys[monkey['true']]['items'].append(new)

        return sorted(insp)[-1] * sorted(insp)[-2]

    result1 = solve_part(1)

    result2 = solve_part(2)
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
