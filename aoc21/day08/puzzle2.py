with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

lines = [line.split('|') for line in lines]
digits = [line[0].rstrip().split(' ') for line in lines]
outputs = [line[1].lstrip().split(' ') for line in lines]

def decoder(line):
    '''Returns a dictionary to decode from a sorted string to a number'''
    digits = {}

    digits[1] = [set(d) for d in line if len(d) == 2][0]
    digits[4] = [set(d) for d in line if len(d) == 4][0]
    digits[7] = [set(d) for d in line if len(d) == 3][0]
    digits[8] = [set(d) for d in line if len(d) == 7][0]
    # Split the rest in two groups
    one_hole = [set(d) for d in line if len(d) == 6] # 0, 6, 9
    two_hole = [set(d) for d in line if len(d) == 5] # 2, 3, 5
    # One holes: compare them to what we know already
    digits[9] = [d for d in one_hole if digits[4] < d][0]
    digits[0] = [d for d in one_hole if digits[7] < d and d != digits[9]][0]
    digits[6] = [d for d in one_hole if d not in [digits[9], digits[0]]][0]
    # Two holes: similarly
    digits[3] = [d for d in two_hole if digits[7] < d][0]
    digits[5] = [d for d in two_hole if digits[6] > d][0]
    digits[2] = [d for d in two_hole if d not in [digits[3], digits[5]]][0]

    decoder = {''.join(sorted(v)): str(k) for k, v in digits.items()}
    return decoder

count = 0
for i, line in enumerate(digits):
    decoded = [decoder(line)[''.join(sorted(d))] for d in outputs[i]]
    count += int(''.join(decoded))

result = count

print(f"Result is {result}")
