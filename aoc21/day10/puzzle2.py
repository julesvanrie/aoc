with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

# lines = [letter for letter in list(line)] for line in lines]

length = len(lines)
width = len(lines[0])

pairs = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}
points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
points_i = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}
count = 0
discard = []
scores = []
for i, line in enumerate(lines):
    opened = []
    for j, digit in enumerate(line):
        if digit in ['{', '(', '[', '<']:
            opened.append(digit)
        else:
            if digit == pairs[opened[-1]]:
                del opened[-1]
            else:
                count += points[digit]
                discard.append(i)
                opened.clear()
                break
    if len(opened) > 0:
        score = 0
        for digit in opened[::-1]:
            line += pairs[digit]
            score *= 5
            score += points_i[pairs[digit]]
        scores.append(score)

# for line in discard[::-1]:
    # del lines[line]

middle = int((len(scores) -1) / 2)

# print(middle)
# print(sorted(scores))
result = sorted(scores)[middle]

print(f"Result is {result}")
