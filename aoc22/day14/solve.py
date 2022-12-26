import os, sys, timeit
from aochelper import get_data

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')

    paths = [line.split(' -> ') for line in lines]

    def initiate_chart():
        chart = {}
        minx = 500; maxx = maxy = -500

        for path in paths:
            for i in range(len(path)-1):
                xl, yl = path[i].split(',')
                xr, yr = path[i+1].split(',')
                xl = int(xl); yl = int(yl); xr = int(xr); yr = int(yr)
                maxx = max(max(xl, xr), maxx)
                minx = min(min(xl, xr), minx)
                maxy = max(max(yl, yr), maxy)
                miny = 0
                if yl == yr:
                    (xl, xr) = (xl, xr) if xl <= xr else (xr, xl)
                    for x in range(xl,xr+1):
                        chart[(x, yl)] = '#'
                if xl == xr:
                    (yl, yr) = (yl, yr) if yl <= yr else (yr, yl)
                    for y in range(yl, yr+1):
                        chart[(xl, y)] = '#'
        return chart, minx, maxx, miny, maxy


    def expand_chart(chart, minx, maxx, miny, maxy):
        maxy += 2; minx -= 150; maxx += 200
        for x in range(minx, maxx):
            chart[(x, maxy)] = '#'
        return chart, minx, maxx, miny, maxy


    def traverse(chart, minx, maxx, miny, maxy):
        i = 0
        while True:
            x = 500; y = 0
            while True:
                if y > maxy + 1:
                    return i, chart, minx, maxx, miny, maxy
                if not chart.get((x, y+1)):
                    y += 1; continue
                if not chart.get((x-1, y+1)):
                    y += 1; x -= 1; continue
                if not chart.get((x+1, y+1)):
                    y += 1; x += 1; continue
                chart[(x, y)] = 'o'
                if y == 0:
                    i += 1
                    return i, chart, minx, maxx, miny, maxy
                break
            i += 1


    def show(chart, minx, maxx, miny, maxy):
        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                print(chart.get((x,y), '.'), end='')
            print('')


    # Part 1
    *chart_stuff, = initiate_chart()
    result1, *chart_stuff = traverse(*chart_stuff)
    # show(*chart_stuff)


    # Part 2
    *chart_stuff, = initiate_chart()
    *chart_stuff, = expand_chart(*chart_stuff)
    result2, *chart_stuff = traverse(*chart_stuff)
    # show(*chart_stuff)

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
