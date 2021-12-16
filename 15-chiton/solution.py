# I could have done A*, but according to the Subreddit, it has little to no benefit over Dijkstra for this problem.
import load_file
from grid import WeightedGrid, dijkstra_search
from timeit import timeit
from numpy import zeros


# ---------------------
# Helper Functions
# ---------------------

def extend_grid(grid):
    length = len(grid)
    new_grid = zeros((5 * length, 5 * length), dtype=int)
    for i in range(5 * length):
        for j in range(5 * length):
            new_grid[i][j] = (grid[i % length][j % length] + abs(i // length) + abs(j // length) - 1) % 9 + 1
    return new_grid


# --------------------
# Puzzle Solutions
# --------------------

def part_1():
    grid = WeightedGrid.from_file('input.txt')
    came_from, cost = dijkstra_search(grid)
    print(f'Lowest risk value: {cost}')


def part_2():
    grid = load_file.as_digit_grid('input.txt')
    grid = extend_grid(grid)
    grid = WeightedGrid(grid)
    came_from, cost = dijkstra_search(grid)
    print(f'Lowest risk value: {cost}')


# ---------------------
# Tests
# ---------------------

def test_1():
    grid = WeightedGrid.from_file('test.txt')
    came_from, cost = dijkstra_search(grid)
    print(f'Lowest risk value: {cost}')


def test_2():
    grid = load_file.as_digit_grid('test2.txt')
    grid = extend_grid(grid)
    print(grid)


def test_3():
    grid = load_file.as_digit_grid('test.txt')
    grid = WeightedGrid(extend_grid(grid))
    came_from, cost = dijkstra_search(grid)
    print(f'Lowest risk value: {cost}')


# -------------------
# Driver
# -------------------

def main():
    while True:
        print('Choose an option from below (q to quit):')
        print('  1  : 100x100 best path search')
        print('  2  : 500x500 best path search')
        print('  t1 : Pathfinding test')
        print('  t2 : Grid extension test')
        print('  t3 : Large pathfinding test')
        print('--------------------------------------------')
        time = None
        match input('>> '):
            case '1':
                time = timeit(part_1, number=1)
            case '2':
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
            print(f'Completed after {time:.4f} s')
        print()


if __name__ == '__main__':
    main()
