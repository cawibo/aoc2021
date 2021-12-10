# part 1

with open("1.in") as f:
    middle = [[9] + [int(e) for e in line.strip()] + [9] for line in f.readlines()]
    topbottom = [9 for _ in range(len(middle[0]))]
    grid = [topbottom] + middle + [topbottom]

    total_risk = 0
    for row in range(1, len(grid) - 1):
        for col in range(1, len(grid[row]) - 1):
            count = 0
            curr_height = grid[row][col]

            for roffset in [1, -1]:
                if grid[row + roffset][col] > curr_height:
                    count += 1
            for coffset in [1, -1]:
                if grid[row][col + coffset] > curr_height:
                    count += 1

            if count == 4:
                total_risk += 1 + curr_height

    print("part1", total_risk)

# part 2


def make_key(row, col):
    return "{},{}".format(row, col)


def flow(grid, row, col, s):
    s |= set([make_key(row, col)])

    for roffset in [1, -1]:
        if grid[row + roffset][col] != 9 and make_key(row + roffset, col) not in s:
            s |= flow(grid, row + roffset, col, s)

    for coffset in [1, -1]:
        if grid[row][col + coffset] != 9 and make_key(row, col + coffset) not in s:
            s |= flow(grid, row, col + coffset, s)

    return s


with open("1.in") as f:
    middle = [[9] + [int(e) for e in line.strip()] + [9] for line in f.readlines()]
    topbottom = [9 for _ in range(len(middle[0]))]
    grid = [topbottom] + middle + [topbottom]

    s = set()
    b = []

    for row in range(1, len(grid) - 1):
        for col in range(1, len(grid[row]) - 1):
            current = grid[row][col]
            if make_key(row, col) not in s and current != 9:
                current_basin = flow(grid, row, col, set())
                b.append(len(current_basin))
                s |= current_basin

    product = 1
    for be in sorted(b)[-3:]:
        product *= be

    print("part2", product)
