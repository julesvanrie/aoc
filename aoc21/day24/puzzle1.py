with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

lines = [line.split(' ') for line in lines]

sub_alus = []
tmp = []
for line in lines:
    if line[0] == 'inp':
        if len(tmp) > 0:
            sub_alus.append(tmp)
        tmp = []
    else:
        tmp.append(line)
sub_alus.append(tmp)

# print(sub_alus[1])

mem = {
    'w': 0,
    'x': 0,
    'y': 0,
    'z': 0,
}


states = [{} for i in range(len(sub_alus))]

# print(len(states))

input = None

def operation(instruction):
    operator = instruction[0]
    op1 = instruction[1]
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

def run_sub_alu(iteration):
    if iteration == 0:
        previous_states = [0]
    else:
        previous_states = list(states[iteration-1].values())
    for digit in range(1,10):
        for prev_state in previous_states:
            reset_mem()
            mem['w'] = digit
            mem['z'] = prev_state
            state = (digit, prev_state)
            for instruction in sub_alus[iteration]:
                operation(instruction)
            states[iteration][state] = mem['z']

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

length = len(sub_alus)
# length = 3

for i in range(length):
    run_sub_alu(i)
    print(len(states[i]))

# print(states[1])

def find_targets(target, position):
    tmp = []
    for key, state in states[position].items():
        if state == target:
            tmp.append(key)
    # targets[i][target] = tmp
    return tmp

# target = 9025
targets = {}
targets[length] = {0: [('',0)]}
# print(targets[3])

for i in range(length, 0,-1):
    # print(i, len(states[i]))
    tmp = {}
    # print(targets[i])
    for target_list in targets[i].values():
        # print(target_list)
        for _, target in target_list:
            tmp[target] = find_targets(target, i-1)
    targets[i-1] = tmp

# print(targets)

results = []
# digits = [0 for i in range(length)]

def get_next_digits(target, position):
    tmp = targets[position][target]
    digits = []
    for digit, state in tmp:
        if position > 0:
            next_digits = get_next_digits(state, position-1)
            for next_digit in next_digits:
                digits.append(next_digit + str(digit))
        else:
            digits.append(str(digit))
    return digits

results = [int(d) for d in get_next_digits(0, 3)]


print(results)

# test = 113
# for i in range(20):
#     test = reduce_number(test, 3)
#     print(test)

# operation(lines[0], -51)
# print(mem)
# operation(lines[1])
# result = find_model_number()

# print(mem)

result = max(results)

print(f"Result for part 1 is {result}")
