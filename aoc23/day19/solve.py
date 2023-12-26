import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint


def parse(instructions):
    steps = [(attr, int.__lt__ if op == "<" else int.__gt__, int(val), dest)
                for attr, op, val, dest in re.findall(r"([a-z]+)([><])(\d+):([a-zA-Z]+)", instructions)]
        # op = int.__lt__ if op == "<" else int.__gt__
        # steps.append(attr, op, val, dest)
    steps.append( [instructions.split(',')[-1]] )
    return steps


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data(split=False)
    instructions, parts = input.split('\n\n')

    instructions = {r.split('{')[0]: parse(r.split('{')[1].strip('}'))
                    for r in instructions.strip().split('\n')}

    parts = [{k: int(v) for k, v in re.findall(r"([a-z]+)\=(\d+)", part)}
             for part in parts.split('\n')]

    result = 0
    for part in parts:
        # print(part)
        new_loc = 'in'
        while new_loc not in  ['A','R']:
            for ins in instructions[new_loc]:
                # print(new_loc, ins)
                if len(ins) == 1:
                    new_loc = ins[0]
                    if new_loc == 'A':
                        result += sum(part.values())
                else:
                    attr, op, val, dest = ins
                    if op(part[attr], val):
                        new_loc = dest
                        if new_loc == 'A':
                            result += sum(part.values())
                        break

    return result


@BaseSolution.time_this
def solve_twos(self):
    input = self.get_data(split=False)
    instructions, parts = input.split('\n\n')

    instructions = {r.split('{')[0]: r.split('{')[1].strip('}')
                    for r in instructions.strip().split('\n')}

    prev_len_global = 1
    while len(instructions) != prev_len_global:
        prev_len_global = len(instructions)

        prev_len = 1
        while prev_len:
            straightAs = {k: ins for k, ins in instructions.items() if ins.endswith('A,A')}
            straightRs = {k: ins for k, ins in instructions.items() if ins.endswith('R,R')}

            for k, ins in straightAs.items():
                instructions[k] = re.sub(r"[a-z]+[<>]\d+:A,A", 'A', ins)
            for k, ins in straightRs.items():
                instructions[k] = re.sub(r"[a-z]+[<>]\d+:R,R", 'R', ins)

            prev_len = len(straightAs) + len(straightRs)

        prev_len = 0
        while len(instructions) != prev_len:
            prev_len = len(instructions)
            straights = [k for k, ins in instructions.items() if ins.count(',') == 0] #1 and ins.endswith('A,A')]

            for old in straights:
                instructions = {k: re.sub(f",{old}$", f',{instructions[old]}', ins) for k, ins in instructions.items()}
                instructions = {k: re.sub(f":{old},", f':{instructions[old]},', ins) for k, ins in instructions.items()}
                del instructions[old]

    if True:
        prev_len = 0
        notAorBs = True
        while notAorBs:
            prev_len = len(instructions)
            notAorBs = {k: ins for k, ins in instructions.items()
                        if (not ins.endswith(',A')) and (not ins.endswith(',R'))}


            for old, oldins in notAorBs.items():
                end = oldins.rsplit(',', 1)[-1]
                if (instructions[end].endswith(',R')
                    or instructions[end].endswith(',A')
                ):
                    instructions[old] = oldins.replace(','+end, ','+instructions[end])
                    del instructions[end]

    result = 0

    return result


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data(split=False)
    instructions, parts = input.split('\n\n')

    instructions = {r.split('{')[0]: r.split('{')[1].strip('}')
                    for r in instructions.strip().split('\n')}

    pprint(instructions)
    print(len(instructions))

    prev_len_global = 0
    while len(instructions) != prev_len_global:
        prev_len_global = len(instructions)

        prev_len = 0
        while len(instructions) != prev_len:
            prev_len = len(instructions)
            straightAs = {k: ins for k, ins in instructions.items() if ins.endswith('A,A')}
            straightRs = {k: ins for k, ins in instructions.items() if ins.endswith('R,R')}

            for k, ins in straightAs.items():
                instructions[k] = re.sub(r"[a-z]+[<>]\d+:A,A$", 'A', ins)
            for k, ins in straightRs.items():
                instructions[k] = re.sub(r"[a-z]+[<>]\d+:R,R$", 'R', ins)

            singulars = {k: ins
                         for k, ins in instructions.items()
                         if not ins.count(',')}

            print('singulars')
            pprint(singulars)

            for s, sing in singulars.items():
                for k, ins in instructions.items():
                    instructions[k] = re.sub(f":{s},", f":{sing},", ins)
                    ins = instructions[k]
                    instructions[k] = re.sub(f",{s}$", f",{sing}", ins)
                del instructions[s]

        print("Removed singulars")
        pprint(instructions)

        AorBs = {k: ins for k, ins in instructions.items()
                    if ins.endswith(',A') or ins.endswith(',R')}
        for k, ins in AorBs.items():
            for key, instruction in instructions.items():
                if instruction.endswith(f",{k}"):
                    instructions[key] =  re.sub(f",{k}$", ','+ins, instruction)

        pprint(instructions)
        pprint(len(instructions))

    print("finally")
    pprint(instructions)


class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
