import os, sys, timeit
from aochelper import get_data
from itertools import cycle

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')



    ##########
    # Part 1 #
    ##########

    class Rock():

        @classmethod
        def reset(cls):
            cls.situation = {}

            cls.highest = [0,0,0,0,0,0,0]

            cls.pattern = [0,0,0,0,0,0,0]

            cls.types = {
                'hor': [[True, True, True, True]],
                'plus': [[False,True,False],[True,True,True],[False,True,False]],
                'revl': [[True,True,True],[False,False,True],[False,False,True]],
                'ver': [[True],[True],[True],[True]],
                'block': [[True,True],[True,True]]
            }

            cls.next_type = cycle(cls.types.keys())

            cls.tallness = 0

        def __init__(self):
            self.type = next(Rock.next_type)
            self.left = 2
            self.width = len(Rock.types[self.type][0])
            self.height = len(Rock.types[self.type])
            self.bottom = Rock.tallness + 4
            self.top = self.bottom + self.height - 1
            self.right = self.left + self.width - 1

            self.stopped = False

        def move(self, hor=0, down=0):
            if self.bottom - down < 1:
                self.stopped = True
                down = min(down, self.bottom-1)
            if not self.stopped and down <= 1 and hor:
                # Determine move hor
                if self.left + hor < 0:
                    hor = 0
                if self.right + hor > 6:
                    hor = 0
                if hor:
                    for x in range(self.width):
                        for y in range(self.height):
                            if Rock.types[self.type][y][x] and \
                                Rock.situation.get((self.left + x + hor, self.bottom + y)) == '#':
                                hor = 0
                                break
                        if not hor:
                            break
            if down and not self.stopped:
                # Determine move down
                for x in range(self.width):
                    for y in range(self.height):
                        if Rock.types[self.type][y][x] and \
                            Rock.situation.get((self.left + x + hor, self.bottom + y - down)) == '#':
                            self.stopped = True
                            down -= 1
            if self.stopped:
                self.prevleft = self.left
                self.prevbottom = self.bottom
                self.left += hor
                self.right += hor
                self.bottom -= down
                self.top -= down
                Rock.tallness = max(Rock.tallness, self.top)
                self._update()
            else:
                if DEBUG:
                    self.prevleft = self.left
                    self.prevbottom = self.bottom
                self.left += hor
                self.right += hor
                self.top -= down
                self.bottom -= down
                if DEBUG:
                    self._update()


        def move_left(self):
            self.prevleft = self.left
            self.prevbottom = self.bottom
            can_move = self.left > 0
            for x in range(self.width):
                for y in range(self.height):
                    if Rock.types[self.type][y][x] and \
                        Rock.situation.get((self.left + x - 1, self.bottom + y)) == '#':
                            can_move = False
            if can_move:
                self.left -= 1
                self.right -= 1
            # self._update()

        def move_right(self):
            self.prevleft = self.left
            self.prevbottom = self.bottom
            can_move = self.right < 6
            for x in range(self.width):
                for y in range(self.height):
                    if Rock.types[self.type][y][x] and \
                        Rock.situation.get((self.left + x + 1, self.bottom + y)) == '#':
                        can_move = False
            if can_move:
                self.left += 1
                self.right += 1
            # self._update()

        def move_down(self):
            self.prevleft = self.left
            self.prevbottom = self.bottom
            if self.bottom > 1:
                for x in range(self.width):
                    for y in range(self.height):
                        if Rock.types[self.type][y][x] and \
                            Rock.situation.get((self.left + x, self.bottom + y - 1)) == '#':
                            self.stopped = True
            else:
                self.stopped = True
            if self.stopped:
                Rock.tallness = max(Rock.tallness, self.top)
                self._update()
            else:
                self.top -= 1
                self.bottom -= 1

        def _update(self):
            symb = '#' if self.stopped else '@'
            for y in range(self.height):
                for x in range(self.width):
                    if Rock.types[self.type][y][x]:
                        Rock.situation.pop((self.prevleft + x, self.prevbottom + y), None)
                for x in range(self.width):
                    if Rock.types[self.type][y][x]:
                        Rock.situation[(self.left + x, self.bottom + y)] = symb
                        if symb == '#':
                            Rock.highest[self.left + x] = max(Rock.highest[self.left + x], self.bottom + y)
                            base = min(Rock.highest)
                            for i, el in enumerate(Rock.highest):
                                Rock.pattern[i] = el - base
            if DEBUG:
                breakpoint()
            return

        @classmethod
        def fast_forward(cls, base=10, increase=20):
            # base = int(len(field) / 7)
            # for y in range(base):
            #     for x in range(7):
            #         Rock.situation[x,y+Rock.tallness-base+y] = field[x + y * 7]

            # for y in range(base):
            #     print()
            Rock.tallness += increase
            for x in range(7):
                for y in range(base):
                    old = Rock.situation.get((x, Rock.tallness - increase - y), None)
                    if old:
                        Rock.situation[(x, Rock.tallness - y)] = old
            # for _ in range(increase % len(Rock.types)):
            #     next(Rock.next_type)
            # for _ in range(increase % len(lines[0])):
            #     next(jet)

            # for y in range(base):
            #     print('\n', y, end=' >')
            #     for x in range(7):
            #         print(Rock.situation.get((x,y ),'.'), end='')


        @classmethod
        def show(cls):
            for y in range(cls.tallness + 4, 0, -1):
                for x in range(7):
                    print(cls.situation.get((x,y),'.'), end='')
                print('')
            print('')

        @classmethod
        def show_highest(cls, base=10):
            for y in range(base):
                print('\n', y, end=' >')
                for x in range(7):
                    print(Rock.situation.get((x,Rock.tallness - y),'.'), end='')


    increases = []

    def run(times):
        Rock.reset()
        jet = None
        jet = cycle([-1 if c == '<' else +1 for c in lines[0]])

        states = {}
        i = 0
        stage = 0
        ffd = False
        while i < times:

            # if not i % 100_000:
            if times > 5000:
                print(i, end='\r')
            rock = Rock()
            prev_tallness = Rock.tallness

            # breakpoint()
            hor = 0
            width = rock.width
            for _ in range(4):
                move = next(jet)
                stage = (stage + 1) % len(lines[0])
                if 2 + hor + move >= 0 and 2 + hor + move + width - 1 < 7:
                    hor += move
            rock.move(hor=hor, down=4)
            if DEBUG and times <= 4:
                rock.show()
            while not rock.stopped:
                # move = next(jet)
                rock.move(hor=next(jet), down=1)
                stage = (stage + 1) % len(lines[0])

                if DEBUG and times <= 4:
                    rock.show()
                # rock.move(down=1)
                # if DEBUG and times <= 4:
                #     rock.show()
            if DEBUG:
                rock.show()
            if i > 0:
                # if i > 500:
                #     increases.append(Rock.tallness - prev_tallness)
                field = ''.join(''.join(Rock.situation.get((x,y), ".") for x in range(7))
                                for y in range(Rock.tallness, Rock.tallness - 40, -1))
                current_rock = rock.type
                # state = (tuple(Rock.pattern), current_rock, stage)
                state = (field, current_rock, stage)
                # breakpoint()

                prev_i, prev_height, prev_stage = states.get(state, (None, None, None))
                # breakpoint()
                # if incr_i:
                #     breakpoint()
                #     print(i)
                #     continue

                if not ffd and prev_i:
                    breakpoint()
                    ffd = True
                    incr_i_one = i - prev_i
                    incr_i = incr_i_one * ((times - i) // incr_i_one)
                    incr_height = (Rock.tallness - prev_height) * ((times - i) // incr_i_one)
                    incr_stage = stage - prev_stage
                    # Rock.tallness += incr_height
                    # states[state] = Rock.tallness
                    i += incr_i
                    # print(Rock.pattern)
                    Rock.fast_forward(40, incr_height)
                    for _ in range(incr_i % len(Rock.types)):
                        next(Rock.next_type)
                    for _ in range(incr_stage % len(lines[0])):
                        next(jet)

                    # print(Rock.highest)
                    # states[state] = (i, Rock.tallness, i - prev_i, Rock.tallness - prev_height)
                else:
                    states[state] = (i, Rock.tallness, stage)

            # if i > 1970:
            #     print(i, Rock.tallness)
            i += 1


        return Rock.tallness

    DEBUG = False

    result1 = None
    result1 = run(2022)

    ##########
    # Part 2 #
    ##########




    result2 = None
    result2 = run(1_000_000_000_000)

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
