import sys
from aochelper import get_data

lines = get_data(sys.argv)

pairs = [line.split(',') for line in lines]

count1 = 0; count2 = 0
for l, r in pairs:
    l = [int(c) for c in l.split('-')]
    r = [int(c) for c in r.split('-')]
    full = 0; overlap = 0
    if l[0] <= r[0] and l[1] >= r[1]: full = 1
    if r[0] <= l[0] and r[1] >= l[1]: full = 1
    if not(l[1] < r[0] or l[0] > r[1]): overlap = 1
    count1 += full; count2 += overlap

print("The result is for part 1 is:", count1)
print("The result is for part 2 is:", count2)
