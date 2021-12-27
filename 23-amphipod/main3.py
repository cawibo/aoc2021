def empty_or_segregated(room, tpe):
    return all(map(lambda char: char == tpe, room))


assert empty_or_segregated("", "A")
assert empty_or_segregated("A", "A")
assert empty_or_segregated("AA", "A")
assert not empty_or_segregated("AC", "A")
assert not empty_or_segregated("C", "A")


def hallway_right(hallway, start):
    for index, elem in enumerate(hallway[start + 1 :]):
        if elem != ".":
            return start + index + 1
    return len(hallway) - 1


assert hallway_right("....A", 0) == 4
assert hallway_right("ABC....D", 4) == 7
assert hallway_right("A...B", 0) == 4
assert hallway_right("A...", 0) == 3


def hallway_left(hallway, start):
    for index, elem in enumerate(hallway[::-1][len(hallway) - start + 1 :]):
        if elem != ".":
            return start - index - 1
    return 0


assert hallway_left("A....", 4) == 1
assert hallway_left("D....CBA", 6) == 1
assert hallway_left("B...A", 4) == 1
assert hallway_left("...A", 3) == 0


def hallways(hallway, start):
    left = hallway_left(hallway, start)
    right = hallway_right(hallway, start)
    return left, right


def can_go_to(hallway, start, end):
    if start < end:
        return all(map(lambda s: s == ".", hallway[start + 1 : end + 1]))
    if start > end:
        return all(map(lambda s: s == ".", hallway[end : start + 1]))

    return False


def all_possible_hallway(hallway, start):
    result = []

    for i in range(len(hallway)):

        # should not be an entryway
        if i not in [RA, RB, RC, RD] and can_go_to(hallway, start, i):
            result.append(i)

    return result


# assert can_go_to("A...B", 0, 2)
# assert can_go_to("A...B", 0, 3)
# assert not can_go_to("A...B", 0, 4)
# assert not can_go_to("A...B.", 0, 5)
# assert can_go_to(".A...B", 5, 4)
# assert can_go_to(".A...B", 5, 3)
# assert can_go_to(".A...B", 5, 2)
# assert not can_go_to(".A...B", 5, 1)
# assert not can_go_to(".A...B", 5, 0)


RA = 2
RB = 4
RC = 6
RD = 8


def is_type(tpe):
    return lambda a: a == tpe


def done(hallway, roomA, roomB, roomC, roomD):
    return (
        all(map(is_type("."), hallway))
        and all(map(is_type("A"), roomA))
        and all(map(is_type("B"), roomB))
        and all(map(is_type("C"), roomC))
        and all(map(is_type("D"), roomD))
    )


COST = {"A": 1, "B": 10, "C": 100, "D": 1000}

lowest = 1e8


def move_from_hallway_to_room(hallway, index, room):
    assert hallway[index] in "ABCD"
    amphipod = hallway[index]
    new_hallway = remove_at(hallway, index)
    new_room = amphipod + room
    return new_hallway, new_room


def move_from_room_to_hallway(room, hallway, index):
    assert hallway[index] == "."
    amphipod = room[0]
    new_room = room[1:]
    new_hallway = add_at(hallway, index, amphipod)
    return new_hallway, new_room


def remove_at(hallway, index):
    return hallway[:index] + "." + hallway[index + 1 :]


def add_at(hallway, index, char):
    return hallway[:index] + char + hallway[index + 1 :]


assert move_from_room_to_hallway("AA", "...........", 5) == (".....A.....", "A")
assert move_from_hallway_to_room("........A..", 8, "A") == ("...........", "AA")

ROOM_SIZE = 2


def steps_to_leave(room):
    assert room
    return ROOM_SIZE - len(room) + 1


assert steps_to_leave("A") == 2
assert steps_to_leave("AA") == 1


def steps_to_enter(room):
    assert len(room) < ROOM_SIZE
    return ROOM_SIZE - len(room)


assert steps_to_enter("") == 2
assert steps_to_enter("A") == 1


def travel_cost(tpe, steps):
    return COST[tpe] * steps


def steps_hallway(frm, to):
    assert frm != to
    return abs(frm - to)


assert steps_hallway(0, 10) == 10
assert steps_hallway(5, 6) == 1
assert steps_hallway(6, 5) == 1


def step(hallway, roomA, roomB, roomC, roomD, cost=0):

    # print("step: ", "\t| ".join(map(str, [hallway, roomA, roomB, roomC, roomD, cost])))
    if done(hallway, roomA, roomB, roomC, roomD):
        print(
            "step: ", "\t| ".join(map(str, [hallway, roomA, roomB, roomC, roomD, cost]))
        )
        print("DONE with cost:", cost)
        print()

        return cost

    before = hallway + roomA + roomB + roomC + roomD

    if cost >= lowest:
        return 1e8

    next_states = []

    for pos, elem in enumerate(hallway):

        if elem == "A" and empty_or_segregated(roomA, "A"):
            if can_go_to(hallway, pos, RA):
                steps = steps_hallway(pos, RA) + steps_to_enter(roomA)
                cost_increment = travel_cost(elem, steps)

                # print("moving A to room")
                new_hallway, new_roomA = move_from_hallway_to_room(hallway, pos, roomA)
                # print("adding A to roomA", "'" + roomA + "'", "'" + new_roomA + "'")

                step(
                    new_hallway,
                    new_roomA,
                    roomB,
                    roomC,
                    roomD,
                    cost + cost_increment,
                )

        elif elem == "B" and empty_or_segregated(roomB, "B"):
            if can_go_to(hallway, pos, RB):
                steps = steps_hallway(pos, RB) + steps_to_enter(roomB)
                cost_increment = travel_cost(elem, steps)

                # print("moving B to room")
                new_hallway, new_roomB = move_from_hallway_to_room(hallway, pos, roomB)
                # print("adding B to roomB", "'" + roomB + "'", "'" + new_roomB + "'")

                step(
                    new_hallway,
                    roomA,
                    new_roomB,
                    roomC,
                    roomD,
                    cost + cost_increment,
                )

        elif elem == "C" and empty_or_segregated(roomC, "C"):
            if can_go_to(hallway, pos, RC):
                steps = steps_hallway(pos, RC) + steps_to_enter(roomC)
                cost_increment = travel_cost(elem, steps)

                # print("moving B to room")
                new_hallway, new_roomC = move_from_hallway_to_room(hallway, pos, roomC)
                # print("adding B to roomC", "'" + roomC + "'", "'" + new_roomC + "'")

                step(
                    new_hallway,
                    roomA,
                    roomB,
                    new_roomC,
                    roomD,
                    cost + cost_increment,
                )

        elif elem == "D" and empty_or_segregated(roomD, "D"):
            if can_go_to(hallway, pos, RD):
                steps = steps_hallway(pos, RD) + steps_to_enter(roomD)
                cost_increment = travel_cost(elem, steps)

                # print("moving B to room")
                new_hallway, new_roomD = move_from_hallway_to_room(hallway, pos, roomD)
                # print("adding B to roomD", "'" + roomD + "'", "'" + new_roomD + "'")

                step(
                    new_hallway,
                    roomA,
                    roomB,
                    roomC,
                    new_roomD,
                    cost + cost_increment,
                )

    assert hallway + roomA + roomB + roomC + roomD == before

    # TODO ensure that they won't leave rooms that are done.
    if roomA and not empty_or_segregated(roomA, "A"):

        for pos in all_possible_hallway(hallway, RA):
            # print("A")
            new_hallway, new_roomA = move_from_room_to_hallway(roomA, hallway, pos)
            steps = steps_hallway(RA, pos) + steps_to_leave(roomA)
            cost_increment = travel_cost(roomA[0], steps)

            step(
                new_hallway,
                new_roomA,
                roomB,
                roomC,
                roomD,
                cost + cost_increment,
            )

    if roomB and not empty_or_segregated(roomB, "B"):

        for pos in all_possible_hallway(hallway, RB):
            # print("B")
            new_hallway, new_roomB = move_from_room_to_hallway(roomB, hallway, pos)
            steps = steps_hallway(RB, pos) + steps_to_leave(roomB)
            cost_increment = travel_cost(roomB[0], steps)

            step(
                new_hallway,
                roomA,
                new_roomB,
                roomC,
                roomD,
                cost + cost_increment,
            )

    if roomC and not empty_or_segregated(roomC, "C"):

        for pos in all_possible_hallway(hallway, RC):
            # print("C")
            new_hallway, new_roomC = move_from_room_to_hallway(roomC, hallway, pos)
            steps = steps_hallway(RC, pos) + steps_to_leave(roomC)
            cost_increment = travel_cost(roomC[0], steps)

            step(
                new_hallway,
                roomA,
                roomB,
                new_roomC,
                roomD,
                cost + cost_increment,
            )

    if roomD and not empty_or_segregated(roomD, "D"):

        for pos in all_possible_hallway(hallway, RD):
            # print("D", hallway, roomD, pos)
            new_hallway, new_roomD = move_from_room_to_hallway(roomD, hallway, pos)
            steps = steps_hallway(RD, pos) + steps_to_leave(roomD)
            cost_increment = travel_cost(roomD[0], steps)

            step(
                new_hallway,
                roomA,
                roomB,
                roomC,
                new_roomD,
                cost + cost_increment,
            )


hallway = "..........."
roomA = "BA"
roomB = "CD"
roomC = "BC"
roomD = "DA"

# print(all_possible_hallway("BC.D...D...", RD))

res = step(hallway, roomA, roomB, roomC, roomD)
print("res", res)
