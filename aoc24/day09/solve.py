import sys
from aocsolution.basesolution import BaseSolution

import re
from copy import deepcopy
from pprint import pprint


@BaseSolution.time_this
def solve_one(self):
    input = self.get_data(split=False)
    result = 0

    position = 0
    fill_id = (len(input) - 1) // 2
    fill_left = int(input[fill_id * 2])

    for id in range(len(input) // 2):
        # Count the blocks that are left for the case of the last file we will only move partly
        blocks_left = int(input[id * 2])
        if id == fill_id:
            blocks_left = fill_left
        # We encounter a file, so we calculate the checksum
        for block in range(blocks_left):
            result += (position + block) * id
        # If we are done
        if id >= fill_id:
            break
        position += int(input[id * 2])
        # We encounter some free space, so move the last block in here
        for block in range(int(input[id * 2 + 1])):
            if not fill_left:
                fill_id -= 1
                fill_left = int(input[fill_id * 2])
                if fill_id <= id:
                    break
            # And calculate the checksum
            result += (position + block) * fill_id
            fill_left -= 1
        position += int(input[id * 2 + 1])

    return result


@BaseSolution.time_this
def solve_two(self):
    input = self.get_data(split=False)
    blocks = [int(c) for c in input]
    result = 0
    nb_files = len(input) // 2 + 1

    # First, we need to calculate the position of each block
    positions = [0 for _ in range(nb_files)]
    for id, size in enumerate(blocks[::2]):
        positions[id] = sum(blocks[:id*2])

    # Then, we need to calculate the empty spaces' position and size
    empties = [(0,0) for _ in range(nb_files - 1)]
    for ix, size in enumerate(blocks[1::2]):
        empties[ix] = (sum(blocks[:ix*2+1]), size)


    # Now, we can start moving the blocks one by one, starting from the end
    for id, size in zip(range(nb_files-1, -1, -1), blocks[-1:0:-2]):
        # Check the empty spaces one by one
        for ix, (empty_pos, empty_size) in enumerate(empties):
            # If large enough, and to the left of the block, we can move it
            if empty_size >= size and empty_pos < positions[id]:
                positions[id] = empty_pos
                # Update the empty blocks
                if empty_size == size:
                    del empties[ix]
                else:
                    empties[ix] = (empty_pos + size, empty_size - size)
                break

    # Finally, calculate the checksum
    for id, pos in enumerate(positions):
        for i in range(blocks[id*2]):
            result += (pos + i) * id

    return result

class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two


if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
