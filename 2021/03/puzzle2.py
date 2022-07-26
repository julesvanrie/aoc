with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

length = len(lines[0])

def most_freq(l, most = True):
    result = []
    nb_lines = len(l)
    for pos in range(length):
        most_freq = sum([int(line[pos]) for line in l]) >= nb_lines / 2
        if most:
            result.append(most_freq)
        else:
            result.append(not(most_freq))
    return result

def calc_rate(l, most = True):
    selection = lines
    for pos in range(length):
        filter = most_freq(selection, most=most)[pos]
        selection = [line for line in selection if (line[pos] == '1') == filter]
        if len(selection) == 1:
            break
    return int('0b' + selection[0], 2)


oxygen = calc_rate(lines, most=True)
co2 = calc_rate(lines, most=False)

result = oxygen * co2
print(f"Result is {result}")
