import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')
    text = lines if lines else get_data(sys.argv)
    input = text.split('\n\n')

    pairs = [[eval(lr) for lr in inp.split('\n')] for inp in input]

    def compare(left, right):
        if type(left) == int and type(right) == int:
                return None if left == right else left < right
        if type(left) == int:
            left = [left]
        if type(right) == int:
            right = [right]
        for i in range(min(len(left), len(right))):
            result = compare(left[i], right[i])
            if result is None:
                continue
            return result
        if len(left) ==  len(right):
            return None
        return len(left) < len(right)

    ##########
    # Part 1 #
    ##########
    results = [compare(pair[0], pair[1]) for pair in pairs]

    # print(results)

    result1 = 0
    for i, r in enumerate(results, 1):
        if r:
            result1 += i


    ##########
    # Part 2 #
    ##########



    # compare(pairs[1][0], pairs[1][1])

    unordered = [[[2]], [[6]]]
    [unordered.extend(pair) for pair in pairs]
    # print(unordered)

    for i in range(len(unordered)):
        for j in range(i+1, len(unordered)):
            if not compare(unordered[i], unordered[j]):
                temp = unordered[i]
                unordered[i] = unordered[j]
                unordered[j] = temp

    result2 = 1
    for i, test in enumerate(unordered, 1):
        if test in [[[2]],[[6]]]:
            result2 *= i

    # results = [compare(pair[0], pair[1]) for pair in pairs]

    # [print(unord) for unord in unordered]

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
