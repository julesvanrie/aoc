with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

lines = [line.split('|') for line in lines]
digits = [line[0].rstrip().split(' ') for line in lines]
outputs = [line[1].lstrip().split(' ') for line in lines]

a = None
b = None
c = None
d = None
e = None
f = None
g = None

def mapi(d):
    if len(d) == 2:
        return 1
    elif len(d) == 3:
        return 7
    elif len(d) == 4:
        return 4
    elif len(d) == 7:
        return 8
    else:
        return None

decoders = [{''.join(sorted(d)): mapi(d) for d in digit}
           for digit in digits]


decoded = [[decoders[i][''.join(sorted(d))] for d in output]
           for i, output in enumerate(outputs)]

# print(digits[0])
# print(outputs[0])
# print(decoders[0])
# print(decoded[0])

count = 0
for line in decoded:
    for d in line:
        if d in [1,4,7,8]:
            count += 1


result = count

print(f"Result is {result}")
