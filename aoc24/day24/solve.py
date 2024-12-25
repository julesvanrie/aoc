import sys
from aocsolution.basesolution import BaseSolution

from pprint import pprint


@BaseSolution.time_this
def solve_one(self):
    self.input = self.get_data(split=False)

    # Parse the x and y inputs into a wires dict of bools
    self.wires = {row.split(': ')[0]: bool(int(row.split(': ')[1]))
             for row in self.input.split('\n\n')[0].split('\n')}

    # Parse the calculations into a calcs dict of left, operator, right
    self.calcs = {row.split(' -> ')[1]: row.split(' -> ')[0]
             for row in self.input.split('\n\n')[1].split('\n')}
    self.calcs = {wire: calc.split(' ')
                  for wire, calc in self.calcs.items()}

    # Print some output, used for part 2
    xplusy = self.wires_to_number('x') + self.wires_to_number('y')
    print('x   ', bin(self.wires_to_number('x')))
    print('y   ', bin(self.wires_to_number('y')))
    print('x+y',bin(xplusy))
    print('z  ', bin(self.calc_z()))
    print('xor', bin(self.calc_z() ^ xplusy))

    # Return the value of z
    return self.calc_z()


def calc_z(self):
    """Calculates all the wires and returns the value of z
    """
    # Calculate all the wires, giving bool or false
    for wire, (lef, op, rig) in self.calcs.items():
        if wire not in self.wires:
            self.wires[wire] = self.calc(lef, op, rig)

    # Read the wires and calculate the result
    return wires_to_number(self, 'z')


def calc(self, lef, op, rig):
    """Recursively calculate the value of a wire.
    If the one of the input wires isn't know yet, call calc recursively.
    """
    wires = self.wires
    calcs = self.calcs
    # One of the inputs not yet calculated, so calculate them
    if lef not in wires:
        wires[lef] = self.calc(*calcs[lef])
    if rig not in wires:
        wires[rig] = self.calc(*calcs[rig])
    # Now calculate the wire
    if op == 'AND':
        return wires[lef] & wires[rig]
    elif op == 'OR':
        return wires[lef] | wires[rig]
    elif op == 'XOR':
        return wires[lef] ^ wires[rig]


def wires_to_number(self, xyz):
    """Converts the wires to a number, starting with the given wire.
    Saves the number of digits in self.nb_digits
    """
    # Start with 0 as binary
    result = 0b0
    i = 0
    # Add bit by bit (pun intended)
    while True:
        if (key := f"{xyz}{i:02d}") in self.wires:
            result += self.wires[key] * 2**i
            i += 1
        else:
            # We're finished, let's store the number of digits for info
            self.nb_digits = i
            break
    return result


@BaseSolution.time_this
def solve_two(self):
    # We disregard the inputs for x and y, because they have no impact for what we do here
    lines = self.get_data(split=False).split('\n\n')[1].split('\n')

    # Then sort the lines by the output wire, so we can see the dependencies
    # First 132 lines are calculations using the x and y inputs as input
    # The other lines are intermediate results, like carrying 1 over if 1+1
    sorted_lines = sorted(lines)
    inputs = sorted(sorted_lines[132:], key=lambda x: x[1:]).copy()
    outputs = sorted(sorted_lines[:132], key=lambda x: x[-3:]).copy()

    # In the next step, we'll rename the random wires into numbered wires.
    # This way we can easily track what happens.

    # This dictionary saves the translation from the numbered wires to the actual wire
    translate = {}

    # Start with the inputs and translate the AND results into c01, c02, etc. (c for carry)
    # Also translate the XOR results into d01, d02, etc. (d for digit)
    # At the same time, replace the wire names in the outputs with the new names
    for i, inp in enumerate(inputs):
        calc, wire = inp.split(' -> ')
        if wire[0] not in 'xyz':
            nb = calc[1:3]
            if calc.find('AND') != -1:
                translate['c' + nb] = wire
                inputs[i] = inp.replace(wire, 'c' + nb)
                for j, out in enumerate(outputs):
                    outputs[j] = out.replace(wire, 'c' + nb)
            elif calc.find('XOR') != -1:
                translate['d' + nb] = wire
                inputs[i] = inp.replace(wire, 'd' + nb)
                for j, out in enumerate(outputs):
                    outputs[j] = out.replace(wire, 'd' + nb)

    # Now we do the same for the outputs
    # Translating the AND results into a01, a02, etc. (a for and)
    # Translating the OR results into o01, o02, etc. (o for or)
    # Translating the XOR results into c01, c02, etc. (c for carry)
    for i, outp in enumerate(outputs):
        calc, wire = outp.split(' -> ')
        if wire[0] not in 'xyz':
            if calc[1].isdigit():
                nb = calc[1:3]
                repl = calc[-3:]
            elif calc[-1].isdigit():
                nb = calc[-2:]
                repl = calc[:3]
            if calc.find('AND') != -1:
                translate['a' + nb] = repl
                for j, out in enumerate(outputs):
                    outputs[j] = out.replace(repl, 'a' + nb)
            elif calc.find(' OR') != -1:
                translate['o' + nb] = repl
                for j, out in enumerate(outputs):
                    outputs[j] = out.replace(repl, 'o' + nb)
            if calc.find('XOR') != -1:
                translate['c' + nb] = repl
                for j, out in enumerate(outputs):
                    outputs[j] = out.replace(repl, 'c' + nb)

    # Now we can print the inputs and outputs
    print('\n'.join(inputs))
    print()
    for out in sorted(outputs, key=lambda x: x[-3:]):
        print(out, translate.get(out[-3:]) if out[-3] != 'z' else '')

    # Next up: manual inspection of the printed lines
    # Spot any anomalies
    # Three cases are obvious from the printout: the result wires are mixed up
    # One case is more difficult to spot: the c and d wires are mixed
    # Write out the mixed up wires, sort them manually and put it all together

class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two
    calc = calc
    calc_z = calc_z
    wires_to_number = wires_to_number


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
