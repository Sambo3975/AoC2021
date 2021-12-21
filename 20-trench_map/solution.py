# -----------------------
# Core Functionality
# -----------------------
from magic_matrix import MagicMatrix
from option_selection import OptionSelector


def load_file(file_name):
    raw_algorithm: str
    raw_image: str
    with open(file_name) as f:
        algorithm, raw_image = f.read().split('\n\n')
    image_rows = raw_image.strip().split()
    image = MagicMatrix()
    for i in range(len(image_rows)):
        for j in range(len(image_rows[i])):
            if image_rows[i][j] == '#':
                image[i, j] = '#'

    return algorithm, image


def enhance(algorithm: str, image: MagicMatrix):
    top, left, bottom, right = image.extents()
    enhanced = MagicMatrix()
    if image.default_value == '#':
        enhanced.default_value = algorithm[-1]
    else:
        enhanced.default_value = algorithm[0]
    for i in range(top - 1, bottom + 2):
        for j in range(left - 1, right + 2):
            index = ''
            for k in range(i - 1, i + 2):
                for l in range(j - 1, j + 2):
                    index += '1' if image[k, l] == '#' else '0'
            index = int(index, 2)
            if algorithm[index] == '#':
                enhanced[i, j] = '#'
            else:
                enhanced[i, j] = '.'

    return enhanced


def multi_phase_enhance(file_name, enhancements, debug=False):
    algorithm, image = load_file(file_name)
    if debug:
        print(f'Before enhancement:\n\n{image}\n')
    for i in range(enhancements):
        image = enhance(algorithm, image)
        if debug:
            print(f'After {i + 1} enhancement(s):\n\n{image}\n')

    return image


def count_lit(image):
    lit = 0
    for v in image.values():
        if v == '#':
            lit += 1

    return lit


# -------------------
# Puzzle Solutions
# -------------------


def part_1():
    image = multi_phase_enhance('input.txt', 2)

    lit = count_lit(image)
    print(f'{lit} pixels are lit.')


def part_2():
    image = multi_phase_enhance('input.txt', 50)

    lit = count_lit(image)
    print(f'{lit} pixels are lit.')


# -------------------
# Tests
# -------------------


def test_enhancements():
    image = multi_phase_enhance('test.txt', 2, True)

    lit = count_lit(image)
    print(f'{lit} pixels are lit.')


def test_more_enhancements():
    image = multi_phase_enhance('test.txt', 50)

    lit = count_lit(image)
    print(f'{lit} pixels are lit.')


# -------------------
# Driver
# -------------------


def main():
    selector = OptionSelector()
    selector.add_option('1', 'Part 1 -- 2 Enhancements', part_1)
    selector.add_option('2', 'Part 2 -- 50 Enhancements', part_2)
    selector.add_option('t1', '2-Enhancement test', test_enhancements)
    selector.add_option('t2', '50-Enhancement test', test_more_enhancements)
    selector.run()


if __name__ == '__main__':
    main()
