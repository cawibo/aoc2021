from collections import defaultdict
from itertools import product


def parse_range(string: str):
    _, rnge = string.split("=")
    lower, higher = [int(e) for e in rnge.split("..")]

    return lower, higher


def parse(filename):
    result = []
    with open(filename) as f:
        for line in f.readlines():
            command, ranges = line.split(" ")
            parsed_ranges = [e for e in map(parse_range, ranges.split(","))]
            result.append([command] + parsed_ranges)
    return result


def in_bounds_1(x, xs):
    return xs[0] <= x <= xs[1]


def in_bounds_3(point, xs, ys, zs):
    x, y, z = point
    return xs[0] <= x <= xs[1] and ys[0] <= y <= ys[1] and zs[0] <= z <= zs[1]


instructions = parse("1.in")

XS = []
YS = []
ZS = []

for instruction in instructions:
    _, (x1, x2), (y1, y2), (z1, z2) = instruction
    XS.extend([x1, x2 + 1])
    YS.extend([y1, y2 + 1])
    ZS.extend([z1, z2 + 1])

XS.sort()
YS.sort()
ZS.sort()

# dd = defaultdict(lambda: False)
S = set()

remaining = len(instructions)
for instruction in instructions:
    print(remaining, "left; currently at:", instruction)
    remaining -= 1
    command, xs, ys, zs = instruction

    minXS = [x for x in XS if in_bounds_1(x, xs)]
    minYS = [y for y in YS if in_bounds_1(y, ys)]
    minZS = [z for z in ZS if in_bounds_1(z, zs)]
    for point in product(minXS, minYS, minZS):
        if in_bounds_3(point, xs, ys, zs):
            if command == "on":
                S.add(point)
            else:
                if point in S:
                    S.remove(point)

total = 0
for i, ei in enumerate(XS[:-1]):
    print(len(XS) - i)
    for j, ej in enumerate(YS[:-1]):
        for k, ek in enumerate(ZS[:-1]):
            if (ei, ej, ek) in S:
                x = XS[i + 1] - ei
                y = YS[j + 1] - ej
                z = ZS[k + 1] - ek
                total += x * y * z


print(total)
