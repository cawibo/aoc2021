from queue import Queue

ex = """4658137637
3277874355
4525611183
3128125888
8734832838
4175463257
8321423552
4832145253
8286834851
4885323138"""

grid = [[int(e) for e in line] for line in ex.split("\n")]


def get_surrounding(grid, row, col):
    res = []
    for roffset in [-1, 0, 1]:
        for coffset in [-1, 0, 1]:
            if row + roffset < 0 or col + coffset < 0:
                continue
            if row + roffset >= len(grid) or col + coffset >= len(grid[0]):
                continue
            res.append("{},{}".format(row + roffset, col + coffset))

    return res


flashes = 0


def step(grid):
    global flashes
    q = Queue()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 9:
                surrounding = get_surrounding(grid, row, col)
                for e in surrounding:
                    q.put(e)
                grid[row][col] = 0
                flashes += 1
            else:
                grid[row][col] += 1

    while not q.empty():
        row, col = [int(e) for e in q.get().split(",")]
        if grid[row][col] == 9:
            surrounding = get_surrounding(grid, row, col)
            for e in surrounding:
                q.put(e)
            grid[row][col] = 0
            flashes += 1
        elif grid[row][col] != 0:

            grid[row][col] += 1

    return grid


def all_0(grid):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] != 0:
                return False

    return True


for cc in range(100):
    print("cc", cc)
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            print(grid[row][col], end=" ")
        print()
    if all_0(grid):
        print(cc)
        break
    grid = step(grid)

for row in range(len(grid)):
    for col in range(len(grid[0])):
        print(grid[row][col], end=" ")
    print()

print(flashes)






