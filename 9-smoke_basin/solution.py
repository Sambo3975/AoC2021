from colorama import init, Fore, Style

init(autoreset=True)


def is_local_min(data, i, j, i_max, j_max):
    entry = data[i][j]
    return (i == 0 or entry < data[i - 1][j]) and (i == i_max - 1 or entry < data[i + 1][j]) and \
           (j == 0 or entry < data[i][j - 1]) and (j == j_max - 1 or entry < data[i][j + 1])


def part_1(data):
    i_max = len(data)
    j_max = len(data[0])
    total_risk = 0
    for i in range(i_max):
        for j in range(j_max):
            if is_local_min(data, i, j, i_max, j_max):
                total_risk += data[i][j] + 1
    print(f'Sum of risk levels: {total_risk}')


def draw_floor(data, marked, last_i, last_j):
    for i in range(len(data)):
        for j in range(len(data[0])):
            if i == last_i and j == last_j:
                print(Fore.CYAN + Style.BRIGHT + str(data[i][j]), end='')
            elif marked[i][j]:
                print(Fore.GREEN + str(data[i][j]), end='')
            else:
                print(data[i][j], end='')
        print()


def get_basin_size(data, i, j, i_max, j_max, debug=False, marked=None, size=0):
    if marked is None:
        marked = [[False for _ in range(j_max)] for _ in range(i_max)]

    marked[i][j] = True
    size += 1
    entry = data[i][j]
    if debug:
        draw_floor(data, marked, i, j)
        input('Press Enter: ')
        print()
    if i > 0 and not marked[i - 1][j] and entry < data[i - 1][j] < 9:
        size += get_basin_size(data, i - 1, j, i_max, j_max, debug, marked)
    if i < i_max - 1 and not marked[i + 1][j] and entry < data[i + 1][j] < 9:
        size += get_basin_size(data, i + 1, j, i_max, j_max, debug,  marked)
    if j > 0 and not marked[i][j - 1] and entry < data[i][j - 1] < 9:
        size += get_basin_size(data, i, j - 1, i_max, j_max, debug, marked)
    if j < j_max - 1 and not marked[i][j + 1] and entry < data[i][j + 1] < 9:
        size += get_basin_size(data, i, j + 1, i_max, j_max, debug, marked)

    return size


def part_2(data, debug=False):
    i_max = len(data)
    j_max = len(data[0])
    basin_sizes = []
    for i in range(i_max):
        for j in range(j_max):
            if is_local_min(data, i, j, i_max, j_max):
                basin_sizes.append(get_basin_size(data, i, j, i_max, j_max, debug))

    basin_sizes.sort(reverse=True)
    if debug:
        print(basin_sizes)
    product_of_sizes = 1
    for i in range(3):
        product_of_sizes *= basin_sizes[i]

    print(f'Product of 3 largest basin sizes: {product_of_sizes}')


def part_2_test(debug=False):
    with open('test.txt') as f:
        raw_data = f.readlines()
        data = []
        for line in raw_data:
            data.append([int(x) for x in line.strip()])
    part_2(data, debug)


def main():
    with open('input.txt') as f:
        raw_data = f.readlines()
        data = []
        for line in raw_data:
            data.append([int(x) for x in line.strip()])

    while True:
        print('Choose an option from below (q to quit): ')
        print('  1  : Part One')
        print('  2  : Part Two')
        print('  t1 : Basin Mapping Test')
        print('  t2 : Basin Size Test')
        print('------------------------------------------')
        match input('>> '):
            case '1':
                part_1(data)
            case '2':
                part_2(data)
            case 't1':
                part_2_test(True)
            case 't2':
                part_2_test()
            case 'q':
                break
            case _:
                print('Invalid Input')
        print()


if __name__ == '__main__':
    main()
