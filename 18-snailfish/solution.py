from ast import literal_eval
from math import floor, ceil

import load_file
from colorama import Fore, Style

from option_selection import OptionSelector

# -----------------------
# Core Functionality
# -----------------------
from testing import test_bed


class Node:
    __node_ct = 0

    def __init__(self, children: list, parent=None):
        """
        CONSTRUCTOR
        :param children: Node's children. May contain any data type, including other Nodes. If a list is contained, a
        child Node will be created with its contents. This means that leaves on the tree may not be lists
        :param parent: Node's parent.
        """
        self.parent = parent
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1

        left = children[0]
        if type(left) == list:
            self.left = Node(left, self)
        else:
            self.left = left
            if isinstance(self.left, Node):
                self.left.parent = self
                self.left.increase_depth()

        right = children[1]
        if type(right) == list:
            self.right = Node(right, self)
        else:
            self.right = right
            if isinstance(self.right, Node):
                self.right.parent = self
                self.right.increase_depth()

        self.id = Node.__node_ct
        Node.__node_ct += 1

    def __repr__(self):
        return f'[{repr(self.left)},{repr(self.right)}]'

    def __eq__(self, other):
        return repr(self) == repr(other)

    def increase_depth(self):
        self.depth += 1
        if isinstance(self.left, Node):
            self.left.increase_depth()
        if isinstance(self.right, Node):
            self.right.increase_depth()


def inorder(node: Node, result: list = None):
    if result is None:
        result = []
    added_this = False
    if type(node.left) == int:
        result.append(node)
        added_this = True
    else:
        result = inorder(node.left, result)

    if type(node.right) == int:
        if not added_this:
            result.append(node)
    else:
        result = inorder(node.right, result)

    return result


def load_as_tree(file_name):
    data = load_file.as_literals(file_name)
    return Node(data[0])


NodeField = tuple[Node, bool]


def is_int(obj):
    return type(obj) == int


def mark_for_explode(root: Node):
    ordered = inorder(root)
    to_left: NodeField | None = None
    to_right: NodeField | None = None
    for i in range(len(ordered)):
        node = ordered[i]
        if node.depth >= 4 and is_int(node.left) and is_int(node.right):
            exploding = node
            if i > 0:
                marked_node = ordered[i - 1]
                to_left = (marked_node, is_int(marked_node.right))
            if i < len(ordered) - 1:
                marked_node = ordered[i + 1]
                to_right = (marked_node, not is_int(marked_node.left))
            return to_left, exploding, to_right

    return None


def foreshadow_explosion(root: Node | int, to_left: NodeField, exploding: Node, to_right: NodeField):
    if is_int(root):
        return str(root)
    if root is exploding:
        return f'[{Fore.RED + str(root.left) + Style.RESET_ALL},{Fore.YELLOW + str(root.right) + Style.RESET_ALL}]'
    for node_field, color in zip((to_left, to_right), (Fore.GREEN, Fore.BLUE)):
        if node_field is None:
            continue
        (marked_node, right_child) = node_field
        if root is marked_node:
            if not right_child:
                left = color + str(root.left) + Style.RESET_ALL
                right = foreshadow_explosion(root.right, to_left, exploding, to_right)
            else:
                left = foreshadow_explosion(root.left, to_left, exploding, to_right)
                right = color + str(root.right) + Style.RESET_ALL
            return f'[{left},{right}]'
    return f'[{foreshadow_explosion(root.left, to_left, exploding, to_right)},' \
           f'{foreshadow_explosion(root.right, to_left, exploding, to_right)}]'


def explode(to_left: NodeField, exploding: Node, to_right: NodeField):
    for node_field, explode_value in zip((to_left, to_right), (exploding.left, exploding.right)):
        if node_field is None:
            continue
        (node, right_child) = node_field
        if right_child:
            node.right += explode_value
        else:
            node.left += explode_value
    parent = exploding.parent
    if parent.left is exploding:
        parent.left = 0
        return parent, False
    elif parent.right is exploding:
        parent.right = 0
        return parent, True


def review_explosion(root: Node, to_left: NodeField, replacement: NodeField, to_right: NodeField):
    if is_int(root):
        return str(root)
    (replacement_node, right_child) = replacement
    if root is replacement_node:
        if right_child:
            if is_int(root.left):
                left = Fore.GREEN + str(root.left) + Style.RESET_ALL
            else:
                left = review_explosion(root.left, to_left, replacement, to_right)
            right = Fore.CYAN + str(root.right) + Style.RESET_ALL
        else:
            left = Fore.CYAN + str(root.left) + Style.RESET_ALL
            if is_int(root.right):
                right = Fore.BLUE + str(root.right) + Style.RESET_ALL
            else:
                right = review_explosion(root.right, to_left, replacement, to_right)
        return f'[{left},{right}]'
    for node_field, color in zip((to_left, to_right), (Fore.GREEN, Fore.BLUE)):
        if node_field is None:
            continue
        (marked_node, right_child) = node_field
        if root is marked_node:
            if not right_child:
                left = color + str(root.left) + Style.RESET_ALL
                right = review_explosion(root.right, to_left, replacement, to_right)
            else:
                left = review_explosion(root.left, to_left, replacement, to_right)
                right = color + str(root.right) + Style.RESET_ALL
            return f'[{left},{right}]'
    return f'[{review_explosion(root.left, to_left, replacement, to_right)},' \
           f'{review_explosion(root.right, to_left, replacement, to_right)}]'


def foreshadow_split(root: Node, splitting: NodeField):
    if is_int(root):
        return str(root)
    (node, right_child) = splitting
    if root is node:
        if right_child:
            left = foreshadow_split(root.left, splitting)
            right = Fore.BLACK + str(root.right) + Style.RESET_ALL
        else:
            left = Fore.BLACK + str(root.left) + Style.RESET_ALL
            right = foreshadow_split(root.right, splitting)
        return f'[{left},{right}]'
    return f'[{foreshadow_split(root.left, splitting)},{foreshadow_split(root.right, splitting)}]'


def split(root: Node, debug: bool = False, original_root=None, steps=0):
    if is_int(root):
        return None
    if debug and original_root is None:
        original_root = root
    if is_int(root.left) and root.left > 9:
        if debug:
            print(f'{steps}: Splitting:')
            print(foreshadow_split(original_root, (root, False)))
        root.left = Node([floor(half := root.left / 2), ceil(half)], root)
        return root.left
    if new_node := split(root.left, debug, original_root):
        return new_node
    if is_int(root.right) and root.right > 9:
        if debug:
            print(f'{steps}: Splitting:')
            print(foreshadow_split(original_root, (root, True)))
        root.right = Node([floor(half := root.right / 2), ceil(half)], root)
        return root.right
    return split(root.right, debug, original_root)


def review_split(root: Node, new_node: Node):
    if is_int(root):
        return root
    if root is new_node:
        return Fore.BLACK + str(root) + Style.RESET_ALL
    return f'[{review_split(root.left, new_node)},{review_split(root.right, new_node)}]'


def reduce(root: Node, debug: bool = False):
    steps = 0
    while True:
        steps += 1
        explode_params = mark_for_explode(root)
        if explode_params is not None:
            if debug:
                print(f'{steps}: Exploding:')
                print(foreshadow_explosion(root, *explode_params))
            replacement = explode(*explode_params)
            if debug:
                print(review_explosion(root, explode_params[0], replacement, explode_params[2]))
            continue
        new_node = split(root, debug, steps=steps)
        if new_node is not None:
            if debug:
                print(review_split(root, new_node))
            continue
        else:
            return root


def add(lhs: Node, rhs: Node, debug: bool = False):
    return reduce(Node([lhs, rhs]), debug)


def sum_snailfish_numbers(numbers: list[Node], debug: bool = False):
    res = numbers[0]
    for x in numbers[1:]:
        res = add(res, x, debug)
    return res


def magnitude(root):
    if isinstance(root.left, Node):
        left = magnitude(root.left)
    else:
        left = root.left

    if isinstance(root.right, Node):
        right = magnitude(root.right)
    else:
        right = root.right

    return 3 * left + 2 * right


def do_homework(numbers):
    result = sum_snailfish_numbers(numbers)
    return magnitude(result)


def largest_magnitude_sum(numbers):
    largest_magnitude = 0
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i != j:
                ni = Node(numbers[i])
                nj = Node(numbers[j])
                largest_magnitude = max(largest_magnitude, magnitude(sum_snailfish_numbers([ni, nj])))

    return largest_magnitude


# -----------------------
# Puzzle Solutions
# -----------------------


def part_1():
    magnitude_of_sum = do_homework([Node(x) for x in load_file.as_literals('input.txt')])
    print(f'Magnitude of final sum: {magnitude_of_sum}')


def part_2():
    largest_sum = largest_magnitude_sum(load_file.as_literals('input.txt'))
    print(f'Largest magnitude: {largest_sum}')


# -----------------------
# Tests
# -----------------------


def test_inorder():
    node = load_as_tree('explode_in.txt')
    ordered = inorder(node)
    for x in ordered:
        print(x)


def test_explode():
    inputs = [Node(x) for x in load_file.as_literals('explode_in.txt')]
    before: list[str] = []
    after: list[str] = []
    for x in inputs:
        explode_params = mark_for_explode(x)
        if explode_params is not None:
            before.append(foreshadow_explosion(x, *explode_params))
            replacement = explode(*explode_params)
            after.append(review_explosion(x, explode_params[0], replacement, explode_params[2]))
        else:
            before.append(str(x))
            after.append(str(x))
    for b, a in zip(before, after):
        print(b)
        print(a)
        print()


def test_reduce():
    inputs = [Node(x) for x in load_file.as_literals('reduce_in.txt')]
    sum_snailfish_numbers(inputs, True)


def trace(inputs: list[str], outputs: list[str], test_number: int):
    numbers = [Node(literal_eval(x)) for x in inputs[test_number].strip().split()]
    expected_result = Node(literal_eval(outputs[test_number].strip()))
    sum_snailfish_numbers(numbers, True)
    print(f'Expected:\n{expected_result}')


def test_sums():
    with open('sum_in.txt') as f:
        inputs = [[Node(literal_eval(x)) for x in y.strip().split()] for y in f.read().split('\n\n')]
    with open('sum_out.txt') as f:
        outputs = [Node(literal_eval(x.strip())) for x in f.read().split('\n\n')]

    test_bed(sum_snailfish_numbers, inputs, outputs, trace)


def test_splitting_order():
    root = Node(literal_eval('[[[[7,7],[7,8]],[[7,7],[0,8]]],[[[14,0],13],[8,7]]]'))
    new_node = split(root, True)
    print(review_split(root, new_node))


def test_magnitudes():
    inputs = [Node(x) for x in load_file.as_literals('magnitude_in.txt')]
    outputs = load_file.as_literals('magnitude_out.txt')
    test_bed(magnitude, inputs, outputs)


def test_sample_problem():
    inputs = [Node(x) for x in load_file.as_literals('test_in.txt')]
    outputs = load_file.as_literals('test_out.txt')
    test_bed(do_homework, [inputs], outputs)


def test_largest_sum():
    inputs = load_file.as_literals('test_in.txt')
    test_bed(largest_magnitude_sum, [inputs], [3993])


# -----------------------
# Driver
# -----------------------


def main():
    selector = OptionSelector()
    selector.add_option('1', 'Part 1 -- Snailfish homework', part_1)
    selector.add_option('2', 'Part 2 -- Largest magnitude sum', part_2)
    selector.add_option('t1', 'Inorder traversal test', test_inorder)
    selector.add_option('t2', 'Explode tests', test_explode)
    selector.add_option('t3', 'Reduction test', test_reduce)
    selector.add_option('t4', 'Sum test', test_sums)
    selector.add_option('t5', 'Splitting order test', test_splitting_order)
    selector.add_option('t6', 'Magnitude tests', test_magnitudes)
    selector.add_option('t7', 'Sample Homework Assignment', test_sample_problem)
    selector.add_option('t8', 'Largest magnitude sum test', test_largest_sum)
    selector.run()


if __name__ == '__main__':
    main()
