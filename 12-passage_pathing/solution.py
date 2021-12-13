from collections import deque


def add_adjacency(adjacencies, a, b):
    if a != 'end' and b != 'start':
        if a not in adjacencies:
            adjacencies[a] = []
        adjacencies[a].append(b)


def get_adjacencies(data):
    adjacencies = {}
    for x in data:
        add_adjacency(adjacencies, x[0], x[1])
        add_adjacency(adjacencies, x[1], x[0])
    return adjacencies


def count_paths(adjacencies, from_='start', path=None, count=0, verbose=False, allow_second_visit=False):
    options = deque(adjacencies[from_])
    if path is None:
        path = deque([from_])
    while len(options) > 0:
        to = options.popleft()
        if to == 'end':
            count += 1
            if verbose:
                print(path)
        elif to.isupper() or (to not in path) or allow_second_visit:
            allow_second_visit_next = (to.isupper() or (to not in path)) and allow_second_visit
            path.append(to)
            count = count_paths(adjacencies, to, path, count, verbose, allow_second_visit_next)
    path.pop()
    return count


def test_1(data, allow_second_visit=False):
    adjacencies = get_adjacencies(data)
    print(adjacencies)
    count_paths(adjacencies, verbose=True, allow_second_visit=allow_second_visit)


def part_1(data, allow_second_visit=False):
    print(f'There are {count_paths(get_adjacencies(data), allow_second_visit=allow_second_visit)} paths.')


def part_2(data):
    pass


def load_file(file_name):
    with open(file_name) as f:
        return [x.strip().split('-') for x in f.readlines()]


def main():
    while True:
        print('Choose an option from below (q to quit):')
        print('  1  : Part 1 - Path count')
        print('  2  : Part 2 - Path count (one second visit)')
        print('  t1 : Part 1 tests')
        print('  t2 : Part 2 tests')
        print('-----------------------------------------------')
        match input('>> '):
            case '1':
                part_1(load_file('input.txt'))
            case '2':
                part_1(load_file('input.txt'), True)
            case 't1':
                print('Example 1:')
                test_1(load_file('test.txt'))
                print('Example 2: ', end='')
                part_1(load_file('test2.txt'))
                print('Example 3: ', end='')
                part_1(load_file('test3.txt'))
            case 't2':
                print('Example 1:')
                test_1(load_file('test.txt'), True)
                print('Example 2: ', end='')
                part_1(load_file('test2.txt'), True)
                print('Example 3: ', end='')
                part_1(load_file('test3.txt'), True)
            case 'q':
                break
            case _:
                print('Invalid input')
        print()


if __name__ == '__main__':
    main()
