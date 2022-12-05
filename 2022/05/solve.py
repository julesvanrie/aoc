import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    if not lines:
        lines = get_data(sys.argv)


    text = ''.join(lines)

    raw_crates, raw_moves = text.split('\n\n')

    n_crates = int(raw_crates.strip(' \n').split('\n')[-1].split(' ')[-1])

    crates = []
    for i in range(n_crates):
        crates.append([])

    for crate in raw_crates.split('\n')[-2::-1]:
        pos = []
        for i in range(1, len(crate), 4):
            if crate[i] != ' ':
                crates[int((i-1)/4)].append(crate[i])


    moves = []
    for move in raw_moves.strip().split('\n'):
        _, n, _, fro, _, to = move.split(' ')
        moves.append((n, fro, to))
        for i in range(int(n)):
            crates[int(to)-1].append(crates[int(fro)-1].pop())

    result1 = ''
    for crate in crates:
        result1 += crate[-1]

    ##########
    # Part 1 #
    ##########


    ##########
    # Part 2 #
    ##########

    crates = []
    for i in range(n_crates):
        crates.append([])

    for crate in raw_crates.split('\n')[-2::-1]:
        pos = []
        for i in range(1, len(crate), 4):
            if crate[i] != ' ':
                crates[int((i-1)/4)].append(crate[i])


    moves = []
    for move in raw_moves.strip().split('\n'):
        _, n, _, fro, _, to = move.split(' ')
        moves.append((n, fro, to))
        temp = []
        for i in range(int(n)):
            temp.append(crates[int(fro)-1].pop())
        crates[int(to)-1].extend(temp[::-1])

    result2 = ''
    for crate in crates:
        result2 += crate[-1]

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
