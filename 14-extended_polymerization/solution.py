import re
from collections import Counter, defaultdict


def load_file(file_name):
    with open(file_name) as f:
        raw_data = f.read().split('\n\n')
    template = raw_data[0]

    rules = []
    for r in raw_data[1].strip().split('\n'):
        rules.append(r.split(' -> '))

    return template, rules


def lengthen_polymer(template, rules):
    insertions = {}  # Keeps track of new characters to insert; indexed by position in the original string
    for x in rules:
        # (?=<str>) is a lookahead for <str>. It matches with an empty string at the position of <str>
        # a(?=b) would match an 'a' that is followed by a 'b' (but would not include the 'b' as part of the match)
        # Used here, it allows us to find overlapping occurrences of the substring
        for m in re.finditer(rf'(?={x[0]})', template):
            insertions[m.start() + 1] = x[1]  # The new character should be inserted between the matched pair

    result = ""
    for i in range(len(template)):
        if i in insertions:
            result += insertions[i]
        result += template[i]

    return result


# This works great for part 1. Part 2 ... Not so much.
# 40 steps creates a polymer chain that is 20 TB in size.
def do_polymerization(file_name, steps):
    template, rules = load_file(file_name)
    for i in range(steps):
        template = lengthen_polymer(template, rules)
    most_common = Counter(template).most_common()
    print(f'Most Common - Least Common = {most_common[0][1] - most_common[-1][1]}')


# I say "fast," but "memory-efficient" would be more accurate
def do_fast_polymerization(file_name, steps):
    template, rules = load_file(file_name)
    pair_mappings = {}
    for x in rules:
        pair_mappings[x[0]] = (x[0][0] + x[1], x[1] + x[0][1])
    pairs = defaultdict(lambda: 0)
    element_counts = defaultdict(lambda: 0)  # The initial template may not contain all elements
    for i in range(len(template)):
        if i < len(template) - 1:
            pairs[template[i:i + 2]] += 1
        element_counts[template[i]] += 1

    for _ in range(steps):
        new_pairs = defaultdict(lambda: 0)
        for k, v in pairs.items():
            mapping = pair_mappings[k]
            element_counts[mapping[0][1]] += v
            new_pairs[mapping[0]] += v
            new_pairs[mapping[1]] += v
        pairs = new_pairs

    element_counts = [v for v in element_counts.values()]
    diff = max(element_counts) - min(element_counts)
    print(f'Most Common - Least Common = {diff}')


def part_1():
    do_polymerization('input.txt', 10)


def part_2():
    do_fast_polymerization('input.txt', 40)


def test_1():
    template, rules = load_file('test.txt')
    print(f'Template:      {template}')
    for i in range(10):
        template = lengthen_polymer(template, rules)
        if i < 4:
            print(f'After step {i + 1:2}: {template}')
        elif i == 4 or i == 9:
            print(f'After step {i + 1:2}: Length {len(template)}')
    print('Occurrence counts:')
    print(c := Counter(template))
    most_common = c.most_common()
    print(f'Most Common - Least Common = {most_common[0][1] - most_common[-1][1]}')


def test_2():
    do_fast_polymerization('test.txt', 40)


def main():
    while True:
        print('Choose an option from below (q to quit):')
        print('  1  : Part 1 -- 10-step polymerization')
        print('  2  : Part 2 -- 40-step polymerization')
        print('  t1 : 10-step polymerization test')
        print('  t2 : 40-step polymerization test')
        print('------------------------------------------')
        match input('>> '):
            case '1':
                part_1()
            case '2':
                part_2()
            case 't1':
                test_1()
            case 't2':
                test_2()
            case 'q':
                break
            case _:
                print('Invalid input')
        print()


if __name__ == '__main__':
    main()
