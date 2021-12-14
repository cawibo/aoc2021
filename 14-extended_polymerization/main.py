from collections import Counter


def step(cp):
    ncp = Counter()  # new pairs counter
    ncs = Counter()  # new singles counter

    for p in cp:
        count = cp[p]  # how many are there?
        insert = T[p]  # what should be inserted?
        ncp[p[0] + insert] += count  # add the "left" pair
        ncp[insert + p[1]] += count  # add the "right" pair
        ncs[insert] += count  # add the inserted character to singles counter

    return ncp, ncs


def current_difference(cs):
    # extract the counter values in a sorted list; None to get all
    counts = Counter(cs).most_common(None)

    most_common = counts[0][1]
    least_common = counts[-1][1]

    return most_common - least_common


# parse input
with open("1.in") as f:
    # initialize starting string and counter structures
    s = f.readline().strip()
    cs = Counter(s)  # counter for singles
    cp = Counter()  # counter for pairs
    for i in range(len(s) - 1):
        key = s[i : i + 2]
        cp[key] += 1

    f.readline()  # empty line

    # insertion rules
    T = {}
    for line in f.readlines():
        frm, to = line.split(" -> ")
        T[frm] = to.strip()


N = 40
for i in range(1, N + 1):
    cp, ncs = step(cp)  # execute a "step"
    cs += ncs  # add the new singles counter to the base one

    if i == 10:
        print("part1:", current_difference(cs))
    if i == 40:
        print("part2:", current_difference(cs))

print("res:", current_difference(cs))
