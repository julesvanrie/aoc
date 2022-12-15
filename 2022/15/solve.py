import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')

    sensors = []
    beacons = []
    for line in lines:
        tmp = line.split(':')
        bx, by = tmp[0].split(',')
        sx, sy = tmp[1].split(',')
        bx, by, sx, sy = [int(t.split('=')[1]) for t in [bx, by, sx, sy]]
        sensors.append((bx, by))
        beacons.append((sx, sy))

    def man(s, b):
        return abs(s[0] - b[0]) + abs(s[1] - b[1])

    ##########
    # Part 1 #
    ##########

    def cov_row(s, man, r):
        if man <= 0:
            return None
        ver = abs(s[1] - r)
        if ver > man:
            return None
        hor = max(man - ver, 0)
        return (s[0] - hor, s[0] + hor)

    def total_cov_row(r):
        cov = []
        for s, b in zip(sensors, beacons):
            cov_r = cov_row(s, man(s, b), r)
            if cov_r:
                cov.append(cov_r)
        return cov

    def xminmax(r):
        cov = total_cov_row(r)
        xmin = 2*62
        xmax = -2*62
        for c in cov:
            xmin = min(xmin, c[0])
            xmax = max(xmax, c[1])
        return xmin-1, xmax+1

    def is_covered(x,y):
        cov = total_cov_row(y)
        for c in cov:
            if x >= c[0] and x <= c[1]:
                return True
        return False

    def print_row(r):
        cov = total_cov_row(r)
        for x in range(-5,26):
            done = False
            for b in beacons:
                if b[1] == r and x == b[0]:
                    print('B', end='')
                    done = True
                    break
            if done:
                continue
            for s in sensors:
                if s[1] == r and x == s[0]:
                    print('S', end='')
                    done = True
                    break
            if done:
                continue
            for c in cov:
                if x >= c[0] and x <= c[1]:
                    print('#', end='')
                    done = True
                    break
            if done:
                continue
            print('.', end='')
        print('')


    def reduce_cov_two(l, r):
        if l[0] <= r[0] and l[1] >= r[1]:
            return [l]
        if l[0] >= r[0] and l[1] <= r[1]:
            return [r]
        if l[1] < r[0]:
            return [l, r]
        if r[1] < l[0]:
            return [r, l]
        if l[0] < r[0] and l[1] < r[1]:
            return [(l[0], r[1])]
        if l[0] > r[0] and l[1] > r[1]:
            return [(r[0], l[1])]


    def reduce_cov_all(cov):
        new = []
        keeps = set()
        removes = set()
        # breakpoint()
        for i in range(len(cov)):
            # if i == 8:
            #     breakpoint()
            if i in removes:
                continue
            for j in range(len(cov)):
                # if j == 8:
                    # breakpoint()
                if i == j or j in removes:
                    continue
                red = reduce_cov_two(cov[i], cov[j])
                if len(red) == 2:
                    keeps.update([i,j])
                else:
                    removes.add(i)
                    if i in keeps:
                        keeps.remove(i)
                    removes.add(j)
                    if j in keeps:
                        keeps.remove(j)
                    new.append(red[0])
        for k in keeps:
            new.append(cov[k])
        return new






    # print(sensors[6],beacons[6])
    # print(man(sensors[6],beacons[6]))

    # print(cov_row(sensors[6], man(sensors[6],beacons[6]), 10))

    # print(total_cov_row(11))
    # # print(reduce_cov_all(total_cov_row(10)))
    # for r in range(-2, 23):
    #     print_row(r)

    def part1(r):
        total = 0
        cov = total_cov_row(r)
        for x in range(*xminmax(r)):
            for c in cov:
                if x >= c[0] and x <= c[1]:
                    total += 1
                    break
            for b in beacons:
                if b[1] == r and x == b[0]:
                    total -= 1
                    break
            for s in sensors:
                if s[1] == r and x == s[0]:
                    total -= 1
                    break
        return total

    # print(xminmax(10))
    # print("For test:", part1(9))
    # print("For test:", part1(10))
    # print("For test:", part1(11))
    # result1 = part1(10)
    # result1 = part1(2000000)
    result1 = None

    ##########
    # Part 2 #
    ##########

    def cut(start, c):
        if c[1] < start[0]:
            return [start]
        if c[0] > start[1]:
            return [start]
        if c[0] <= start[0] and c[1] >= start[1]:
            return []
        if c[0] > start[0] and c[1] > start[1]:
            return [(start[0], c[0]-1)]
        if c[0] < start[0] and c[1] < start[1]:
            return [(c[1]+1, start[1])]
        if c[0] > start[0] and c[1] < start[1]:
            return [(start[0], c[0]-1), (c[1]+1, start[1])]


    def check_range(start=(0,26), cov=[]):
        ranges = {start}
        while len(ranges) >= 1 and list(ranges)[0][0] != list(ranges)[0][1]:
            # print(ranges)
            first = ranges.pop()
            temp = set()
            for c in cov:
                # if isinstance(start, int):
                #     breakpoint()
                slices = cut(first, c)
                if not slices:
                    temp = set()
                    break
                for slice in slices:
                    # print(slices, end=' ')
                    temp.add(slice)
                    # print(ranges)
                    # return ranges.extend(check_range(sl, cov) for sl in slices)
                print('F', first, 'C', c, 'ranges', temp)
            for t in temp:
                ranges.add(t)
            print(ranges)
        return ranges
        result = []
        for ra in ranges:
            # if isinstance(ra, tuple):
            #     breakpoint()
            next = check_range(ra, cov)
            if next:
                result.extend(next)
        print(ranges, result)
        return result




    def check_range(start=(0,26), cov=[]):
        ranges = set()
        for c in cov:
            # if isinstance(start, int):
            #     breakpoint()
            slices = cut(start, c)
            if not slices:
                ranges = set()
                break
            for slice in slices:
                # print(slices, end=' ')
                ranges.add(slice)
                # print(ranges)
                # return ranges.extend(check_range(sl, cov) for sl in slices)
            print('start', start, 'C', c, 'ranges', ranges)
        while ranges:
            current = ranges.pop()
            temp = check_range(current, cov)
            for t in temp:
                ranges.add(t)
            if current == temp:
                return ranges
        return {}

    def check_range(start=(0,20), cov=[]):
        if len(cov) == 0:
            return {start}
        ranges = set()
        # breakpoint()
        # if isinstance(start, int):
        #     breakpoint()
        slices = cut(start, cov[0])
        if not slices:
            return {}
        for slice in slices:
            for t in check_range(slice, cov[1:]):
                ranges.add(t)
        # print(len(cov), ranges)
        return ranges




    print(total_cov_row(11))
    print(check_range(cov=total_cov_row(11)))

    def part2(area):
        for r in range(area+1):
            if not (r % 1000):
                print(r, end='\r')
            ch = list(check_range(start=(0,area), cov=total_cov_row(r)))
            if len(ch) == 1 and ch[0][0] == ch[0][1]:
                return ch[0][0] * area + r
        return False


    result2 = part2(4000000)
    # result2=None
    print("The result is for part 1 is:", result1)
    print("The result is for part 2 is:", result2)

    return result1, result2

def time():
    with open(os.devnull, 'w') as out:
        sys.stdout = out
        number = 20
        timing = timeit.timeit(solve, number=number) / number
        sys.stdout = sys.__stdout__
    print(f"This took {timing:.6f} seconds")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1][:4] == "time":
        del sys.argv[1]
        time()
    else:
        solve()
