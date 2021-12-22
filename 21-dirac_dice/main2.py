from functools import lru_cache
from itertools import product

# each roll of a die creates 3 universes
# each turn entails three rolls of the die
# as such, 3*3*3 universes are created.

# also, becasue the three outcomes of a die
# are pre-determinate, i.e., 1, 2, and 3,
# it is possible to calculate the cumulative
# outcome. Perhaps a gaussian distribution.

# each turn creates 27 universes
# 3 and 9 are present once each
# 4 and 8 are present three times each
# 5 and 7 are present six times each
# and finally, 6 is present seven times


@lru_cache(maxsize=None)
def move(current_pos, spaces):
    for _ in range(spaces):
        if current_pos == 10:
            current_pos = 0
        current_pos += 1
    return current_pos


@lru_cache(maxsize=None)
def turn(
    active_player: int,
    player_one_pos: int,
    player_one_score: int,
    player_two_pos: int,
    player_two_score: int,
):
    if player_one_score >= 21:  # player one wins
        return (1, 0)
    elif player_two_score >= 21:  # player two wins
        return (0, 1)

    if active_player == 1:
        wins = [0, 0]
        for rolls in product(range(1, 4), range(1, 4), range(1, 4)):
            new_pos = move(player_one_pos, sum(rolls))
            result = turn(
                2, new_pos, player_one_score + new_pos, player_two_pos, player_two_score
            )
            wins[0] += result[0]
            wins[1] += result[1]

    elif active_player == 2:
        wins = [0, 0]
        for rolls in product(range(1, 4), range(1, 4), range(1, 4)):
            new_pos = move(player_two_pos, sum(rolls))
            result = turn(
                1,
                player_one_pos,
                player_one_score,
                new_pos,
                player_two_score + new_pos,
            )
            wins[0] += result[0]
            wins[1] += result[1]

    return wins


assert move(7, 5) == 2
assert move(10, 5) == 5

res = turn(1, 4, 0, 1, 0)
print("part2:", max(res))

# 437424806752258
# 469604932270189
# 341960390180808
# 444356092776315
# 40746749749147287
# 55199972140670812
# 93916751312613
