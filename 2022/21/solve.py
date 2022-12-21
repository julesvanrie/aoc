import os, sys, timeit
from aochelper import get_data
from pprint import pprint

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')

    known = {}
    tbd = {}

    # Parsing
    def initiate():
        nonlocal known, tbd
        known = {}
        tbd = {}
        for line in lines:
            key, value = line.split(': ')
            try:
                value = int(value)
                known[key] = int(value)
            except:
                value = value.split(' ')
                tbd[key] = value
        return known, tbd

    def op(left, right, op):
        if op == '+':
            return known[left] + known[right]
        if op == '-':
            return known[left] - known[right]
        if op == '*':
            return known[left] * known[right]
        if op == '/':
            return (known[left] / known[right])



    ##########
    # Part 1 #
    ##########

    def calc(root, tree=None):
        if not tree:
            tree = set(tbd.keys())
        while root not in known:
            for monkey, value in tbd.items():
                if monkey not in known and monkey in tree:
                    if value[0] in known and value[2] in known:
                        known[monkey] = op(value[0], value[2], value[1])
                if root in known:
                    break

            # if 'root' in known:
            #     break
        return known[root]

    initiate()

    result1 = calc('root')
    print("The result is for part 1 is:", result1)

    ##########
    # Part 2 #
    ##########

    initiate()
    firsttree = set()
    human_tree_nb = 2

    def find(root):
        left = tbd[root][0]
        right = tbd[root][2]
        if left == 'humn' or right == 'humn':
            nonlocal human_tree_nb
            human_tree_nb = 0
        if left not in known:
            firsttree.add(left)
            find(left)
        if right not in known:
            firsttree.add(right)
            find(right)

    find(tbd['root'][0])
    firsttree.add(tbd['root'][0])

    if human_tree_nb == 0:
        human_tree = firsttree
        monkey_tree = set(tbd.keys()) -  firsttree
        human_tree_root = tbd['root'][0]
        monkey_tree_root = tbd['root'][2]
    else:
        monkey_tree = firsttree
        human_tree = set(tbd.keys()) -  firsttree
        human_tree_root = tbd['root'][2]
        monkey_tree_root = tbd['root'][0]

    monkey_tree_result = calc(monkey_tree_root)
    print('monkey', monkey_tree_result)

    check = False


    def target(start=0, end= 1_000_000_000_000_000):
        test = [start, ((start+end)/2), end]
        results = []
        for t in test:
            initiate()
            known['humn'] = t
            results.append(calc(human_tree_root, human_tree))
        print(monkey_tree_result, results)
        if monkey_tree_result in results:
            return test[results.index(monkey_tree_result)]
        if monkey_tree_result > results[0] and monkey_tree_result < results[1]:
            return target(start=test[0], end=test[1])
        if monkey_tree_result < results[0] and monkey_tree_result > results[1]:
            return target(start=test[0], end=test[1])
        if monkey_tree_result > results[1] and monkey_tree_result < results[2]:
            return target(start=test[1], end=test[2])
        if monkey_tree_result < results[1] and monkey_tree_result > results[2]:
            return target(start=test[1], end=test[2])

        # check = human_tree_result == monkey_tree_result
        # print(monkey_tree_result, human_tree_result)



    result2 = target()

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
