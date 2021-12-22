def dice_gen():
    while True:
        for res in range(1, 101):
            yield res


def pos_gen():
    while True:
        for res in range(1, 11):
            yield res


lines = """Player 1 starting position: 4
Player 2 starting position: 1""".split(
    "\n"
)

POSITION = 0
SCORE = 1
players = []
for line in lines:
    _, starting_pos = line.split(":")
    pos = pos_gen()
    for _ in range(int(starting_pos)):
        next(pos)
    players.append((pos, 0))


WIN_SCORE = 1000
counter = 0
dice = dice_gen()
while all(score < WIN_SCORE for _, score in players):
    index = counter % 2

    # roll the dice three times
    to_move = sum(next(dice) for _ in range(3))

    # move the player
    pos = players[index][POSITION]
    for _ in range(to_move):
        space = next(pos)

    # calculate score
    old_score = players[index][SCORE]
    new_score = space + old_score

    # update
    players[index] = (pos, new_score)

    counter += 3

# find the loser by fetching the player with the lowest score
loser = min(players, key=lambda p: p[SCORE])

print("part1", loser[SCORE] * counter)
