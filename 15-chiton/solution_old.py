"""This was my first attempt. It is horrendously inefficient, taking 3 minutes for part 1 and longer than I care to
determine for part 2. I think it's all the conditional branching. """

from heapq import heappop, heappush
from timeit import timeit

from colorama import init, Fore, Style
from numpy import array, zeros

init(autoreset=True)


def load_file(file_name):
    with open(file_name) as f:
        return array([[int(x) for x in y.strip()] for y in f.readlines()], dtype=int)


def extend_grid(grid):
    length = len(grid)
    new_grid = zeros((5 * length, 5 * length), dtype=int)
    for i in range(5 * length):
        for j in range(5 * length):
            new_grid[i][j] = (grid[i % length][j % length] + abs(i // length) + abs(j // length) - 1) % 9 + 1
    return new_grid


def trace_path(visited, start_i=0, start_j=0, goal_i=None, goal_j=None):
    if goal_i is None:
        goal_i = len(visited) - 1
        goal_j = len(visited[0]) - 1
    i = goal_i
    j = goal_j
    path = [(i, j)]
    while i != start_i or j != start_j:
        i, j = visited[i][j]
        path.append((i, j))
    path.reverse()
    return path


def shortest_path(grid, start_i=0, start_j=0, goal_i=None, goal_j=None):
    """Find the shortest path using a version of Dijkstra's Algorithm"""
    if goal_i is None:
        goal_i = len(grid) - 1
        goal_j = len(grid[0]) - 1
    visited = [[None for _ in range(len(grid[0]))] for _ in range(len(grid))]
    queue: list[tuple] = [(0, start_i, start_j, None, None)]  # Priority queue (AKA heap queue)

    while len(queue) > 0:
        weight, node_i, node_j, via_i, via_j = heappop(queue)
        if via_i is not None and visited[node_i][node_j] is None:
            visited[node_i][node_j] = (via_i, via_j)
        if node_i == goal_i and node_j == goal_j:
            return weight, visited
        # Prioritize steps that would move us down and to the right
        if node_i < len(grid) - 1 and visited[node_i + 1][node_j] is None:
            heappush(queue, (weight + grid[node_i + 1][node_j], node_i + 1, node_j, node_i, node_j))
        if node_j < len(grid[0]) - 1 and visited[node_i][node_j + 1] is None:
            heappush(queue, (weight + grid[node_i][node_j + 1], node_i, node_j + 1, node_i, node_j))
        if node_i > 0 and visited[node_i - 1][node_j] is None:
            heappush(queue, (weight + grid[node_i - 1][node_j], node_i - 1, node_j, node_i, node_j))
        if node_j > 0 and visited[node_i][node_j - 1] is None:
            heappush(queue, (weight + grid[node_i][node_j - 1], node_i, node_j - 1, node_i, node_j))

    raise ValueError(f'Could not find path from ({start_i}, {start_j}) to ({goal_i}, {goal_j})')


def part_1():
    grid = load_file('input.txt')
    weight, _ = shortest_path(grid)
    print(f'Lowest risk value: {weight}')


def part_2():
    grid = load_file('input.txt')
    weight, _ = shortest_path(extend_grid(grid))
    print(f'Lowest risk value: {weight}')


def test_1():
    grid = load_file('test.txt')
    weight, visited = shortest_path(grid)
    path = trace_path(visited)
    print(f'Lowest risk value: {weight}')
    print('Lowest risk path:')
    print('Key: ' + Fore.GREEN + '[visited] ' + Fore.CYAN + Style.BRIGHT + '[path]')
    for i in range(len(grid)):
        for j in range(len(grid)):
            if (i, j) in path:
                print(Fore.CYAN + Style.BRIGHT + str(grid[i][j]), end='')
            elif visited[i][j]:
                print(Fore.GREEN + str(grid[i][j]), end='')
            else:
                print(grid[i][j], end='')
        print()
    print()


def test_2():
    grid = load_file('test2.txt')
    grid = extend_grid(grid)
    print(grid)


def test_3():
    grid = load_file('test.txt')
    weight, _ = shortest_path(extend_grid(grid))
    print(f'Lowest risk value: {weight}')


def main():
    while True:
        print('Choose an option from below (q to quit):')
        print('  1  : Weight of lowest-risk path (~3 min)')
        print('  2  : Weight of lowest-risk path (big)')
        print('  t1 : Pathfinding test')
        print('  t2 : Grid extension test')
        print('  t3 : Thicc pathfinding test')
        print('--------------------------------------------')
        time = None
        match input('>> '):
            case '1': # Takes 3 minutes
                time = timeit(part_1, number=1)
            case '2':  # Takes at least 1.5 hours and fills up my RAM (I gave up on it before it finished)
                time = timeit(part_2, number=1)
            case 't1':
                time = timeit(test_1, number=1)
            case 't2':
                time = timeit(test_2, number=1)
            case 't3':
                time = timeit(test_3, number=1)
            case 'q':
                break
            case _:
                print('Invalid input')
        if time is not None:
            print(f'Completed after {time // (60 ** 60):d} h {time // 60:d} m {time % 60:.4f} s')
        print()


if __name__ == '__main__':
    main()
