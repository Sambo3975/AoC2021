def part_1(data):
    distance = 0
    depth = 0
    for line in data:
        params = line.strip().split()
        params[1] = int(params[1])
        match params[0]:
            case 'forward':
                distance += params[1]
            case 'down':
                depth += params[1]
            case 'up':
                depth -= params[1]
    print(f'Reached distance {distance} and depth {depth} (product: {distance * depth})')


def part_2(data):
    aim = 0
    distance = 0
    depth = 0
    for line in data:
        params = line.strip().split()
        params[1] = int(params[1])
        match params[0]:
            case 'forward':
                distance += params[1]
                depth += aim * params[1]
            case 'down':
                aim += params[1]
            case 'up':
                aim -= params[1]
    print(f'Reached distance {distance} and depth {depth} (product: {distance * depth})')


def main():
    with open('input.txt') as f:
        data = f.readlines()
    part_1(data)
    part_2(data)


if __name__ == '__main__':
    main()
