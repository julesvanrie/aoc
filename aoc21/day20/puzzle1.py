with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

algo = [1 if d == '#' else 0 for d in lines[0]]

image = [[1 if d == '#' else 0 for d in line] for line in lines[2:]]

def step(image, step_number):
    new = []
    height = len(image)
    width = len(image[0])
    for y in range(-1, height + 1):
        new_line = []
        for x in range(-1, width + 1):
            code = []
            for y_code in range(y-1, y+2):
                for x_code in range(x-1, x+2):
                    if x_code >= 0 and x_code < width and y_code >= 0 and y_code < height:
                        code.append(str(image[y_code][x_code]))
                    else:
                        # Here's the crucial step...
                        if algo[0] == 1 and step_number % 2 == 1:
                            code.append('1')
                        else:
                            code.append('0')
            code_number = int('0b' + ''.join(code), 2)
            decoded = algo[code_number]
            new_line.append(decoded)
        new.append(new_line)
    return new

for i in range(2):
    image = step(image, i)

count = 0
for i in image:
    count += sum(i)
    # for d in i:
    #     if d == 1:
    #         print('#', end='')
    #     else:
    #         print('.', end='')
    # print('')

result = count

print(f"Result for part 1 is {result}")

for i in range(48):
    image = step(image, i)

count = 0
for i in image:
    count += sum(i)

result = count

print(f"Result for part 2 is {result}")
