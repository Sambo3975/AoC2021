from matplotlib import pyplot as plt


def get_fuel_cost_linear(data, pos):
    fuel_cost = 0
    for x in data:
        fuel_cost += abs(x - pos)
    return fuel_cost


def part_1(data):
    # Logically speaking, what we want must be some type of average
    # First, I tried the mean, but it was a too high
    # The median turns out to be the optimal solution
    if len(data) % 2 == 1:
        median = sorted(data)[len(data) // 2]
    else:
        pos = len(data) // 2 - 1
        median = sum(sorted(data)[pos:pos + 2]) // 2
    fuel_cost = 0
    for x in data:
        fuel_cost += abs(x - median)
    print(f'Optimal position for crab subs: {median}. Fuel cost: {fuel_cost}')


def get_fuel_cost_arithmetic(data, pos):
    fuel_cost = 0
    for x in data:
        n = abs(x - pos)
        fuel_cost += n * (n + 1) // 2  # sum of arithmetic series
    return fuel_cost


def part_2(data):
    # Again, we want some type of average, but it's not the median; the mean seems to be the ticket
    # A simple round on the mean doesn't get the correct answer, so we will have to check the floor and the ceiling
    mean_floor = sum(data) // len(data)
    mean_ceil = mean_floor + 1
    means = (mean_floor, mean_ceil)
    costs = [get_fuel_cost_arithmetic(data, x) for x in means]
    optimum = min(costs)
    print(f'Optimal position for crab subs: {means[costs.index(optimum)]}. Fuel cost: {optimum}')


def plot(data):
    xrange = range(min(data), max(data) + 1)
    y1 = [get_fuel_cost_linear(data, x) for x in xrange]
    y2 = [get_fuel_cost_arithmetic(data, x) for x in xrange]
    plt.plot(xrange, y1, label='Linear fuel consumption')
    plt.plot(xrange, y2, label='Arithmetic fuel consumption')
    plt.title('Best Crab Alignment Position')
    plt.legend()
    plt.xlabel('Alignment position')
    plt.ylabel('Fuel cost')
    plt.show()


def main():
    with open('input.txt') as f:
        data = [int(x) for x in f.read().split(',')]
    part_1(data)
    part_2(data)
    match input('Plot the data (y/n) [y]? '):
        case 'n':
            return
        case _:
            plot(data)  # Tuns out this isn't very interesting because the fuel cost for part 2 dwarfs that of part 1


if __name__ == '__main__':
    main()
