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


count = 0
for i, line in enumerate(lines):
    opened = []
    for j, digit in enumerate(line):
        if digit in ['{','(','[','<']:
            opened.append(digit)
        else:
            if digit == pairs[opened[-1]]:
                del opened[-1]
            else:
                count += points[digit]
                break

result = count
print(f"Result is {result}")
