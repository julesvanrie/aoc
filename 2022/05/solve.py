import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    if not lines:
        text = get_data(sys.argv)

    raw_crates, raw_moves = text.split('\n\n')

    n_crates = int(raw_crates.strip(' \n').split('\n')[-1].split(' ')[-1])

    def move_it(part=1):
        crates = [[] for i in range(n_crates)]

        for crate in raw_crates.split('\n')[-2::-1]:
            pos = []
            for i in range(1, len(crate), 4):
                if crate[i] != ' ':
                    crates[int((i-1)/4)].append(crate[i])

        for move in raw_moves.split('\n'):
            _, n, _, fro, _, to = move.split(' ')
            if part == 1:
                for i in range(int(n)):
                    crates[int(to)-1].append(crates[int(fro)-1].pop())
            if part == 2:
                temp = []
                for i in range(int(n)):
                    temp.append(crates[int(fro)-1].pop())
                crates[int(to)-1].extend(temp[::-1])

        result = ''
        for crate in crates:
            result += crate[-1]

        return result

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
