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
        '''Calculate manhattan distance between sensor and beacon'''
        return abs(s[0] - b[0]) + abs(s[1] - b[1])


    def cov_row(sensor, man, row):
        '''Calculates part of a row covered by a sensor at location 'sensor' and
        with manhattan distance 'man'.
        Returns: tuple of coordinates.'''
        if man <= 0:
            return None
        ver = abs(sensor[1] - row)
        if ver > man:
            return None
        hor = max(man - ver, 0)
        return (sensor[0] - hor, sensor[0] + hor)


    def total_cov_row(row):
        '''Calculates all parts of a row that are covered.
        Returns: list of tuples of coordinates.'''
        cov = []
        for s, b in zip(sensors, beacons):
            cov_r = cov_row(s, man(s, b), row)
            if cov_r:
                cov.append(cov_r)
        return cov


    ##########
    # Part 1 #
    ##########

    def xminmax(row):
        '''Calculates first and last coordinate of a row that is covered.'''
        cov = total_cov_row(row)
        xmin = 2*62
        xmax = -2*62
        for c in cov:
            xmin = min(xmin, c[0])
            xmax = max(xmax, c[1])
        return xmin-1, xmax+1


    def print_row(row, minx=-5, maxx=26):
        '''Prints out a row like in the challenge instructions.'''
        cov = total_cov_row(row)
        for x in range(minx, maxx):
            done = False
            for b in beacons:
                if b[1] == row and x == b[0]:
                    print('B', end='')
                    done = True
                    break
            if done:
                continue
            for s in sensors:
                if s[1] == row and x == s[0]:
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


    def part1(row):
        '''Calculates number of positions that cannot contain a beacon'''
        total = 0
        cov = total_cov_row(row)
        for x in range(*xminmax(row)):
            for c in cov:
                if x >= c[0] and x <= c[1]:
                    total += 1
                    break
            # Case where there is already a beacon
            for b in beacons:
                if b[1] == row and x == b[0]:
                    total -= 1
                    break
        return total

    result1 = part1(2000000)


    ##########
    # Part 2 #
    ##########

    def cut(start, c):
        '''Cuts range c out of range start.
        Returns list with slices (can contain 0, 1 or 2 slices).'''
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


    def check_range(start=(0,20), cov=[]):
        '''Takes a start range, and a list of pieces to cut out of the range.
        Cuts out the first range, and if any slices remain after that operation,
        calls itself to recursively cut the resulting slice(s).
        If no slices remaining, returns empty set.
        Otherwise returs set with remaining slices.'''
        if len(cov) == 0:
            return {start}
        ranges = set()
        slices = cut(start, cov[0])
        if not slices:
            return {}
        for slice in slices:
            for t in check_range(slice, cov[1:]):
                ranges.add(t)
        return ranges


    def part2(area):
        '''Run check_range iteratively over all rows.
        If a row contains one remaining slice with equal first and last
        coordinate, calculates the tuning frequency.'''
        for r in range(area+1):
            # if not (r % 1000):
            #     print(r, end='\r')
            ch = list(check_range(start=(0,area), cov=total_cov_row(r)))
            if len(ch) == 1 and ch[0][0] == ch[0][1]:
                return ch[0][0] * area + r
        return False


    result2 = part2(4000000)

    print("The result is for part 1 is:", result1)
    print("The result is for part 2 is:", result2)

    return result1, result2


def time():
    with open(os.devnull, 'w') as out:
        sys.stdout = out
        number = 1
        timing = timeit.timeit(solve, number=number) / number
        sys.stdout = sys.__stdout__
    print(f"This took {timing:.6f} seconds")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1][:4] == "time":
        del sys.argv[1]
        time()
    else:
        solve()
