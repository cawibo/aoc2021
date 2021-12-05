def parse(line):
    frm, to = line.split(" -> ")
    return [int(e) for e in frm.split(",") + to.split(",")]


def get_path(x1, y1, x2, y2, part1=False):
    if x1 == x2:
        return ["{}, {}".format(x1, min(y1, y2) + y) for y in range(abs(y1 - y2) + 1)]
    if y1 == y2:
        return ["{}, {}".format(min(x1, x2) + x, y1) for x in range(abs(x1 - x2) + 1)]

    if part1:
        return []

    # diagonals
    if x1 < x2 and y1 < y2:
        return ["{}, {}".format(x1 + o, y1 + o) for o in range(abs(x1 - x2) + 1)]
    if x1 < x2 and y1 > y2:
        return ["{}, {}".format(x1 + o, y1 - o) for o in range(abs(x1 - x2) + 1)]
    if x1 > x2 and y1 < y2:
        return ["{}, {}".format(x1 - o, y1 + o) for o in range(abs(x1 - x2) + 1)]
    if x1 > x2 and y1 > y2:
        return ["{}, {}".format(x2 + o, y2 + o) for o in range(abs(x1 - x2) + 1)]

    return []


def pretty(double, seen, dim=10):
    for i in range(dim):
        for j in range(dim):
            key = "{}, {}".format(j, i)
            if key in double:
                print("d", end=" ")
            elif key in seen:
                print("s", end=" ")
            else:
                print(".", end=" ")
        print()


def solve(paths):
    double = set()
    seen = set()

    for path in paths:
        for coord in path:
            if coord in seen:
                double.add(coord)
            seen.add(coord)

    # pretty(double, seen)
    return len(double)


with open("1.in") as f:
    res = solve([get_path(*parse(line), part1=True) for line in f.readlines()])

    print(res)
