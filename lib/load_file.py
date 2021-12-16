def as_digit_grid(file_name):
    with open(file_name) as f:
        return [[int(y) for y in x.strip()] for x in f.readlines()]
