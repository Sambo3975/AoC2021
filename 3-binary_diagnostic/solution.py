def part_1(data):
    gamma_rate = ''
    bits = len(data[0].strip())
    for i in range(bits):
        zeros = 0
        ones = 0
        for x in data:
            if x[i] == '0':
                zeros += 1
            else:
                ones += 1
        if zeros > ones:
            gamma_rate = gamma_rate + '0'
        else:
            gamma_rate = gamma_rate + '1'
    gamma_rate = int(gamma_rate, 2)                  # Most common bit in the corresponding position
    epsilon_rate = ~gamma_rate & int(bits * '1', 2)  # bitwise inverse (truncated to N bits)
    print(f'Γ: {gamma_rate}, E: {epsilon_rate}, Power consumption: {gamma_rate * epsilon_rate}')


def life_support_rating(data, checking_co2=False):
    pos = 0
    while len(data) > 1:  # Repeat until there is only one option
        # Find the most common bit value in the current position
        zeros = 0
        ones = 0
        for x in data:
            if x[pos] == '0':
                zeros += 1
            else:
                ones += 1
        # Determine the bit criteria
        if zeros <= ones:
            criterion = '0' if checking_co2 else '1'
        else:
            criterion = '1' if checking_co2 else '0'
        # Eliminate values that do not meet the bit criteria
        new_data = []
        for x in data:
            if x[pos] == criterion:
                new_data.append(x)
        data = new_data
        pos += 1
    return int(data[0], 2)


def part_2(data):
    o2_rating = life_support_rating(data)
    co2_rating = life_support_rating(data, True)
    print(f'Oxygen generator rating: {o2_rating}')
    print(f'CO2 scrubber rating: {co2_rating}')
    print(f'Life support rating: {o2_rating * co2_rating}')


def main():
    with open('input.txt') as f:
        data = f.readlines()
    part_1(data)
    part_2(data)


if __name__ == '__main__':
    main()
