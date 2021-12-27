board = []
with open("1.in") as f:
    for line in f.readlines():
        row = []
        for char in line.strip():
            row.append(char)
        board.append(row)


R = len(board)
C = len(board[0])


def pretty(board):
    for row in range(R):
        for col in range(C):
            print(board[row][col], end="")
        print()
    print()


def step(board):
    # find all > cucumbers that are going to move
    for row in range(R):
        for col in range(C):
            rnext = (row + 1) % R
            cnext = (col + 1) % C

            if board[row][col] == ">":
                if board[row][cnext] == ".":
                    board[row][col] = "D"

    # move them
    for row in range(R):
        for col in range(C):
            rnext = (row + 1) % R
            cnext = (col + 1) % C

            if board[row][col] == "D":
                board[row][col] = "."
                board[row][cnext] = ">"

    # find all v cucumbers that are going to move
    for row in range(R):
        for col in range(C):
            rnext = (row + 1) % R
            cnext = (col + 1) % C

            if board[row][col] == "v":
                if board[rnext][col] == ".":
                    board[row][col] = "W"

    # move them
    for row in range(R):
        for col in range(C):
            rnext = (row + 1) % R
            cnext = (col + 1) % C

            if board[row][col] == "W":
                board[row][col] = "."
                board[rnext][col] = "v"


def to_key(board):
    L = []
    for row in board:
        L.append("".join(row))
    return "".join(L)


prev = to_key(board)
for i in range(1, 10000):
    step(board)
    current = to_key(board)
    if current == prev:
        break
    prev = current

print("part1:", i)
