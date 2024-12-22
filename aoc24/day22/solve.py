import sys
from aocsolution.basesolution import BaseSolution

from collections import defaultdict

@BaseSolution.time_this
def solve_one(self):
    input = self.get_data()
    buyers = [int(row) for row in input]

    result = 0
    for buyer in buyers:
        secret = buyer
        for _ in range(2000):
            secret = gen_secret(secret)
        result += secret

    return result


def gen_secret(secret):
    secret ^= secret * 64
    secret %= 16777216
    secret ^= secret // 32
    secret %= 16777216
    secret ^= secret * 2048
    secret %= 16777216
    return secret


@BaseSolution.time_this
def solve_two_unoptimized(self):
    input = self.get_data()

    buyers = [int(row) for row in input]

    sequences = [[] for _ in range(len(buyers))]
    for ix, buyer in enumerate(buyers):
        sequences[ix] = {}
        secret = buyer
        changes = [0 for _ in range(2000)]
        for i in range(2000):
            new_secret = gen_secret(secret)
            changes[i] = new_secret % 10 - secret % 10
            if i >= 3:
                seq = tuple(changes[i-3:i+1])
                if seq not in sequences[ix]:
                    sequences[ix][seq] = new_secret % 10
            secret = new_secret

    all_seq = set()
    for ix in range(len(sequences)):
        all_seq |= sequences[ix].keys()

    largest = 0
    for seq in all_seq:
        if (new_largest := sum(
                sequences[ix].get(seq, 0)
                for ix in range(len(sequences))
                )) > largest:
            largest = new_largest

    return largest

@BaseSolution.time_this
def solve_two(self):
    input = self.get_data()

    buyers = [int(row) for row in input]

    results = defaultdict(int)

    for buyer in buyers:
        secret = buyer
        changes = [0 for _ in range(2000)]
        covered = set()
        for i in range(2000):
            new_secret = gen_secret(secret)
            changes[i] = new_secret % 10 - secret % 10
            if i >= 3:
                seq = tuple(changes[i-3:i+1])
                if seq not in covered:
                    results[seq] += new_secret % 10
                    covered.add(seq)
            secret = new_secret

    return max(results.values())


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
