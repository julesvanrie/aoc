with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

nb_lines = len(lines)

def most_freq(l):
    length = len(l[0])
    result = []
    for pos in range(length):
        result.append(sum([int(line[pos]) for line in l]) > nb_lines / 2)
    return result

freq = most_freq(lines)
gamma = int('0b' + ''.join(['1' if pos else '0' for pos in freq]), 2)
epsilon = int('0b' + ''.join(['0' if pos else '1' for pos in freq]), 2)

result = gamma * epsilon

print(f"Result is {result}")
