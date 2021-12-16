# I could have done A*, but according to the Subreddit, it has little to no benefit over Dijkstra for this problem.
import load_file
from grid import WeightedGrid, dijkstra_search
from numpy import zeros


# ---------------------
# Helper Functions
# ---------------------
from option_selection import OptionSelector


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
    selector = OptionSelector(timed=True)
    selector.add_option('1', '100x100 best path search', part_1)
    selector.add_option('2', '500x500 best path search', part_2)
    selector.add_option('t1', 'Pathfinding test', test_1)
    selector.add_option('t2', 'Grid extension test', test_2)
    selector.add_option('t3', 'Large pathfinding test', test_3)
    selector.run()


if __name__ == '__main__':
    main()
