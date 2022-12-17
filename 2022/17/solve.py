import os, sys, timeit
from aochelper import get_data
from itertools import cycle

def solve(lines=None):
    # with open("input.txt") as fo:
    #     lines = fo.read().strip('\n').split('\n')
    text = lines if lines else get_data(sys.argv)
    lines = text.split('\n')

    jet = cycle(lines[0])


    ##########
    # Part 1 #
    ##########

    class Rock():

        situation = {}

        types = {
            'hor': [[True, True, True, True]],
            'plus': [[False,True,False],[True,True,True],[False,True,False]],
            'revl': [[True,True,True],[False,False,True],[False,False,True]],
            'ver': [[True],[True],[True],[True]],
            'block': [[True,True],[True,True]]
        }

        next_type = cycle(types.keys())

        tallness = 0

        def __init__(self):
            self.type = next(self.next_type)
            self.left = 2
            self.width = len(Rock.types[self.type][0])
            self.height = len(Rock.types[self.type])
            self.bottom = Rock.tallness + 4
            self.top = self.bottom + self.height - 1
            self.right = self.left + self.width - 1

            self.stopped = False

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
            rock._update()

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
            rock._update()

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
            else:
                self.top -= 1
                self.bottom -= 1
            rock._update()

        def _update(self):
            symb = '#' if self.stopped else '@'
            for y in range(self.height):
                for x in range(self.width):
                    if Rock.types[self.type][y][x]:
                        Rock.situation.pop((self.prevleft + x, self.prevbottom + y), None)
                for x in range(self.width):
                    if Rock.types[self.type][y][x]:
                        Rock.situation[(self.left + x, self.bottom + y)] = symb
            return

        @classmethod
        def show(cls):
            for y in range(cls.tallness, 0, -1):
                for x in range(7):
                    print(cls.situation.get((x,y),'.'), end='')
                print('')
            print('')

    height = 0
    for _ in range(2022):
        rock = Rock()
        while not rock.stopped:
            move = next(jet)
            if move == '<':
                rock.move_left()
            else:
                rock.move_right()
            rock.move_down()
        # rock.show()


    result1 = Rock.tallness

    ##########
    # Part 2 #
    ##########



    result2 = None

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
