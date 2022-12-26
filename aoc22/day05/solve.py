import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    text = lines if lines else get_data(sys.argv)

    raw_crates, raw_moves = text.split('\n\n')

    n_crates = int(raw_crates.strip(' \n').split('\n')[-1].split(' ')[-1])

    def move_it(part=1):
        crates = [[] for i in range(n_crates)]

        for line in raw_crates.split('\n')[-2::-1]:
            for i in range(int((len(line)+1)/4)):
                if line[i*4+1] != ' ':
                    crates[i].append(line[i*4+1])

        for move in raw_moves.split('\n'):
            _, n, _, fro, _, to = move.split(' ')
            n = int(n); fro = int(fro); to = int(to)
            if part == 1:
                [crates[to-1].append(crates[fro-1].pop()) for i in range(n)]
            if part == 2:
                temp = [crates[fro-1].pop() for i in range(n)]
                crates[to-1].extend(temp[::-1])

        return ''.join(crate[-1] for crate in crates)

    result1 = move_it(part=1)
    result2 = move_it(part=2)

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
