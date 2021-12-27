from collections import defaultdict


def get_pos(coord, dd, key):
    x, y = coord
    res = []

    for yoffset in [-1, 0, 1]:
        for xoffset in [-1, 0, 1]:
            tmp = "0"
            if dd[(x + xoffset, y + yoffset)] == "#":
                tmp = "1"
            res.append(tmp)
    pos = int("".join(res), 2)
    return key[pos]


def count(dd: defaultdict):
    count = 0
    for val in dd.values():
        if val == "#":
            count += 1
    return count


key = None
dd = defaultdict(lambda: ".")
with open("1.in") as f:
    key = f.readline().strip()
    f.readline()
    lines = f.readlines()

    y = 0
    for line in lines:
        line = line.strip()

        x = 0
        for char in line:
            dd[(x, y)] = char
            x += 1
        y += 1

    X = x
    Y = y

for i in range(50):
    default = (lambda: "#") if i % 2 == 0 else (lambda: ".")
    new_dd = defaultdict(default)

    for y in range(-1 - i, Y + 2 + i):
        for x in range(-1 - i, X + 2 + i):
            new_dd[(x, y)] = get_pos((x, y), dd, key)

    dd = new_dd

print(count(dd))
