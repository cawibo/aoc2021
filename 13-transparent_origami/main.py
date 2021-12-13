def construct(coords):
    """construct a board according to input coords"""

    board = []
    for y in range(max([e[1] for e in coords]) + 1):
        row = []
        for x in range(max([e[0] for e in coords]) + 1):
            val = 1 if (x, y) in coords else 0
            row.append(val)
        board.append(row)
    return board


def pretty(board):
    """pretty printer of board"""
    for row in range(len(board)):
        for col in range(len(board[0])):
            print(board[row][col], end=" ")
        print()


def count_dots(board):
    """count the number of 'coords' in a board"""
    counter = 0
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col]:
                counter += 1
    return counter


def fold(board, f):
    """fold the board once according to f"""

    new_board = []

    if f[0] == "y":
        # fold over x-axis

        middle_row = f[1]

        for roffset in range(middle_row):
            row = []
            for c in range(len(board[0])):
                this = board[roffset][c]
                that = board[len(board) - roffset - 1][c]
                row.append(this | that)
            new_board.append(row)
    else:
        # fold over y-axis

        middle_col = f[1]

        for r in range(len(board)):
            row = []
            for coffset in range(middle_col):
                this = board[r][coffset]
                that = board[r][len(board[0]) - coffset - 1]
                row.append(this | that)
            new_board.append(row)

    return new_board


def solve1(coords, folds):
    board = construct(coords)
    new_board = fold(board, folds[0])
    print("part1", count_dots(new_board))


def solve2(coords, folds):
    board = construct(coords)
    for f in folds:
        board = fold(board, f)

    print("part2")
    pretty(board)


folds = []
coords = set()
with open("1.in") as f:
    dots = True
    for line in f.readlines():
        try:
            if dots:
                x, y = [int(e) for e in line.strip().split(",")]
                coords.add((x, y))

            else:
                xoy, k = line.split()[2].split("=")
                folds.append((xoy, int(k)))
        except:
            dots = False


solve1(coords, folds)
solve2(coords, folds)
