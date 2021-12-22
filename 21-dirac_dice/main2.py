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


from functools import lru_cache


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

    # print("scores", player_one_score, player_two_score)

    if active_player == 1:
        moved_three = move(player_one_pos, 3)
        moved_four = move(player_one_pos, 4)
        moved_five = move(player_one_pos, 5)
        moved_six = move(player_one_pos, 6)
        moved_seven = move(player_one_pos, 7)
        moved_eight = move(player_one_pos, 8)
        moved_nine = move(player_one_pos, 9)

        active_player = 2

        res_three = turn(
            active_player,
            moved_three,
            player_one_score + moved_three,
            player_two_pos,
            player_two_score,
        )
        res_four = turn(
            active_player,
            moved_four,
            player_one_score + moved_four,
            player_two_pos,
            player_two_score,
        )
        res_five = turn(
            active_player,
            moved_five,
            player_one_score + moved_five,
            player_two_pos,
            player_two_score,
        )
        res_six = turn(
            active_player,
            moved_six,
            player_one_score + moved_six,
            player_two_pos,
            player_two_score,
        )
        res_seven = turn(
            active_player,
            moved_seven,
            player_one_score + moved_seven,
            player_two_pos,
            player_two_score,
        )
        res_eight = turn(
            active_player,
            moved_eight,
            player_one_score + moved_eight,
            player_two_pos,
            player_two_score,
        )
        res_nine = turn(
            active_player,
            moved_nine,
            player_one_score + moved_nine,
            player_two_pos,
            player_two_score,
        )

    elif active_player == 2:
        moved_three = move(player_two_pos, 3)
        moved_four = move(player_two_pos, 4)
        moved_five = move(player_two_pos, 5)
        moved_six = move(player_two_pos, 6)
        moved_seven = move(player_two_pos, 7)
        moved_eight = move(player_two_pos, 8)
        moved_nine = move(player_two_pos, 9)

        active_player = 1

        res_three = turn(
            active_player,
            moved_three,
            player_one_score,
            player_two_pos,
            player_two_score + moved_three,
        )
        res_four = turn(
            active_player,
            player_one_pos,
            player_one_score,
            moved_four,
            player_two_score + moved_four,
        )
        res_five = turn(
            active_player,
            player_one_pos,
            player_one_score,
            moved_five,
            player_two_score + moved_five,
        )
        res_six = turn(
            active_player,
            player_one_pos,
            player_one_score,
            moved_six,
            player_two_score + moved_six,
        )
        res_seven = turn(
            active_player,
            player_one_pos,
            player_one_score,
            moved_seven,
            player_two_score + moved_seven,
        )
        res_eight = turn(
            active_player,
            player_one_pos,
            player_one_score,
            moved_eight,
            player_two_score + moved_eight,
        )
        res_nine = turn(
            active_player,
            player_one_pos,
            player_one_score,
            moved_nine,
            player_two_score + moved_nine,
        )

    player_one_wins = (
        res_three[0]
        + res_nine[0]
        + res_four[0] * 3
        + res_eight[0] * 3
        + res_five[0] * 6
        + res_seven[0] * 6
        + res_six[0] * 7
    )
    player_two_wins = (
        res_three[1]
        + res_nine[1]
        + res_four[1] * 3
        + res_eight[1] * 3
        + res_five[1] * 6
        + res_seven[1] * 6
        + res_six[1] * 7
    )

    return (player_one_wins, player_two_wins)


assert move(7, 5) == 2
assert move(10, 5) == 5

res = turn(1, 4, 0, 8, 0)
print(res)

# 341960390180808
# 444356092776315
# 40746749749147287
# 55199972140670812
