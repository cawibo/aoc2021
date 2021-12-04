def transform(brick):
    res = []
    for i in range(5):
        row = brick[i]
        column = [brick[j][i] for j in range(5)]
        res.append(set(row))
        res.append(set(column))

    return res


def has_won(brick, seen):
    for s in brick:
        if len(s.intersection(seen)) == 5:
            return True
    return False


def unmarked(brick):
    unmarked = set()
    for s in brick:
        unmarked |= s - seen
    return sum(unmarked)


with open("1.in") as f:
    numbers = [int(e) for e in f.readline().split(",")]

    bricks = []
    current = []
    for line in f.readlines():
        if line == "\n":
            continue
        current.append([int(e) for e in line.split()])
        if len(current) == 5:
            bricks.append(transform(current))
            current = []

is_first = 1
seen = set()
for number in numbers:
    seen.add(number)

    next_bricks = []
    for brick in bricks:
        if has_won(brick, seen):
            if is_first:
                print("part1", number * unmarked(brick))
                is_first = 0

            if len(bricks) == 1:
                print("part2", number * unmarked(brick))

        else:
            next_bricks.append(brick)

    bricks = next_bricks
