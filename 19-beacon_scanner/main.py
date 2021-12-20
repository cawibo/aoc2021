import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy.spatial.distance import cdist


def parse(filename):
    scanners = []
    with open(filename) as f:
        scanner = []
        for line in f.readlines():
            line = line.strip()
            if not line and scanner:
                scanners.append(scanner)
            elif line.startswith("---"):
                scanner = []
            elif line:
                coord = np.array([int(e) for e in line.split(",")])
                scanner.append(coord)
        scanners.append(scanner)  # append last scanner
    return scanners


def rotate_about_x(coordinate, quarters=1):
    r = R.from_rotvec(quarters * 90 * np.array([1, 0, 0]), degrees=True)
    return r.apply(coordinate)


def rotate_about_y(coordinate, quarters=1):
    r = R.from_rotvec(quarters * 90 * np.array([0, 1, 0]), degrees=True)
    return r.apply(coordinate)


def rotate_about_z(coordinate, quarters=1):
    r = R.from_rotvec(quarters * 90 * np.array([0, 0, 1]), degrees=True)
    return r.apply(coordinate)


def orientations(beacons, beacon):
    for x in range(4):
        for y in range(4):
            for z in range(4):
                x_beacons = rotate_about_x(beacons, x)
                x_scanner = rotate_about_x(beacon, x)
                xy_beacons = rotate_about_y(x_beacons, y)
                xy_scanner = rotate_about_y(x_scanner, y)
                xyz_beacons = rotate_about_z(xy_beacons, z)
                xyz_scanner = rotate_about_z(xy_scanner, z)
                yield xyz_beacons, xyz_scanner


def as_set(scanner):
    return set([str(b) for b in np.rint(scanner)])


def all_distances(beacon, beacons):
    return cdist([beacon], beacons, "euclidean")[0]


def find_beacon_pair(scanner_a, scanner_b):
    for beacon_a in scanner_a:
        a_distance = all_distances(beacon_a, scanner_a)
        a_distance_set = as_set(a_distance)
        for beacon_b in scanner_b:
            b_distance = all_distances(beacon_b, scanner_b)
            b_distance_set = as_set(b_distance)

            intersection = a_distance_set & b_distance_set
            if len(intersection) >= 12:  # they are the same beacon
                print("found a beacon-pair")
                return beacon_a, beacon_b


from queue import Queue


def queue_up(lst):
    q = Queue()
    [q.put(elem) for elem in lst]
    return q


def find_correct_orientation(pair, base, beacons):
    print("pair", pair)
    base_beacon, beacon = pair
    base_set = as_set(base - base_beacon)

    translated_beacons = beacons - beacon
    for oriented_beacons, oriented_scanner in orientations(translated_beacons, -beacon):
        intersection = as_set(oriented_beacons) & base_set
        if len(intersection) >= 12:
            return oriented_beacons, oriented_scanner


def solve(scanners):
    q = queue_up(scanners)

    res = set()
    base = None
    relative_scanners = None
    while not q.empty():
        print(q.qsize())
        beacons = q.get()
        if base is None:
            base = np.array(beacons)
            res |= as_set(beacons)
            relative_scanners = np.array([[0, 0, 0]])
            continue

        pair = find_beacon_pair(base, beacons)
        if pair is None:
            print("pair is None")
            q.put(beacons)
        else:
            oriented_beacons, oriented_scanner = find_correct_orientation(
                pair, base, beacons
            )
            if oriented_beacons is None:
                print("oriented_beacons is None")
                q.put(beacons)
                continue

            base_beacon, _ = pair
            translated_beacons = oriented_beacons + base_beacon

            base = np.append(base, np.array(translated_beacons), axis=0)
            res |= as_set(translated_beacons)

            translated_scanner = oriented_scanner + base_beacon
            relative_scanners = np.append(
                relative_scanners, [translated_scanner], axis=0
            )

    print(len(res))
    highest = 0
    for a in relative_scanners:
        for b in relative_scanners:
            manhattan = sum(abs(e1 - e2) for e1, e2 in zip(a, b))
            highest = max(highest, manhattan)
    print(highest)


scanners = parse("1.in")

solve(scanners)
