def step(pos, vel):
    x, y = pos
    vx, vy = vel

    # update
    x += vx
    y += vy

    # drag
    if vx != 0:
        if vx > 0:
            vx -= 1
        else:
            vx += 1

    # gravity
    vy -= 1

    return (x, y), (vx, vy)


def hit(pos, target):
    x, y = pos
    tx, ty = target

    return min(tx) <= x and x <= max(tx) and min(ty) <= y and y <= max(ty)


def miss(pos, target):
    x, y = pos
    tx, ty = target

    return max(tx) < x or y < min(ty)


def parse(text):
    text = text.strip("target area: ")
    xs, ys = text.split(", ")

    return [
        [int(e) for e in xs.strip("x=").split("..")],
        [int(e) for e in ys.strip("y=").split("..")],
    ]


target = parse("target area: x=244..303, y=-91..-54")

max_height_all = -float("inf")
hit_counter = 0

# all x are positive in problem set
X = max([abs(e) for e in target[0]])
# ys can be either positive or negative
Y = max([abs(e) for e in target[1]])
for ivx in range(X + 1):
    for ivy in range(-Y, Y):
        pos = [0, 0]
        vel = (ivx, ivy)
        max_height_current = -float("inf")

        while not miss(pos, target):
            max_height_current = max(max_height_current, pos[1])
            pos, vel = step(pos, vel)

            if hit(pos, target):
                max_height_all = max(max_height_all, max_height_current)
                hit_counter += 1
                break

print("part1", max_height_all)
print("part2", hit_counter)
