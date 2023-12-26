import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    h = len(input)

    hail = [r.split(' @ ') for r in input]
    hail = [(tuple(map(int, loc.split(', '))),
             tuple(map(int, v.split(', '))))
            for (loc, v) in hail]

    # pprint(hail)
    minxy = 7 if h < 10 else 200000000000000
    maxxy = 27 if h < 10 else 400000000000000

    result = 0

    for i in range(h):
        for j in range(i+1,h):
            (xa, ya, za), (vxa, vya, vza) = hail[i]
            (xb, yb, zb), (vxb, vyb, vzb) = hail[j]


            if vxa / vya != vxb / vyb and vxa / vya != - vxb / vyb:
                # x = xa + t*vxa
                # t = (x-xa) / vxa
                # y = ya + t*vya
                # y = ya + (x-xa)*vya/vxa
                # y = (ya - xa*vya/vxa) + x * (vya/vxa)
                # y = ia + sa*x
                # with:
                ia = ya-xa*vya/vxa
                sa = vya/vxa
                # Same for b
                ib = yb-xb*vyb/vxb
                sb = vyb/vxb

                # y = y
                # ia + sa*x = ib + sb*x
                x = (ib-ia) / (sa-sb)
                y = ia + sa*x
                ta = (x-xa) / vxa
                tb = (x-xb) / vxb

                if ta > 0 and tb > 0:
                    if minxy < x < maxxy and minxy < y < maxxy:
                        result += 1
            #             print(x, y, ta, tb)
            #         else:
            #             print("outside")
            #     else:
            #         print("past")
            # else:
            #     print("parallel")

    return result


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()[:7]
    h = len(input)

    hail = [r.split(' @ ') for r in input]
    hail = [(tuple(map(int, loc.split(', '))),
             tuple(map(int, v.split(', '))))
            for (loc, v) in hail]

    # pprint(hail)
    minxy = 7 if h < 10 else 200000000000000
    maxxy = 27 if h < 10 else 400000000000000

    result = 0

    dt = 0
    goal = False
    while not goal:
    # if True:
        dt += 1
        print(dt)
        # if dt == 2: breakpoint()
        for i in range(h):
            (xa, ya, za), (vxa, vya, vza) = hail[i]
            xs, ys, zs = (xa+vxa, ya+vya, za+vza)
            for j in range(h):
                # if dt == 2 and i == 4 and j == 1: breakpoint()
                if i == j:
                    continue
                (xb, yb, zb), (vxb, vyb, vzb) = hail[j]
                dxs = xb+vxb*(dt+1) - xs
                dys = yb+vyb*(dt+1) - ys
                dzs = zb+vzb*(dt+1) - zs
                if dxs % dt or dys % dt or dzs % 1:
                    continue
                vxs, vys, vzs = (dxs / dt, dys / dt, dzs / dt)
                goal = True
                for k in range(h):
                    print(dt, i, j, k, end='\r')
                    if k in [i,j]:
                        continue
                    (xc, yc, zc), (vxc, vyc, vzc) = hail[k]
                    # xs + tx*vxs = xc + tx*vxc
                    if (vxs == vxc #and xs != xc
                        or vys == vyc #and ys != yc
                        or vzs == vzc #and zs != zc
                        ):
                        goal = False
                        break
                    xss, yss, zss = (xs-vxs, ys-vys, zs-vzs)
                    tx = (xc-xss) / (vxs - vxc)
                    ty = (yc-yss) / (vys - vyc)
                    tz = (zc-zss) / (vzs - vzc)
                    if (tx % 1 or ty % 1 or tz % 1
                        or tx != ty or ty != tz):
                        goal = False
                        break
                if goal:
                    break
            # if goal:
            #     break
        if goal:
            break

    # print(goal)
    rxs, rys, rzs = (xs-vxs, ys-vys, zs-vzs)

    return rxs + rys + rzs



    #         # xa + vxa*t = xb + vbx*t
    #         # ya + vya*t = yb + vby*t
    #         # za + vza*t = zb + vbz*t
    #         if vxa == vxb or vya == vyb or vza == vzb:
    #             print(i, j, "won't cross")
    #             continue

    #         t1 = (xb-xa) / (vxa-vxb)
    #         t2 = (yb-ya) / (vya-vyb)
    #         t3 = (zb-za) / (vza-vzb)

    #         if t1 == t2 and t2 == t3:
    #             print("hallelujah")


    #         # ia = ya-xa*vya/vxa
    #         # sa = vya/vxa
    #         # ib = yb-xb*vyb/vxb
    #         # sb = vyb/vxb
    #         # x = (ib-ia) / (sa-sb)
    #         # y = ia + sa*x
    #         # ta = (x-xa) / vxa
    #         # tb = (x-xb) / vxb

    #         # # print(t, x, y)

    #         # if ta > 0 and tb > 0:
    #         #     if minxy < x < maxxy and minxy < y < maxxy:
    #         #         result += 1
    #     #             print(x, y, ta, tb)
    #     #         else:
    #     #             print("outside")
    #     #     else:
    #     #         print("past")
    #     # else:
    #     #     print("parallel")

    # return result


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
