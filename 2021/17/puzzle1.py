with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

x_range = lines[0].split(',')[0].split('=')[1].split('..')
y_range = lines[0].split(',')[1].split('=')[1].split('..')

min_x = int(x_range[0])
max_x = int(x_range[1])
min_y = int(y_range[0])
max_y = int(y_range[1])

def step(x, y, v_x, v_y):
    x += v_x
    y += v_y
    if v_x > 0:
        v_x -= 1
    elif v_x < 0:
        v_x += 1
    else:
        pass
    v_y -= 1
    return x, y, v_x, v_y

def check(x, y):
    if y < min_y or x > max_x:
        return -1    # overshooted
    if x >= min_x and x <= max_x and y <= max_y and y >= min_y:
        return 0     # target reached
    return 1         # else continue

x_s = []
y_s = []
v_x_s = []
v_y_s = []
y_max_s = []

for v_x_i in range(1, max_x):
    for v_y_i in range(min_y, 200):
        x = 0
        y = 0
        v_x = v_x_i
        v_y = v_y_i
        y_max = 0
        another_one = 1
        while another_one == 1:
            x, y, v_x, v_y = step(x, y, v_x, v_y)
            if y > y_max:
                y_max = y
            another_one = check(x, y)
            if another_one == 0:
                x_s.append(x)
                y_s.append(y)
                v_x_s.append(v_x_i)
                v_y_s.append(v_y_i)
                y_max_s.append(y_max)

y_max = max(y_max_s)
i = y_max_s.index(y_max)

result = (y_max, x_s[i], y_s[i], v_x_s[i], v_y_s[i])
print(result)
print(f"Result is {result[0]}")
