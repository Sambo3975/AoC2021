left_to_right = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}


def part_1(data):
    right_to_score = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    syntax_score = 0
    completion_stacks = []
    for line in data:
        incomplete = True
        bracket_stack = []
        for c in line.strip():
            if c in left_to_right:
                bracket_stack.append(left_to_right[c])
            elif c == bracket_stack[-1]:
                bracket_stack.pop()
            else:
                syntax_score += right_to_score[c]
                incomplete = False
                break
        if incomplete:
            # Might as well collect the data needed for part 2 since we have it
            completion_stacks.append(bracket_stack)

    print(f'Syntax score: {syntax_score}')
    return completion_stacks


def part_2(stax):
    right_to_score = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }

    scores = []
    for x in stax:
        x.reverse()
        score = 0
        for c in x:
            score *= 5
            score += right_to_score[c]
        scores.append(score)
    scores.sort()
    print(f'Autocomplete score: {scores[len(scores) // 2]}')


def main():
    with open('input.txt') as f:
        data = f.readlines()
    stax = part_1(data)
    part_2(stax)


if __name__ == '__main__':
    main()
