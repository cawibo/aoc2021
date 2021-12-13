folds = []
coords = set()
with open("1.in") as f:
    for line in f.readlines():
        if line and line.startswith("fold"):
            xoy, k = line.split()[2].split("=")
            folds.append((xoy, int(k)))

        elif line.strip() != "":
            x, y = [int(e) for e in line.strip().split(",")]
            coords.add((x, y))


PART1 = True
for f in folds:
    new_coords = set()
    m = f[1]

    if f[0] == "x":
        for (x, y) in coords:
            nx = x if x < m else 2 * m - x
            new_coords.add((nx, y))

    elif f[0] == "y":
        for (x, y) in coords:
            ny = y if y < m else 2 * m - y
            new_coords.add((x, ny))

    coords = new_coords
    if PART1:
        print(len(coords))
        PART1 = False

R = max([e[1] for e in coords]) + 1
C = max([e[0] for e in coords]) + 1

for r in range(R):
    for c in range(C):
        if (c, r) in coords:
            print("#", end=" ")
        else:
            print(".", end=" ")
    print()
