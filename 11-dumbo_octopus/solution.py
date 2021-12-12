from colorama import init, Fore, Style
from copy import deepcopy

init(autoreset=True)


def flash(data, i, j, i_max, j_max, flashed):
    flashed[i][j] = True
    for k in range(i - 1, i + 2):
        for l in range(j - 1, j + 2):
            if 0 <= k < i_max and 0 <= l < j_max:
                data[k][l] += 1
                if data[k][l] > 9 and not flashed[k][l]:
                    flash(data, k, l, i_max, j_max, flashed)


def update_dumbos(data):
    i_max = len(data)
    j_max = len(data[0])
    i_range = range(i_max)
    j_range = range(j_max)
    flashed = [[False for _ in j_range] for _ in i_range]

    flashes = 0

    # Increase each octopus's energy by 1
    for i in i_range:
        for j in j_range:
            data[i][j] += 1

    # Handle flashing
    for i in i_range:
        for j in j_range:
            if data[i][j] > 9 and not flashed[i][j]:
                flash(data, i, j, i_max, j_max, flashed)

    # Handle energy reset
    for i in i_range:
        for j in j_range:
            if data[i][j] > 9:
                data[i][j] = 0
                flashed[i][j] = False
                flashes += 1

    return flashes, flashes == i_max * j_max


def draw_dumbos(data):
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == 0:
                print(Fore.CYAN + Style.BRIGHT + str(data[i][j]), end='')
            else:
                print(data[i][j], end='')
        print()
    print()


def prompt():
    input('Press Enter: ')


def simulate_dumbos(data, steps, verbose=False, flashes=0):
    # Passing a negative number for steps keeps going until all the dumbo octopuses are in sync.
    all_flashed = False

    if verbose:
        print('Before any steps:')
        draw_dumbos(data)
    i = 0
    while (steps > 0 and i < steps) or (steps < 0 and not all_flashed):
        step_flashes, all_flashed = update_dumbos(data)
        flashes += step_flashes
        if verbose:
            prompt()
            print(f'After step {i + 1}:')
            draw_dumbos(data)
        i += 1

    if all_flashed:
        print(f'All dumbo octopuses flashed on step {i}')
    print(f'Total flashes: {flashes}')
    return flashes


def test1_1(data):
    simulate_dumbos(data, 2, True)


def test1_2(data):
    flashes = simulate_dumbos(data, 10, True)
    for i in range(9):
        prompt()
        flashes = simulate_dumbos(data, 10, False, flashes)
        print(f'After step {20 + 10 * i}:')
        draw_dumbos(data)
    prompt()


def part_1(data):
    simulate_dumbos(data, 100)


def test2_1(data):
    simulate_dumbos(data, -1)


def part_2(data):
    simulate_dumbos(data, -1)


def load_file(file_name):
    with open(file_name) as f:
        raw_data = f.readlines()
    data = []
    for line in raw_data:
        data.append([int(c) for c in line.strip()])
    return data


def main():
    test1_1_data = None
    test1_2_data = None
    data = None
    while True:
        print('Choose an option from below (q to quit):')
        print('  1   : Part 1')
        print('  2   : Part 2')
        print('  t11 : Part 1 Test 1')
        print('  t12 : Part 1 Test 2')
        print('  t21 : Part 2 Test 1')
        print('------------------------------------------')
        match input('>> '):
            case '1':
                data = load_file('input.txt') if data is None else data
                part_1(deepcopy(data))
            case '2':
                data = load_file('input.txt') if data is None else data
                part_2(deepcopy(data))
            case 't11':
                test1_1_data = load_file('test.txt') if test1_1_data is None else test1_1_data
                test1_1(deepcopy(test1_1_data))
            case 't12':
                test1_2_data = load_file('test2.txt') if test1_2_data is None else test1_2_data
                test1_2(deepcopy(test1_2_data))
            case 't21':
                test1_2_data = load_file('test2.txt') if test1_2_data is None else test1_2_data
                test2_1(deepcopy(test1_2_data))
            case 'q':
                break
            case _:
                print('Invalid input')
        print()


if __name__ == '__main__':
    main()
