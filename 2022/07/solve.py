import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')

    tree = {}
    current = 'root'

    for line in lines[1:]:
        if line == '$ cd ..':
            current = current[:current.rfind('/')]
            continue
        if line[:4] == '$ cd':
            current += '/' + line[5:]
            if not tree.get(current, None):
                tree[current] = 0
            continue
        if line == '$ ls':
            continue
        if line[:4] == 'dir ':
            continue
        else:
            tree[current] = tree.get(current, 0) + int(line.split(' ')[0])

    sizes = []

    def du(folder):
        nonlocal sizes
        size = tree[folder]
        for k, v in tree.items():
            if folder in k:
                if k.count('/') == folder.count('/') + 1:
                    size += du(k)
        sizes.append(size)
        return size

    used = du('root')
    smalls = [size for size in sizes if size <= 100000]
    result1 = sum(smalls)

    # Part 2 #

    total = 70000000
    needed = 30000000
    candidates = [size for size in sizes if total - used + size >= needed]
    result2 = min(candidates)

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
