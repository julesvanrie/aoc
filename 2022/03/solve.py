import sys
from aochelper import get_data


def solve(lines):
    if not lines:
        lines = get_data(sys.argv)

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
        print(group)
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
