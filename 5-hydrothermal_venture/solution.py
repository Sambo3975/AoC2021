import re

from magic_matrix import MagicMatrix


def filter_line(line):
    return (line[0] == line[2]) or (line[1] == line[3])


def part_1(data):
    data = filter(filter_line, data)  # Remove all entries not resulting in horizontal or vertical lines
    floor_map = MagicMatrix()
    for x in data:
        if x[1] == x[3]:  # Horizontal
            for i in range(min(x[0], x[2]), max(x[0], x[2]) + 1):
                floor_map[x[1], i] = (floor_map[x[1], i] or 0) + 1
        else:             # Vertical
            for i in range(min(x[1], x[3]), max(x[1], x[3]) + 1):
                floor_map[i, x[0]] = (floor_map[i, x[0]] or 0) + 1

    two_or_more_ct = 0
    for x in floor_map.values():
        if x >= 2:
            two_or_more_ct += 1

    print(f'Points where at least two lines overlap (orthogonal only): {two_or_more_ct}')


def part_2(data):
    floor_map = MagicMatrix()
    for d in data:
        if d[0] == d[2]:  # Vertical
            for i in range(min(d[1], d[3]), max(d[1], d[3]) + 1):
                floor_map[i, d[0]] = (floor_map[i, d[0]] or 0) + 1
        else:  # Horizontal / Diagonal
            if d[0] > d[2]:  # Make sure lines are arranged from left to right
                d[0], d[1], d[2], d[3] = d[2], d[3], d[0], d[1]
            if d[1] < d[3]:
                yrange = range(d[1], d[3] + 1)
            elif d[1] == d[3]:
                yrange = [d[1]] * (abs(d[0] - d[2]) + 1)
            else:
                yrange = range(d[1], d[3] - 1, -1)
            for x, y in zip(range(d[0], d[2] + 1), yrange):
                floor_map[y, x] = (floor_map[y, x] or 0) + 1

    two_or_more_ct = 0
    for x in floor_map.values():
        if x >= 2:
            two_or_more_ct += 1

    print(f'Points where at least two lines overlap (all): {two_or_more_ct}')


def parse_line(line):
    match = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', line)
    return [int(x) for x in match.groups()]


def main():
    with open('input.txt') as f:
        data = [parse_line(x) for x in f.readlines()]
    part_1(data)
    part_2(data)


if __name__ == '__main__':
    main()
