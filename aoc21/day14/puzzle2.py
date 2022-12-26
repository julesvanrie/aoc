with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

polymer = lines[0:1][0]
inserts_list = [line.split(' -> ') for line in lines[2:]]
inserts = {line[0]: line[1] for line in inserts_list}

# Initial pairs
pairs = {}
for i in range(len(polymer) - 1):
    pair = polymer[i:i+2]
    pairs[pair] = pairs.get(pair, 0) + 1

for step in range(40):
    for pair, count in pairs.copy().items():
        p1 = pair[0] + inserts[pair]
        p2 = inserts[pair] + pair[1]
        pairs[pair] -= count
        pairs[p1] = pairs.get(p1, 0) + count
        pairs[p2] = pairs.get(p2, 0) + count

counts = {}
for pair, count in pairs.items():
    counts[pair[0]] = counts.get(pair[0], 0) + count

# Add last letter
counts[polymer[-1]] = counts.get(polymer[-1], 0) + 1

min = 2**64
max = 0
for count in counts.values():
    if count < min:
        min = count
    if count > max:
        max = count

result = max - min

print(f"Result is {result}")
