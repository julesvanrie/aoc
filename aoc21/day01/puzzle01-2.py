with open("input.txt", "r") as fd:
    lines = fd.readlines()

tmp = []
for index, line in enumerate(lines):
    if index + 2 < len(lines) and index + 1 < len(lines):
        tmp.append(int(line) + int(lines[index + 1]) + int(lines[index + 2]))
    else:
        break

with open("input_2.txt", "w") as fd:
    for line in tmp:
        fd.write(f"{line}\n")
