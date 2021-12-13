import re

from magic_matrix import MagicMatrix


def load_file(file_name):
    with open(file_name) as f:
        raw_data = f.read().split('\n\n')

    sheet = MagicMatrix()
    for c in raw_data[0].split():
        (x, y) = [int(x) for x in c.split(',')]
        sheet[y, x] = '#'

    folds = []
    for f in raw_data[1].strip().split('\n'):
        match = re.match(r'^fold along ([xy])=(\d+)$', f)
        folds.append((match.group(1), int(match.group(2))))

    return sheet, folds


def fold(sheet: MagicMatrix, instruction: tuple):
    new_sheet = MagicMatrix()
    if instruction[0] == 'x':
        for x1, x2 in zip(range(instruction[1] - 1, -1, -1), range(instruction[1] + 1, sheet.get_height())):
            for y in range(sheet.get_width()):
                if (new_val := sheet[y, x1] or sheet[y, x2]) is not None:
                    new_sheet[y, x1] = new_val
    elif instruction[0] == 'y':
        for y1, y2 in zip(range(instruction[1] - 1, -1, -1), range(instruction[1] + 1, sheet.get_width())):
            for x in range(sheet.get_height()):
                if (new_val := sheet[y1, x] or sheet[y2, x]) is not None:
                    new_sheet[y1, x] = new_val
    return new_sheet


def test_1(sheet, folds):
    print(sheet)
    sheet = fold(sheet, folds[0])
    print()
    print(sheet)
    print()
    print(f'{len(sheet)} dots are visible.')
    sheet = fold(sheet, folds[1])
    print()
    print(sheet)


def part_1(sheet, folds):
    sheet = fold(sheet, folds[0])
    print(f'{len(sheet)} dots are visible.')


def part_2(sheet, folds):
    for x in folds:
        sheet = fold(sheet, x)
    print(sheet)


def main():
    test_sheet, test_folds = load_file('test.txt')
    sheet, folds = load_file('input.txt')
    while True:
        print('Choose an option from below (q to quit):')
        print('  1  : Part 1 - Single fold')
        print('  2  : Part 2 - Reveal Activation Code')
        print('  t1 : Folding test')
        print('------------------------------------------')
        match input('>> '):
            case '1':
                part_1(sheet, folds)
            case '2':
                part_2(sheet, folds)
            case 't1':
                test_1(test_sheet, test_folds)
            case 'q':
                break
            case _:
                print('Invalid input')
        print()


if __name__ == '__main__':
    main()
