import re


# Taken from my attempt at AoC 2015
class MagicMatrix:
    """A 'magic matrix' that expands infinitely in all directions"""

    def __init__(self, empty_char='.'):
        self.__data = {}
        self.__extents = [0, 0, 0, 0]  # x1, y1, x2, y2
        self.__column_width = 1
        self.min = None
        self.max = None
        self.empty_char = empty_char

    def __getitem__(self, item):
        key = MagicMatrix.__translate_index(item)
        if key in self.__data:
            return self.__data[key]
        else:
            return None

    def __setitem__(self, key, value):
        translated_key = MagicMatrix.__translate_index(key)
        if translated_key not in self.__data:
            self.__extents[0] = min(self.__extents[0], key[0])
            self.__extents[1] = min(self.__extents[1], key[1])
            self.__extents[2] = max(self.__extents[2], key[0])
            self.__extents[3] = max(self.__extents[3], key[1])
        self.__column_width = max((self.__column_width, len(str(value)), len(str(self.__extents[1])),
                                   len(str(self.__extents[3]))))
        if self.min is None:
            self.min = value
            self.max = value
        else:
            self.min = min(self.min, value)
            self.max = max(self.max, value)
        self.__data[translated_key] = value

    def __len__(self):
        return len(self.__data)

    def __repr__(self):
        string = ''
        for i in range(self.__extents[0], self.__extents[2] + 1):
            string += '[ '
            for j in range(self.__extents[1], self.__extents[3] + 1):
                value = self[i, j]
                if value is not None:
                    string += str(value)
                    string += ' ' * (self.__column_width - len(str(value)))
                else:
                    string += self.empty_char
                    string += ' ' * (self.__column_width - 1)
                string += ' '
            string += ']  ' + str(i) + '\n' if i < self.__extents[2] else ']  ' + str(i)
        string += '\n\n  '
        for i in range(self.__extents[1], self.__extents[3] + 1):
            string += str(i)
            string += ' ' * (self.__column_width - len(str(i)) + 1)
        return string

    # Added in some iterators since the last version

    def __iter__(self):
        return (k for k in self.__data.keys())

    def values(self):
        return (v for v in self.__data.values())

    def items(self):
        return ((k, v) for (k, v) in self.__data.items())

    @staticmethod
    def __translate_index(item):
        assert isinstance(item, tuple) and len(item) == 2, 'Invalid index'
        return '{}, {}'.format(item[0], item[1])

    def get_width(self):
        return self.__extents[2] - self.__extents[0] + 1

    def get_height(self):
        return self.__extents[3] - self.__extents[1] + 1


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
