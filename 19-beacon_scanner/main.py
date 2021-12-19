from math import sqrt


def parse():
    scanners = []
    with open("ex.in") as f:
        scanner = []
        for line in f.readlines():
            line = line.strip()
            if not line and scanner:
                scanners.append(scanner)
            elif line.startswith("---"):
                scanner = []
            elif line:
                coord = tuple([int(e) for e in line.split(",")])
                scanner.append(coord)
        scanners.append(scanner)  # last scanner

    return scanners


def pow2(n):
    return n ** 2


def distance(*coord):
    return sqrt(sum(map(pow2, *coord)))


def sufficiently_equal(this, that):
    assert this >= 0 and that >= 0
    acceptable_diff = 10e-2
    return abs(this - that) <= acceptable_diff


def possible_neighbours(scanner_a, scanner_b):
    for beacon_a in scanner_a:
        for beacon_b in scanner_b:
            distance_a = distance(beacon_a)
            distance_b = distance(beacon_b)
            if sufficiently_equal(distance_a, distance_b):
                print(distance_a, distance_b)
                print("sufficiently equal:", beacon_a, beacon_b)
                return beacon_a
    return None


def rotate_axes(coord, by=None):
    if by is None:
        by = 1
    for _ in range(by):
        coord = coord[1:] + tuple([coord[0]])
    return coord


from itertools import product


def arrangements():
    for rot in range(3):
        for a in product([1, -1], repeat=3):
            yield (a, rot)


def add(offset, coord):
    return tuple([sum(e) for e in zip(offset, coord)])


def arrange(coefficients, coord):
    return tuple([coefficient * val for coefficient, val in zip(coefficients, coord)])


def add_relative(offset, beacons):
    return tuple([add(offset, coord) for coord in beacons])


def as_set(scanner):
    result = set()
    for coord in scanner:  # todo rewrite
        result.add(tuple((coord)))
    return result


from itertools import permutations


def apply_arrangement(scanner, arrangement):
    arranged_scanner = []
    coefficients, rot = arrangement
    for coord in scanner:
        # coord = rotate_axes(coord, by=rot)
        coord = arrange(coefficients, coord)
        for p in permutations(coord, 3):
            arranged_scanner.append(p)
    return arranged_scanner


from copy import deepcopy


def at_least_12(base: set, offset, scanner):
    for arrangement in arrangements():
        scanner_local = deepcopy(scanner)
        arranged_scanner = apply_arrangement(scanner_local, arrangement)
        translated_arranged_scanner = add_relative(offset, arranged_scanner)

        scanner_set = as_set(translated_arranged_scanner)
        print(offset in scanner_set)
        intersection = len(base.intersection(scanner_set))
        # print(scanner_set)
        print("intersection", intersection)
        if intersection >= 12:
            print("intersection", intersection)
            return scanner_set


scanners = parse()

# base = as_set(scanners[0])
# print(at_least_12(base, scanners[1]))
# print(at_least_12(base, scanners[2]))
# print(at_least_12(base, scanners[3]))

from queue import Queue

q = Queue()
for scanner in scanners:
    q.put(scanner)

base = set()
while not q.empty():
    scanner = q.get()
    if not base:  # first scanner
        base |= as_set(scanner)
    else:
        print("hej", q.qsize())
        # if offset := possible_neighbours(base, scanner):
        pn = possible_neighbours(base, scanner)
        if pn:
            print("offset", offset)
            res = at_least_12(base, offset, scanner)
            print("res", res)
            if res is not None:
                print("Hejsan")
                import sys

                sys.exit(0)


# for i, ie in enumerate(scanners):
#     for j, je in enumerate(scanners):
#         if i == j:
#             continue

#         if (offset := possible_neighbours(ie, je)) is not None:
#             base = as_set(ie)
#             print("offset", offset)

#             res = at_least_12(base, offset, je)
#             print("res", res)


assert rotate_axes((1, 2, 3)) == ((2, 3, 1))
assert rotate_axes((1, 2, 3), by=2) == ((3, 1, 2))
assert rotate_axes((1, 2, 3), by=3) == ((1, 2, 3))

assert add((1, 2, 3), (1, 2, 3)) == (2, 4, 6)
assert add((2, 2, 2), (1, 1, 1)) == (3, 3, 3)

# for arrangement in arrangements():
#     print(apply_arrangment([[1, 2, 3]], arrangement))
