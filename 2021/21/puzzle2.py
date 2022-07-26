with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

start_one = int(lines[0].split(': ')[1])
start_two = int(lines[1].split(': ')[1])

die_ranges = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}

def play(player, pos_one, pos_two, score_one, score_two):
    next_player = (player + 1) % 2
    local_wins = [0,0]
    for throw, counts in die_ranges.items():
        pos_one_new = pos_one
        pos_two_new = pos_two
        score_one_new = score_one
        score_two_new = score_two
        if player == 0:
            pos_one_new = (pos_one_new + throw - 1) % 10 + 1
            score_one_new += pos_one_new
            if score_one_new >= 21:
                local_wins[0] += counts
                continue
        if player == 1:
            pos_two_new = (pos_two_new + throw - 1) % 10 + 1
            score_two_new += pos_two_new
            if score_two_new >= 21:
                local_wins[1] += counts
                continue
        tmp = play(next_player, pos_one_new, pos_two_new, score_one_new,
             score_two_new)
        local_wins[0] += tmp[0] * counts
        local_wins[1] += tmp[1] * counts
    return local_wins

wins = play(0, start_one, start_two, 0, 0)

result = max(wins)

print(f"Result for part 2 is {result}")
