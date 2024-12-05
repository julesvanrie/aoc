import sys
from aocsolution.basesolution import BaseSolution

@BaseSolution.time_this
def solve_one(self):
    self.prep_data()
    correct_updates = [upd
                       for upd in self.updates
                       if self.is_valid(upd)]
    return self.calc_middles(correct_updates)

@BaseSolution.time_this
def solve_two(self):
    self.prep_data()
    incorrect_updates = [self.correct_update(upd)
                         for upd in self.updates
                         if not self.is_valid(upd)]
    return calc_middles(self, incorrect_updates)

def prep_data(self):
    input = ''.join(self.get_data(split=False))
    rules, updates = input.split('\n\n')
    rules = rules.split('\n')
    self.rules = [[int(el) for el in rule.split('|')] for rule in rules]
    self.updates = updates.split('\n')

def is_valid(self, update):
    page_pos = {int(page): ix for ix, page
                in enumerate(update.split(','))}
    for left, right in self.rules:
        if ((l_pos := page_pos.get(left)) is not None
        and (r_pos := page_pos.get(right)) is not None
        and l_pos > r_pos):
                return False
    return True

def calc_middles(self, updates):
    result = 0
    for update in updates:
        pages = update.split(',')
        middle_pos = int((len(pages)-1)/2)
        result += int(pages[middle_pos])
    return result

def correct_update(self, update):
    if self.is_valid(update):
        return update
    page_pos = {int(page): ix for ix, page
                in enumerate(update.split(','))}
    for left, right in self.rules:
        if ((l_pos := page_pos.get(left)) is not None
        and (r_pos := page_pos.get(right)) is not None
        and l_pos > r_pos):
            page_pos[left] = r_pos
            page_pos[right] = l_pos
            switched = sorted(page_pos, key=lambda item: page_pos[item])
            switched_str = ','.join(str(p) for p in switched)
            return self.correct_update(switched_str)

class Solution(BaseSolution):
    solve_one = solve_one
    solve_two = solve_two
    is_valid = is_valid
    calc_middles = calc_middles
    correct_update = correct_update
    prep_data = prep_data

if __name__ == "__main__":
    test = len(sys.argv) > 1 and 'test' in sys.argv[1]
    timing = len(sys.argv) > 1 and 'time' in sys.argv[1]
    solution = Solution(test=test)
    print("The result for part 1 is:", solution.solve_one())
    print("The result for part 2 is:", solution.solve_two())
