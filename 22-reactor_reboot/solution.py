import re
import numpy as np

from option_selection import OptionSelector
from testing import test_bed

# ----------------------
# Parsing
# ----------------------

pattern_line = re.compile(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)')


def parse_file(file_name, ignore_large=False):
    inputs = []
    with open(file_name) as f:
        for line in f.readlines():
            m = pattern_line.match(line)
            state = True if m.group(1) == 'on' else False
            groups = m.groups()
            coordinates = tuple([int(groups[i]) for i in range(len(groups)) if i > 0])
            if ignore_large and ((c0 := coordinates[0]) < -50 or c0 > 50):
                break
            inputs.append((state, coordinates))

    return inputs


# ---------------------------
# Part 1
# ---------------------------

def initialize_reactor(instructions):
    reactor = np.full((101, 101, 101), fill_value=False, dtype=bool)
    for ins in instructions:
        state = ins[0]
        (x1, x2, y1, y2, z1, z2) = [c + 50 for c in ins[1]]
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    reactor[x, y, z] = state

    on_count = 0
    for x in range(101):
        for y in range(101):
            for z in range(101):
                if reactor[x, y, z]:
                    on_count += 1

    return on_count


def test_small_initialization():
    instructions = (
        parse_file('small_in.txt'),
        parse_file('test_in.txt', True),
    )
    test_bed(initialize_reactor, instructions, (39, 590784))


def part_1():
    instructions = parse_file('input.txt', True)
    on_count = initialize_reactor(instructions)
    print(f'{on_count} cubes are on.')


# -------------------------
# Part 2
# -------------------------

# The numbers after the initialization region are far too large for us to make a 3D array. This means we need an
# alternative, more abstract approach


class RectangularPrism:
    """A rectangular prism"""

    def __init__(self, coordinates):
        (x1, x2, y1, y2, z1, z2) = coordinates
        self.left = x1
        self.right = x2
        self.top = y1
        self.bottom = y2
        self.front = z1
        self.back = z2

    def volume(self):
        return (self.right - self.left + 1) * (self.bottom - self.top + 1) * (self.back - self.front + 1)

    def overlaps(self, other):
        return self.right >= other.left and other.right >= self.left \
               and self.bottom >= other.top and other.bottom >= self.top \
               and self.back >= other.front and other.back >= self.front

    def __repr__(self):
        return f'RectangularPrism(({self.left}, {self.right}, {self.top}, {self.bottom}, {self.front}, {self.back}))'


def should_slice(old_s, old_e, new_s, new_e):
    return old_s < new_s <= old_e, old_s <= new_e < old_e


class Reactor:
    """The submarine's reactor"""

    def __init__(self):
        self.on_regions: list[RectangularPrism] = []

    def set_region(self, state, coordinates):
        new = RectangularPrism(coordinates)
        new_on_regions: list[RectangularPrism] = []
        for old in self.on_regions:
            if old.overlaps(new):
                slice_left, slice_right = should_slice(old.left, old.right, new.left, new.right)
                slice_top, slice_bottom = should_slice(old.top, old.bottom, new.top, new.bottom)
                slice_front, slice_back = should_slice(old.front, old.back, new.front, new.back)
                if slice_left:
                    new_on_regions.append(RectangularPrism((old.left, new.left - 1,
                                                            old.top, old.bottom,
                                                            old.front, old.back)))
                    old.left = new.left
                if slice_right:
                    new_on_regions.append(RectangularPrism((new.right + 1, old.right,
                                                            old.top, old.bottom,
                                                            old.front, old.back)))
                    old.right = new.right
                if slice_top:
                    new_on_regions.append(RectangularPrism((old.left, old.right,
                                                            old.top, new.top - 1,
                                                            old.front, old.back)))
                    old.top = new.top
                if slice_bottom:
                    new_on_regions.append(RectangularPrism((old.left, old.right,
                                                            new.bottom + 1, old.bottom,
                                                            old.front, old.back)))
                    old.bottom = new.bottom
                if slice_front:
                    new_on_regions.append(RectangularPrism((old.left, old.right,
                                                            old.top, old.bottom,
                                                            old.front, new.front - 1)))
                if slice_back:
                    new_on_regions.append(RectangularPrism((old.left, old.right,
                                                            old.top, old.bottom,
                                                            new.back + 1, old.back)))
            else:
                new_on_regions.append(old)
        if state:
            new_on_regions.append(new)
        self.on_regions = new_on_regions

    def count_on(self):
        on_count = 0
        for x in self.on_regions:
            on_count += x.volume()
        return on_count


def reboot(instructions):
    reactor = Reactor()
    for x in instructions:
        reactor.set_region(*x)
    return reactor.count_on()


def test_reboot():
    inputs = (
        parse_file('small_in.txt'),
        parse_file('test_in.txt', True),
        parse_file('test2_in.txt'),
    )
    test_bed(reboot, inputs, (39, 590784, 2758514936282235))


def part_2():
    instructions = parse_file('input.txt')
    on_count = reboot(instructions)
    print(f'{on_count} cubes are on.')


# -------------------------
# Driver
# -------------------------

def main():
    selector = OptionSelector()
    selector.add_option('1', 'Part 1 -- Small initialization', part_1)
    selector.add_option('2', 'Part 2 -- Full reboot', part_2)
    selector.add_option('t1', 'Test 1 -- Small initialization test', test_small_initialization)
    selector.add_option('t2', 'Test 2 -- Full reboot test', test_reboot)
    selector.run()


if __name__ == '__main__':
    main()
