import sys
from aochelper import get_data


def solve(lines=None):
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')

    ##########
    # Part 1 #
    ##########

    doubles = []
    for line in lines:
        left = line[:int(len(line)/2)]
        right = line[int(len(line)/2):]
        for char in right:
            if char in left:
                doubles.append(char)
                break


    result = 0
    for double in doubles:
        if double >= 'a':
            result += ord(double) - ord('a') + 1
        else:
            result += ord(double) - ord('A') + 27

    print("The result is for part 1 is:", result)

    ##########
    # Part 2 #
    ##########

    doubles = []

    for i in range(int(len(lines) / 3)):
        group = lines[i*3:i*3+3]
        for char in group[0]:
            if char in group[1]:
                if char in group[2]:
                    doubles.append(char)
                    break

    result2 = 0
    for double in doubles:
        if double >= 'a':
            result2 += ord(double) - ord('a') + 1
        else:
            result2 += ord(double) - ord('A') + 27

    print("The result is for part 2 is:", result2)

    return result, result2


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
