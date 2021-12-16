from option_selection import OptionSelector
from packet_decoder import PacketDecoder


def parse_file(file_name):
    parse_tree, leftovers = PacketDecoder.parse_file(file_name)
    print(parse_tree)
    print(f'Leftover bits: {leftovers}')


def version_sum_tree(tree, version_sum=0):
    for sub_packet in tree:
        version_sum += sub_packet['version']
        if 'sub-packets' in sub_packet:
            version_sum = version_sum_tree(sub_packet['sub-packets'], version_sum)
    return version_sum


def version_sum_str(string):
    parse_tree, _ = PacketDecoder.parse(string)
    version_sum = version_sum_tree(parse_tree)
    print(f'Sum of versions: {version_sum}')


def version_sum_file(file_name):
    parse_tree, _ = PacketDecoder.parse_file(file_name)
    version_sum = version_sum_tree(parse_tree)
    print(f'Sum of versions: {version_sum}')


def decode_str(string):
    value = PacketDecoder.decode(string)
    print(f'Packet decodes to {value}')


def decode_file(file_name):
    value = PacketDecoder.decode_file(file_name)
    print(f'Packet decodes to {value}')


def part_1():
    version_sum_file('input.txt')


def part_2():
    decode_file('input.txt')


def test_1():
    parse_file('test.txt')


def test_2():
    parse_file('test2.txt')


def test_3():
    parse_file('test3.txt')


def test_4():
    with open('test4.txt') as f:
        for line in f.readlines():
            version_sum_str(line.strip())


def test_5():
    with open('test5.txt') as f:
        for line in f.readlines():
            decode_str(line.strip())


def main():
    selector = OptionSelector(timed=True)
    selector.add_option('1', 'Version sum', part_1)
    selector.add_option('2', 'Full decode', part_2)
    selector.add_option('t1', 'Literal parse test', test_1)
    selector.add_option('t2', 'Length-based operator parse test', test_2)
    selector.add_option('t3', 'Count-based operator parse test', test_3)
    selector.add_option('t4', 'Version sum tests', test_4)
    selector.add_option('t5', 'Packet decode tests', test_5)
    selector.run()


if __name__ == '__main__':
    main()
