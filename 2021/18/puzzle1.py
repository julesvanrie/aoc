with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]


def parse(line):
    digits = []
    levels = []
    splits = []
    pos = 0
    level = 0
    for c in line:
        if c == '[':
            level += 1
        elif c == ']':
            level -= 1
        elif c == ',':
            splits.append(level)
            pos += 1
        else:
            digits.append(int(c))
            levels.append(level)
    return digits, levels, splits


def add(left, right):
    digits = left[0] + right[0]
    levels = left[1] + right[1]
    splits = left[2] + [0] + right[2]
    levels = [level + 1 for level in levels]
    splits = [split + 1 for split in splits]
    return digits, levels, splits


def reduce(fish):
    start_len = len(fish[0])
    digits = fish[0]
    levels = fish[1]
    splits = fish[2]
    # Do explosions, if any
    i = 0
    while i < len(digits):
        if levels[i] > 4:
            if i > 0:
                digits[i-1] += digits[i]
            if i < len(digits) - 2:
                digits[i+2] += digits[i+1]
            digits[i] = 0
            levels[i] -= 1
            digits.pop(i+1)
            levels.pop(i+1)
            splits.pop(i)
            break
        i += 1
    # If no explosions, check for splits
    else:
        i = 0
        while i < len(digits):
            if digits[i] > 9:
                left = digits[i] // 2
                right = digits[i] - left
                digits[i] = left
                digits.insert(i+1, right)
                levels[i] += 1
                levels.insert(i+1, levels[i])
                splits.insert(i, levels[i])
                break
            i += 1
    new_fish = (digits, levels, splits)
    # If something happend, do an extra run, to check for further actions
    if len(new_fish[0]) != start_len:
        new_fish = reduce(new_fish)
    return new_fish


def magnitude(element):
    if len(element[0]) == 1:
        mag = element[0][0]
    else:
        splits = element[2]
        for i, split in enumerate(splits):
            if split == 1:
                splits_red = [split - 1 for split in splits]
                left = (element[0][:i + 1], element[1][:i + 1], splits_red[:i])
                right = (element[0][i + 1:], element[1][i + 1:],
                         splits_red[i + 1:])
                break
        mag = 3 * magnitude(left) + 2 * magnitude(right)
    return mag

##############
# FOR PART 1 #
##############

# Loop through all lines and add up
left = parse(lines.pop(0))
for i in range(len(lines)):
    right = parse(lines.pop(0))
    left = reduce(add(left, right))

result = magnitude(left)

print(f"Result for part 1 is {result}")
