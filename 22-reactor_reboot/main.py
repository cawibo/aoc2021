from collections import defaultdict
from itertools import product


def parse_range(string: str):
    _, rnge = string.split("=")
    lower, higher = [int(e) for e in rnge.split("..")]

    lower = max(lower, -60)
    higher = min(higher, 60)

    return lower, higher


def parse(filename):
    result = []
    with open(filename) as f:
        for line in f.readlines():
            command, ranges = line.split(" ")
            parsed_ranges = [e for e in map(parse_range, ranges.split(","))]
            result.append([command] + parsed_ranges)
    return result


def cube(xs, ys, zs):
    return product(
        range(xs[0], xs[1] + 1), range(ys[0], ys[1] + 1), range(zs[0], zs[1] + 1)
    )


def action(command, xs, ys, zs, dd: defaultdict):
    value = 1 if command == "on" else 0

    for x, y, z in cube(xs, ys, zs):
        dd[(x, y, z)] = value

    return dd


dd = defaultdict(lambda: 0)
for instruction in parse("1.in"):
    command, xs, ys, zs = instruction
    dd = action(command, xs, ys, zs, dd)

print(sum(dd.values()))
