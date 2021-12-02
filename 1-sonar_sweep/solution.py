def part_1(data):
    increase_count = 0
    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            increase_count += 1
    print(f'Increase count: {increase_count}')


def part_2(data):
    increase_count = 0
    sum_prev = sum(data[:3])
    for i in range(1, len(data) - 2):
        sum_cur = sum_prev - data[i - 1] + data[i + 2]
        if sum_cur > sum_prev:
            increase_count += 1
    print(f'Increase count (sliding window): {increase_count}')


def main():
    with open('input.txt') as f:
        data = [int(x) for x in f.readlines()]
    part_1(data)
    part_2(data)


if __name__ == '__main__':
    main()
