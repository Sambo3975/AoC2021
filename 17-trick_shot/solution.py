import re

from option_selection import OptionSelector

CoordinatePair = tuple[int, int]
Boundary = tuple[int, int, int, int]
Trajectory = dict[tuple[int, int], bool]


# ---------------------------
# Core Functions
# ---------------------------


def load_file(file_name: str):
    with open(file_name) as f:
        match = re.match(r'^target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)$', f.read().strip())
    match = [int(x) for x in match.groups()]
    return match[0], match[2], match[1], match[3]


def step_probe(x: int, y: int, vx: int, vy: int, trajectory: Trajectory = None):
    x += vx
    y += vy
    vx = max(vx - 1, 0)
    vy -= 1
    if trajectory is not None:
        trajectory[(x, y)] = True
    return x, y, vx, vy


def reaches_target(velocity: CoordinatePair, target: Boundary):
    """
    Check if a probe launched with the given velocity will reach the target area
    :param velocity Starting velocity (vx, vy)
    :param target Bounds of target area (left, bottom, right, top)
    :return: True if the probe reaches the target
    """
    (vx, vy) = velocity
    (tx1, ty1, tx2, ty2) = target
    x, y = 0, 0
    trajectory: Trajectory = {}
    while True:
        x, y, vx, vy = step_probe(x, y, vx, vy, trajectory)
        if tx1 <= x <= tx2 and ty1 <= y <= ty2:
            return True, trajectory
        elif (x < tx1 and vx == 0) or x > tx2 or (y < ty1 and vy < 0):
            return False, trajectory


def find_best_vx(target: Boundary):
    """
    Find the "best" starting x-velocity for the probe. The "best" value should be the lowest possible, as this gives
    us more time before arriving, thus giving us more time to go up high, then come back down
    :param target: The target area
    :return: The "best" value for vx
    """
    start_vx = -1
    while True:
        start_vx += 1
        vx = start_vx
        x = 0
        while vx > 0:
            x, _, vx, _ = step_probe(x, 0, vx, 0)
        if x >= target[0]:
            return start_vx


def find_best_vy(target: Boundary):
    """
    Find the "best" starting y-velocity for the probe. This value should be as high as possible without "clipping"
    through the target
    :param target: The target area
    :return: vy: int -- Best vy value
    """
    # Probe will come back down to the y-level where it started with v[y] = -vi[y]
    # On the step after that, it will be moving with v[y] = -(vi[y] + 1)
    # This means we need (vi[i] + 1) to be equal to the position of the bottom of the target
    return -(target[1] + 1)


def find_coolest_shot(target: Boundary):
    """
    Find the "coolest" shot that will reach the target area
    :param target: Target area
    :return:
        (vx, vy) -- Starting velocity
        trajectory: Trajectory -- Trajectory from start position to target
    """
    vx = find_best_vx(target)
    vy = find_best_vy(target)
    return vx, vy


def count_options(target: Boundary):
    """
    Count the number of shots that make it to the target using brute force
    :param target: Target area
    :return: options: int
    """
    (left, bottom, right, top) = target
    solutions = 0
    x_min = find_best_vx(target)
    y_max = find_best_vy(target)
    for vy in range(bottom, y_max + 2):
        for vx in range(x_min, right + 2):
            if reaches_target((vx, vy), target)[0]:
                solutions += 1

    return solutions


# ------------------------
# Prints
# ------------------------


def get_char_at(trajectory: Trajectory, target: Boundary, position: CoordinatePair):
    if position == (0, 0):
        return 'S'
    if position in trajectory:
        return '#'
    (x, y) = position
    (left, bottom, right, top) = target
    if left <= x <= right and bottom <= y <= top:
        return 'T'
    return '.'


def draw_trajectory(trajectory: Trajectory, target: Boundary, window: Boundary = None):
    if window is None:
        bottom = min(min(trajectory, key=lambda t: t[1])[1], target[1])
        right = max(max(trajectory)[0], target[2])
        top = max(max(trajectory, key=lambda t: t[1])[1], target[3], 0)
        window = (0, bottom, right, top)

    (left, bottom, right, top) = window

    print('\n'.join([
        ''.join([get_char_at(trajectory, target, (x, y)) for x in range(left, right + 1)])
        for y in range(top, bottom - 1, -1)]))


# ----------------------
# Puzzle Solutions
# ----------------------


def part_1():
    target = load_file('input.txt')
    velocity = find_coolest_shot(target)
    _, trajectory = reaches_target(velocity, target)
    max_y = max(trajectory, key=lambda t: t[1])[1]
    print(f'Velocity for coolest shot, {velocity}, reaches y={max_y}')


def part_2():
    target = load_file('input.txt')
    options = count_options(target)
    print(f'{options} unique velocities will reach the target')


# ----------------------
# Tests
# ----------------------


def test_trajectory():
    target = load_file('test.txt')
    while True:
        match input('Enter 2 numbers to simulate a probe launch (q to quit): ').split():
            case [vx, vy]:
                try:
                    hit, trajectory = reaches_target((int(vx), int(vy)), target)
                    print('Hit!' if hit else 'Miss.')
                    draw_trajectory(trajectory, target)
                except ValueError:
                    print('Invalid input')
            case ['q']:
                break
            case _:
                print('Invalid input')


def test_coolest_shot():
    target = load_file('test.txt')
    velocity = find_coolest_shot(target)
    _, trajectory = reaches_target(velocity, target)
    print(f'Velocity for coolest shot: {velocity}')
    draw_trajectory(trajectory, target)


def test_find_all_shots():
    target = load_file('test.txt')
    options = count_options(target)
    print(f'{options} unique velocities will reach the target')


# -------------------------
# Driver
# -------------------------


def main():
    selector = OptionSelector()
    selector.add_option('1', 'Part 1 -- Coolest shot search', part_1)
    selector.add_option('2', 'Part 2 -- Comprehensive shot search', part_2)
    selector.add_option('t1', 'Trajectory simulation test', test_trajectory)
    selector.add_option('t2', 'Coolest shot search test', test_coolest_shot)
    selector.add_option('t3', 'Comprehensive shot search test', test_find_all_shots)
    selector.run()


if __name__ == '__main__':
    main()
