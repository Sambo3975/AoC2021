import re


# ------------------------
# Core Functionality
# ------------------------
from collections import defaultdict

import load_file
from option_selection import OptionSelector
from testing import test_bed


def load_start_positions(file_name):
    with open(file_name) as f:
        raw_data = f.readlines()
    starts = []
    for i in range(2):
        m = re.match(r'Player \d starting position: (\d+)', raw_data[i].strip())
        starts.append(int(m.group(1)))
    return starts[0] - 1, starts[1] - 1


def play_dirac_dice(positions):
    (p1_pos, p2_pos) = positions
    p1_turn = False
    roll = 0
    rolls = 0
    p1_score = 0
    p2_score = 0
    while p1_score < 1000 and p2_score < 1000:
        p1_turn = not p1_turn
        add = 3 * roll + 6
        if p1_turn:
            p1_pos = (p1_pos + add) % 10
            p1_score += p1_pos + 1
        else:
            p2_pos = (p2_pos + add) % 10
            p2_score += p2_pos + 1
        roll = (roll + 3) % 100
        rolls += 3

    if p1_turn:
        return 1, p2_score * rolls
    else:
        return 2, p1_score * rolls


def count_winning_futures(positions):
    possibilities = defaultdict(lambda: 0)
    possibilities[(positions[0], 0, positions[1], 0)] = 1
    p1_wins = 0
    p2_wins = 0

    while len(possibilities) > 0:

        next_turn = defaultdict(lambda: 0)

        for state, times in possibilities.items():

            (p1_pos, p1_score, p2_pos, p2_score) = state

            for i in range(1, 4):

                next_pos_1 = (p1_pos + i) % 10
                next_score_1 = p1_score + next_pos_1 + 1

                if next_score_1 >= 21:
                    p1_wins += times
                    continue

                for j in range(1, 4):

                    next_pos_2 = (p2_pos + j) % 10
                    next_score_2 = p2_score + next_pos_2 + 1

                    if next_score_2 >= 21:
                        p2_wins += times
                        continue

                    next_turn[(next_pos_1, next_score_1, next_pos_2, next_score_2)] += times

        possibilities = next_turn

    return p1_wins, p2_wins


# ---------------------
# Puzzle Solutions
# ---------------------


def part_1():
    positions = load_start_positions('input.txt')
    winner, final_score = play_dirac_dice(positions)
    print(f'Player {winner} wins! Final score: {final_score}')


# ---------------------
# Tests
# ---------------------


def test_deterministic():
    positions = load_start_positions('test_in.txt')
    outputs = load_file.as_literals('test_out.txt')
    test_bed(play_dirac_dice, [positions], outputs)


def test_multiverse():
    positions = load_start_positions('test_in.txt')
    test_bed(count_winning_futures, [positions], [(444356092776315, 341960390180808)])


# ---------------------
# Driver
# ---------------------


def main():
    selector = OptionSelector()
    selector.add_option('1', 'Part 1 -- Deterministic Game', part_1)
    selector.add_option('t1', 'Deterministic Test', test_deterministic)
    selector.add_option('t2', 'Dirac Test', test_multiverse)
    selector.run()


if __name__ == '__main__':
    main()
