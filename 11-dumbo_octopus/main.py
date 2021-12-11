from queue import Queue


def get_surrounding(grid, row, col):
    """Returns an array of all valid coordinates around the input row,col

    Each coordinate (or element of the list) is a string with the format: '{row},{col}'."""

    res = []

    for roffset in [-1, 0, 1]:
        for coffset in [-1, 0, 1]:

            # ignore coordinates that are out of bounds for the input grid
            if row + roffset < 0 or col + coffset < 0:
                continue
            if row + roffset >= len(grid) or col + coffset >= len(grid[0]):
                continue

            res.append("{},{}".format(row + roffset, col + coffset))

    return res


def step(grid):
    """Returns a new grid that is 'one step' ahead of the input grid and
    the number of flashes that have occurred during this step."""

    flashes = 0
    q = Queue()

    # update the entire grid by increasing each octopus' energy level by one
    for row in range(len(grid)):
        for col in range(len(grid[0])):

            # an octopi that flashes (reaches 10) should be reset to 0
            # and all of its surrounding octopi should be added to a q
            # for additional energy updates (this step).
            if grid[row][col] == 9:

                # add all surrounding octopi to queue
                surrounding = get_surrounding(grid, row, col)
                for e in surrounding:
                    q.put(e)
                grid[row][col] = 0

                # when an octopus flashes, increase the counter by one
                flashes += 1

            # otherwise, increase energy level by one
            else:
                grid[row][col] += 1

    # repeat the process until energy levels are stable and
    # no more octopi are flashing.
    while not q.empty():
        row, col = [int(e) for e in q.get().split(",")]

        if grid[row][col] == 9:

            surrounding = get_surrounding(grid, row, col)
            for e in surrounding:
                q.put(e)
            grid[row][col] = 0

            flashes += 1

        # octopi that have already flashed (during a step) cannot
        # increase their energy level above 0 for the remainder of
        # that step.
        elif grid[row][col] != 0:

            grid[row][col] += 1

    return grid, flashes


def all_0(grid):
    """Returns True if all energy levels in the input grid are 0,
    otherwise it returns False."""

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] != 0:
                return False

    return True


def solve1(grid):
    """Solves part 1 of aoc21 day 11.
    How many flashes are there in the first 100 steps?"""

    total_flashes = 0

    for _ in range(100):
        grid, flashes = step(grid)
        total_flashes += flashes

    return total_flashes


def solve2(grid):
    """Solves part 2 of aoc21 day 11.
    After how many iterations (steps) is the whole grid 0?"""

    for i in range(1, 1000):
        grid, _ = step(grid)

        if all_0(grid):
            return i

    return -1


string = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

grid = [[int(e) for e in line] for line in string.split("\n")]
print(solve1(grid))
grid = [[int(e) for e in line] for line in string.split("\n")]
print(solve2(grid))
