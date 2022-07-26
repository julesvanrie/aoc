with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

start_one = int(lines[0].split(': ')[1])
start_two = int(lines[1].split(': ')[1])

class Player:
    die_count = 0
    die_result = 0

    def __init__(self, start):
        self.pos = start
        self.score = 0
        self.win = False

    def play(self):
        for i in range(3):
            self.pos += self.die()
            self.pos = (self.pos - 1) % 10 + 1
        self.score += self.pos
        if self.score >= 1000:
            self.win = True

    @classmethod
    def die(cls):
        cls.die_count += 1
        cls.die_result = cls.die_result % 100 + 1
        return cls.die_result


player_one = Player(start_one)
player_two = Player(start_two)

while True:
    player_one.play()
    if player_one.win:
        result = player_two.score * Player.die_count
        break
    player_two.play()
    if player_two.win:
        result = player_one.score * Player.die_count
        break

print(f"Result for part 1 is {result}")
