with open(f"input.txt", "r") as fd:
    lines_ = fd.readlines()


def enhance(steps, image, algo):
    images = [[
        ''.join([
            algo[int(
                ''.join([
                    ('1' if algo[0] == '1' and step % 2 == 1 else '0') if
                    pos[0] < 0 or pos[1] < 0 or pos[0] >= len(images[-1][0]) or
                    pos[1] >= len(images[-1]) else images[-1][pos[1]][pos[0]]
                    for pos in ((x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                                (x - 1, y), (x, y), (x + 1, y), (x - 1, y + 1),
                                (x, y + 1), (x + 1, y + 1))
                ]), 2)] for x in range(-1,
                                       len(images[-1][0]) + 1)
        ]) for y in range(-1,
                          len(image) + 1)
    ] if step > 0 else image for step in range(steps)]
    return ''.join(images[-1]).count('1')


print(
    f"ANS for P1:",
    enhance(
        2, [l.strip().replace('.', '0').replace('#', '1') for l in lines_[2:]],
        lines_[0].strip().replace('.', '0').replace('#', '1')))
# print(
#     f"ANS for P2:",
#     enhance(
#         50,
#         [l.strip().replace('.', '0').replace('#', '1') for l in lines_[2:]],
#         lines_[0].strip().replace('.', '0').replace('#', '1')))
