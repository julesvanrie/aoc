def h_v(mapi, x1, x2, y1, y2):
    if x1 != x2:
        x = x1
        while x != x2:
            mapi[y1][x] += 1
            if x > x2:
                x -= 1
            elif x < x2:
                x += 1
        mapi[y1][x] += 1
    else:
        y = y1
        while y != y2:
            mapi[y][x1] += 1
            if y > y2:
                y -= 1
            elif y < y2:
                y += 1
        mapi[y][x1] += 1
    return mapi


with open("input.txt", "r") as fd:
    lines = fd.readlines()

coord = []
t = 0

for line in lines:
    values = line.strip().split(" -> ")
    tmp = (int(values[0].split(',')[0]), int(values[0].split(',')[1]),
           int(values[1].split(',')[0]), int(values[1].split(',')[1]))
    t = max(tmp) if max(tmp) > t else t
    coord.append(tmp)

mapi = []
for index in range(t + 1):
    mapi.append([0 for _ in range(t + 1)])

for xy in coord:
    x1, y1, x2, y2 = xy[0], xy[1], xy[2], xy[3]
    if not (x1 == x2) and not (y1 == y2):
        if abs(x1 - x2) != abs(y1 - y2):
            continue
        while x1 != x2:
            mapi[y1][x1] += 1
            if x1 > x2:
                x1 -= 1
            elif x1 < x2:
                x1 += 1
            if y1 > y2:
                y1 -= 1
            elif y1 < y2:
                y1 += 1
        mapi[y1][x1] += 1
    else:
        mapi = h_v(mapi, x1, x2, y1, y2)

res = 0
for t in mapi:
    for i in t:
        if i > 1:
            res += 1

print(f"RES: {res}")
