with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

lines = [line.split('-') for line in lines]
reverse = [[line[1], line[0]] for line in lines]
lines.extend(reverse)

connections = {}
for con in lines:
    if con[0] != 'end' and con[1] != 'start':
        connections[con[0]] = connections.get(con[0], []) + [con[1]]

paths = []

from copy import deepcopy

def find_path(path):
    new_path = deepcopy(path)
    for con in connections[new_path[-1]]:
        if con == 'end':
            paths.append(new_path + [con])
            continue
        elif con.islower() and con in new_path:
            continue
        else:
            find_path(new_path + [con])

find_path(['start'])

result = len(paths)

print(f"Number of paths is {result}")
