def dummy_dijkstra(risk, distance):
    """dijkstra, but it evaluates in order of appearance instead of by distance
    if path goes left or up, reapplication is required."""

    R = len(distance)
    C = len(distance[0])

    for r in range(R):
        for c in range(C):
            current_distance = distance[r][c]

            for roffset in [-1, 0, 1]:
                for coffset in [-1, 0, 1]:

                    if roffset != 0 and coffset != 0:
                        continue  # diagonal exploration not allowed

                    if (  # in bounds
                        0 <= r + roffset
                        and r + roffset < R
                        and 0 <= c + coffset
                        and c + coffset < C
                    ):
                        candidate_distance = distance[r + roffset][c + coffset]
                        candidate_risk = risk[r + roffset][c + coffset]

                        if candidate_distance > current_distance + candidate_risk:
                            distance[r + roffset][c + coffset] = (
                                current_distance + candidate_risk
                            )

    return distance


def solve(risk, iters=1):
    """applies dijkstra {iters} times to a 2d array with equal size to {risk}, using
    elements in {risk} as cost for transitions"""

    distance = [[float("inf") for _ in range(len(risk[0]))] for _ in range(len(risk))]
    distance[0][0] = 0

    for _ in range(iters):
        distance = dummy_dijkstra(risk, distance)

    return distance[-1][-1]


def pretty(grid):
    for row in grid:
        for elem in row:
            print(elem, end=" ")
        print()


def expand(risk, factor=5):
    """expand the risk-grid according to the rules in aoc21-d15-p2 with a factor of {factor}"""

    R = len(risk)
    C = len(risk[0])
    nrisk = [
        [0 for _ in range(len(risk) * factor)] for _ in range(len(risk[0]) * factor)
    ]

    for row in range(R):
        for col in range(C):
            base = risk[row][col]
            for roffset in range(factor):
                for coffset in range(factor):
                    # risk is never zero, and 10 should wrap-around to 1
                    val = ((base + roffset + coffset - 1) % 9) + 1
                    nrisk[row + R * roffset][col + C * coffset] = val

    return nrisk


risk = []
with open("1.in") as f:
    lines = f.read().split("\n")

    risk = [[int(r) for r in line] for line in lines]

print("part1", solve(risk))
risk = expand(risk)
print("part2", solve(risk, iters=6))
