import random

from bingo_board import BingoBoard, draw_boards
from tail_recursion import tail_recursive, recurse


def part_1_test(calls, boards):
    print('Welcome to Bingo!')
    draw_boards(*boards)
    for c in calls:
        input('Press Enter to call a number: ')
        print(f'Called {c}!')
        win = False
        for i in range(len(boards)):
            if score := boards[i].call(c):
                win = (i, score)
                break
        draw_boards(*boards)
        if win:
            print(f'Board {win[0] + 1} wins! Score: {win[1]}')
            break


def part_1(calls, boards):
    print('Locating best board...')
    for c in calls:
        for i in range(len(boards)):
            if score := boards[i].call(c):
                print(f'Board {i + 1} wins! Score: {score}')
                return


def part_2(calls, boards):
    print('Locating worst board...')
    calls.reverse()
    while len(boards) > 1:
        call = calls.pop()
        next_boards = []
        for x in boards:
            if not x.call(call):
                next_boards.append(x)
        boards = next_boards
    while not (score := boards[0].call(calls.pop())):
        continue
    print(f'The worst board has a score of {score}.')


def read_game(file):
    with open(file) as f:
        game_data = f.read().split('\n\n')
    calls = [int(x) for x in game_data[0].split(',')]
    boards = []
    for i in range(1, len(game_data)):
        boards.append(BingoBoard([int(x) for x in game_data[i].strip().split()]))

    return calls, boards


def input_int(prompt, mini, maxi, default):
    while True:
        try:
            selection = input(f'{prompt} ({mini}-{maxi}) [{default}]? ')
            if selection == '':
                selection = default
            else:
                selection = int(selection)
            if selection < mini or selection > maxi:
                raise ValueError
            return selection
        except ValueError:
            continue


def input_yn(prompt, default):
    while True:
        match input(f'{prompt} (y/n) [{default}]? '):
            case '':
                return False if default == 'n' else True
            case 'y' | 'Y':
                return True
            case 'n' | 'N':
                return False


@tail_recursive
def new_game(players=None, size=None, num_range=None, diagonal_win=None):

    # Pre-initialization

    players = players or input_int('How many players', 2, 6, 2)
    size = size or input_int('What board size', 3, 10, 5)
    min_range = size ** 2
    num_range = num_range or input_int('What\'s the highest number', min_range, 999, max(min_range, 99))
    if diagonal_win is None:
        diagonal_win = input_yn('Are diagonal wins allowed', 'y')

    # Initialization

    calls = random.sample(range(num_range), num_range)
    boards = [BingoBoard(random.sample(range(num_range), min_range), diagonal_win) for _ in range(players)]

    draw_boards(*boards)

    # Game

    winner = None
    skip = False
    while winner is None:
        if not skip:
            if input('Press Enter to call the next number (s to skip to end): ') == 's':
                skip = True
        called_on_board = False
        c = -1
        while not called_on_board:
            c = calls.pop()
            for i in range(len(boards)):
                win = boards[i].call(c)
                if boards[i].called_on_board:
                    called_on_board = True
                # Ties are broken by score
                if (win and not winner) or (winner and win > winner[1]):
                    if winner:
                        boards[winner[0]].win = None
                    winner = (i, win)

        if not skip:
            print(f'Called {c}!')
        if not skip or winner:
            draw_boards(*boards)

    if winner:
        print(f'Board {winner[0] + 1} wins! Score: {winner[1]}')

    # Post-Game

    if input_yn('Play again', 'y'):
        recurse(players, size, num_range, diagonal_win)


def main():
    while True:
        print('Welcome to Bingo! Choose an option from below! (q to quit)')
        print('Advent of Code:')
        print('  t1: test game')
        print('   1: part one solution')
        print('   2: part two solution')
        print('Randomly-generated games:')
        print('  s: standard game (5x5, numbers 0-99, no diagonal wins)')
        print('  d: diagonal game (5x5, numbers 0-99, with diagonal wins)')
        print('  c: custom game (choose board size, numbers, and whether diagonal wins are allowed)')
        print('  r: random game (random board size, random numbers, and random diagonal win setting)')
        print('--------------------------------------------------------------------------------------')
        enter_to_continue = True
        match input('> '):
            case 't1':
                part_1_test(*read_game('test.txt'))
            case '1':
                part_1(*read_game('input.txt'))
            case '2':
                part_2(*read_game('input.txt'))
            case 's':
                new_game(None, 5, 99, False)
                enter_to_continue = False
            case 'd':
                new_game(None, 5, 99, True)
                enter_to_continue = False
            case 'c':
                new_game()
                enter_to_continue = False
            case 'r':
                size = random.randint(3, 10)
                numbers = random.randint(size ** 2, 999)
                diagonal = bool(random.randint(0, 1))
                print(f'Rules: {size}x{size}, numbers up to {numbers}, {"with" if diagonal else "no"} diagonal wins')
                new_game(None, size, numbers, diagonal)
                enter_to_continue = False
            case 'q':
                print('Goodbye!')
                break
            case _:
                enter_to_continue = False
                print('Invalid input')
        if enter_to_continue:
            print()
            input('Press Enter to continue: ')
        print()


if __name__ == '__main__':
    main()
