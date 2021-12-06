import glob
import importlib
import os
import re


def help_msg():
    print('Welcome to Advent of Code 2021!')
    print('Enter a number between 1 and 25 to choose a day.')
    print('Enter \'q\' to quit.')
    print('Enter \'h\' do display this message again.')


def day_title(path):
    match = re.match(r'^(\d+)(-[a-z_]+)', path)
    # print(data)
    day_number = match.group(1)
    name = re.sub(r'[-_](\w)', lambda pat: ' ' + pat.group(1).upper(), match.group(2))
    print(f'Day {day_number}:{name}')


if __name__ == '__main__':
    help_msg()
    while True:
        cmd = input('> ')
        match cmd:
            case 'q':
                break
            case 'h':
                help_msg()
            case _:
                try:
                    day = int(cmd)
                    if 1 <= day <= 25:
                        paths = glob.glob(cmd + '-*/')
                        if len(paths) > 0:
                            solution = importlib.import_module(paths[0][:-1] + '.solution')
                            print()
                            day_title(paths[0])
                            os.chdir(paths[0])  # Move to the selected day's path, so it can open files properly
                            solution.main()     # The linter doesn't like this, but it works fine
                            print()
                            os.chdir('../')     # Move back up to the root directory so this will work repeatedly
                        else:
                            print(f'Day {day} not yet implemented.')
                    else:
                        print(f'Day {day} out of range.')
                except ValueError:
                    print('Invalid input.')
