with open('test.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

lines = [line.split(' ') for line in lines]

# model_number = 13579246899999

mem = {
    'w': 0,
    'x': 0,
    'y': 0,
    'z': 0,
}


states = []


input = None

def operation(instruction, arg=None):
    operator = instruction[0]
    op1 = instruction[1]
    if operator == 'inp':
        mem[op1] = arg
        return
    else:
        op2 = instruction[2]
        if op2 in mem.keys():
            op2 = mem[op2]
        else:
            op2 = int(op2)
    if operator == 'add':
        mem[op1] += op2
    elif operator == 'mul':
        mem[op1] *= op2
    elif operator == 'div':
        if mem[op1] >= 0:
            mem[op1] = mem[op1] // op2
        else:
            mem[op1] = ((mem[op1] -1) // op2) + 1
    elif operator == 'mod':
        mem[op1] = mem[op1] % op2
    elif operator == 'eql':
        mem[op1] = 1 if mem[op1] == op2 else 0
    return

def reset_mem():
    for k in mem.keys():
        mem[k] = 0

def load_input(number):
    global input
    input = [int(d) for d in str(number)]

def run_alu(number):
    global input
    reset_mem()
    load_input(number)
    for instruction in lines:
        operation(instruction, input)

def count_inputs():
    return len([1 for line in lines if line[0] == 'inp'])

def reduce_number(number, length):
    new_number = number - 1
    str_number = str(new_number)
    if len(str_number) < length:
        return None
    for i, d in enumerate(str_number):
        # print(i, d)
        if d == '0':
            new_number -= int(str_number[i:])
            new_number = reduce_number(new_number, length)
    # print(new_number)
    return new_number

def is_valid_z(z):
    if z == 0:
        result = True
    else:
        result = False
    return result

def find_model_number():
    length = count_inputs()
    model_number = int(''.join(['9' for d in range(length)]))
    # for i in range(100):
    while True:
        run_alu(model_number)
        if is_valid(mem['z']):
            return model_number
        else:
            model_number = reduce_number(model_number, length)
        print(model_number)

# test = 113
# for i in range(20):
#     test = reduce_number(test, 3)
#     print(test)

operation(lines[0], -51)
print(mem)
operation(lines[1])
# result = find_model_number()

print(mem)

print(f"Result for part 1 is {result}")
