with open("input_2.txt", "r") as fd:
    lines = fd.readlines()

total = 0
for index, line in enumerate(lines):
    if index == 0:
        continue
    elif int(lines[index - 1]) < int(line):
        total += 1

print(f"Total: {total}")
