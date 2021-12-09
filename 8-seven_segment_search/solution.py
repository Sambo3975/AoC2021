unique_segments_map = {}

number_to_segments = {
    0: set('abcefg'),
    1: set('cf'),
    2: set('acdeg'),
    3: set('acdfg'),
    4: set('bcdf'),
    5: set('abdfg'),
    6: set('abdefg'),
    7: set('acf'),
    8: set('abcdefg'),
    9: set('abcdfg'),
}

ords = range(ord('a'), ord('g') + 1)


def part_1(data):
    unique_digit_count = 0
    for x in data:
        for y in x[1]:
            if len(y) in unique_segments_map:
                unique_digit_count += 1
    print(f'There are {unique_digit_count} digits with a unique number of segments.')


def test_decoder(encoded, decoder):
    decoded = 0
    for e in encoded:
        s = set(decoder[x] for x in e)
        valid_digit = False
        for k, v in number_to_segments.items():
            if s == v:
                decoded *= 10
                decoded += k
                valid_digit = True
                break
        if not valid_digit:
            return None
    return decoded


def decode(note):
    all_segments = set([chr(x) for x in ords])
    wire_to_segments = {}
    for x in ords:
        wire_to_segments[chr(x)] = all_segments.copy()

    # This allows us to deduce down to 8 possible encodings

    for signals in note[0]:
        if (num_segments := len(signals)) in unique_segments_map and num_segments < 7:
            inv_signals = all_segments.difference(signals)
            segments = number_to_segments[unique_segments_map[num_segments]]
            inv_segments = all_segments.difference(segments)
            for x in signals:
                wire_to_segments[x] = wire_to_segments[x].difference(inv_segments)
            for x in inv_signals:
                wire_to_segments[x] = wire_to_segments[x].difference(segments)

    for x in ords:
        wire_to_segments[c] = list(wire_to_segments[c := chr(x)])

    pairs = []
    single = None
    for k, v in wire_to_segments.items():
        if len(v) == 2:
            for k2, v2 in wire_to_segments.items():
                if k2 > k and v == v2:
                    pairs.append((k, k2))
        else:
            single = k

    for i in range(2):
        for j in range(2):
            for k in range(2):
                decoder = {
                    single: wire_to_segments[single][0],
                }
                for pair, idx in zip(pairs, (i, j, k)):
                    decoder[pair[0]] = wire_to_segments[pair[0]][idx]
                    decoder[pair[1]] = wire_to_segments[pair[0]][(idx + 1) % 2]
                if decoded := test_decoder(note[1], decoder):
                    return decoded


def part_2_test():
    with open('test2.txt') as f:
        data = [parse_line(x) for x in f.readlines()]
    decoded = [decode(x) for x in data]
    for note, number in zip(data, decoded):
        print(f'{note[1]} -> {number}')
    print(f'Total of all outputs: {sum(decoded)}')


def part_2(data):
    decoded = [decode(x) for x in data]
    print(f'Total of all outputs: {sum(decoded)}')


def parse_line(line):
    return [x.strip().split() for x in line.split('|')]


def main():
    for s, d in zip((2, 4, 3, 7), (1, 4, 7, 8)):
        unique_segments_map[s] = d
    with open('input.txt') as f:
        data = [parse_line(x) for x in f.readlines()]
    while True:
        print('Choose an option from below (q to quit):')
        print('  1  : Part One')
        print('  2  : Part Two')
        print('  t2 : Part Two Test')
        print('-----------------------------------------')
        match input('>> '):
            case '1':
                part_1(data)
            case '2':
                part_2(data)
            case 't2':
                part_2_test()
            case 'q':
                break
            case _:
                print('invalid input')
        print()


if __name__ == '__main__':
    main()
