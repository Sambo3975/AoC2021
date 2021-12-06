def simulate_lanternfish(data, days, days_before=0):
    assert days >= 0 and days >= days_before, 'Cannot run simulation backward.'
    for _ in range(days - days_before):
        zeros = data[0]
        for i in range(8):
            data[i] = data[i + 1]
        data[6] += zeros
        data[8] = zeros
    print(f'{sum(data)} fish after {days} days.')


def part_1(data):
    simulate_lanternfish(data, 80)


def part_2(data):
    simulate_lanternfish(data, 256, 80)  # Setting it up this way allows us to avoid doing the same work twice.


def main():
    with open('input.txt') as f:
        data = [int(x) for x in f.read().split(',')]
    fish = [0] * 9
    for x in data:
        fish[x] += 1
    print(f'Starting population: {len(data)} fish')
    part_1(fish)
    part_2(fish)


if __name__ == '__main__':
    main()
