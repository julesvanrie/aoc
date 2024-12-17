import sys
from aocsolution.basesolution import BaseSolution


@BaseSolution.time_this
def solve_one(self):
    line_A, line_B, line_C, _, line_P = self.get_data()

    A = int(line_A.split(": ")[1])
    B = int(line_B.split(": ")[1])
    C = int(line_C.split(": ")[1])
    P = [int(p) for p in line_P.split(": ")[1].split(",")]
    return solve(A, B, C, P)


def solve(A, B, C, P):
    pos = 0
    result = []

    while pos < len(P):
        op = P[pos]
        r = P[pos + 1]
        c = A if r == 4 else B if r == 5 else C if r == 6 else r
        if op == 0:
            A //= (2**c)
        elif op == 1:
            B ^= r
        elif op == 2:
            B = c % 8
        elif op == 3 and A:
            pos = r - 2
        elif op == 4:
            B ^= C
        elif op == 5:
            result.append(c % 8)
        elif op == 6:
            B = A // (2**c)
        elif op == 7:
            C = A // (2**c)
        pos += 2

    return ','.join(str(r) for r in result)


@BaseSolution.time_this
def solve_two(self):
    _, line_B, line_C, _, line_P = self.get_data()

    B = int(line_B.split(": ")[1])
    C = int(line_C.split(": ")[1])
    P_text = line_P.split(": ")[1]
    P = [int(p) for p in P_text.split(",")]

    candidates = [0]

    for i in range(0,16):
        new_candidates = []
        for cand in candidates:
            for A in range(8):
                new_A = cand * 8 + A
                new_P = solve(new_A, B, C, P)
                if new_P == P_text[-2*i-1:]:
                    new_candidates.append(new_A)
                    # print(oct(new_A))
                    if i == 15:
                        return new_A
        candidates = new_candidates


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
