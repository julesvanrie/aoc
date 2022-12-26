with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

polymer = lines[0:1][0]
inserts_list = [line.split(' -> ') for line in lines[2:]]
inserts = {line[0]: line[1] for line in inserts_list}

for step in range(10):
    new_polymer = polymer
    for i in range(len(polymer)-1):
        insert_pos = i * 2 + 1
        insert = inserts[polymer[i:i + 2]]
        new_polymer = new_polymer[:insert_pos] + insert + new_polymer[insert_pos:]
    polymer = new_polymer

counts = {}
for letter in polymer:
    counts[letter] = counts.get(letter, 0) + 1

min = len(polymer)
max = 0
for count in counts.values():
    if count < min:
        min = count
    if count > max:
        max = count

result = max - min

print(f"Result is {result}")
