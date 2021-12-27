RA = 2
RB = 4
RC = 6
RD = 8


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
        return all(map(lambda s: s == ".", hallway[end:start]))

    return False


assert can_go_to(".........AD", 9, 2)


def all_possible_hallway(hallway, start):
    result = []

    for i in range(len(hallway)):

        # should not be an entryway
        if i not in [RA, RB, RC, RD] and can_go_to(hallway, start, i):
            result.append(i)

    return result


assert can_go_to("A...B", 0, 2)
assert can_go_to("A...B", 0, 3)
assert not can_go_to("A...B", 0, 4)
assert not can_go_to("A...B.", 0, 5)
assert can_go_to(".A...B", 5, 4)
assert can_go_to(".A...B", 5, 3)
assert can_go_to(".A...B", 5, 2)
assert not can_go_to(".A...B", 5, 1)
assert not can_go_to(".A...B", 5, 0)


def is_type(tpe):
    return lambda a: a == tpe


def done(hallway, rooms):
    return (
        all(map(is_type("."), hallway))
        and all(map(is_type("A"), rooms[0]))
        and all(map(is_type("B"), rooms[1]))
        and all(map(is_type("C"), rooms[2]))
        and all(map(is_type("D"), rooms[3]))
    )


COST = {"A": 1, "B": 10, "C": 100, "D": 1000}


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

ROOM_SIZE = 4


def steps_to_leave(room):
    assert room
    return ROOM_SIZE - len(room) + 1


# assert steps_to_leave("A") == 2
# assert steps_to_leave("AA") == 1


def steps_to_enter(room):
    assert len(room) < ROOM_SIZE
    return ROOM_SIZE - len(room)


# assert steps_to_enter("") == 2
# assert steps_to_enter("A") == 1


def travel_cost(tpe, steps):
    assert tpe in "ABCD"
    assert steps >= 0
    return COST[tpe] * steps


assert travel_cost("A", 10) == 10
assert travel_cost("B", 5) == 50
assert travel_cost("C", 2) == 200
assert travel_cost("D", 8) == 8000


def steps_hallway(frm, to):
    assert frm != to
    return abs(frm - to)


assert steps_hallway(0, 10) == 10
assert steps_hallway(5, 6) == 1
assert steps_hallway(6, 5) == 1


def get_room(rooms, tpe):
    assert tpe in "ABCD"
    if tpe == "A":
        return rooms[0]
    elif tpe == "B":
        return rooms[1]
    elif tpe == "C":
        return rooms[2]
    else:
        return rooms[3]


def get_entryway(tpe):
    assert tpe in "ABCD"
    if tpe == "A":
        return RA
    elif tpe == "B":
        return RB
    elif tpe == "C":
        return RC
    else:
        return RD


def correct_rooms(rooms, room, tpe):
    M = {"A": 0, "B": 1, "C": 2, "D": 3}
    index = M[tpe]
    new_rooms = deepcopy(rooms)
    new_rooms[index] = room
    return new_rooms


from copy import deepcopy


cache = {}


def to_key(hallway, rooms):
    return hallway + ":" + "|".join(rooms)


lowest = 1e8


def step(hallway, rooms, cost, history=""):
    key = to_key(hallway, rooms)
    if key in cache:
        # print(key)
        stored_cost = cache[key]
        if stored_cost < cost:
            return
            # print("using cached value")
            cost = stored_cost
        else:
            # print("overwriting cache")
            cache[key] = cost
    else:
        # print("write to cache")
        cache[key] = cost

    global lowest
    if cost >= lowest:
        return

    # print("step: ", "\t| ".join(map(str, [hallway, str(rooms), cost])))
    if done(hallway, rooms):
        print("DONE with cost:", cost)
        print("key", key, ":", cost)
        print(history)
        print()
        lowest = min(lowest, cost)
        return cost

    for pos, elem in enumerate(hallway):
        if elem == ".":
            continue

        # print("found amphipod", elem, "at", pos)
        entryway = get_entryway(elem)
        room = get_room(rooms, elem)
        # print("entryway", entryway, "for room", room)
        # print(empty_or_segregated(room, elem))
        # print(can_go_to(hallway, pos, entryway))
        if empty_or_segregated(room, elem) and can_go_to(hallway, pos, entryway):
            steps = steps_hallway(pos, entryway) + steps_to_enter(room)
            cost_increment = travel_cost(elem, steps)

            new_hallway, new_room = move_from_hallway_to_room(hallway, pos, room)
            new_rooms = correct_rooms(rooms, new_room, elem)
            step(
                new_hallway,
                new_rooms,
                cost + cost_increment,
                history + "\n" + key + " : " + str(cost),
            )

    for ri, room in enumerate(rooms):
        tpe = "ABCD"[ri]
        if not empty_or_segregated(room, tpe):
            entryway = get_entryway(tpe)
            current_tpe = room[0]

            for pos in all_possible_hallway(hallway, entryway):
                new_hallway, new_room = move_from_room_to_hallway(room, hallway, pos)
                steps = steps_hallway(entryway, pos) + steps_to_leave(room)
                cost_increment = travel_cost(current_tpe, steps)

                new_rooms = correct_rooms(rooms, new_room, tpe)

                step(
                    new_hallway,
                    new_rooms,
                    cost + cost_increment,
                    history + "\n" + key + " : " + str(cost),
                )


hallway = "..........."
roomA = "DDDC"
roomB = "DCBA"
roomC = "BBAB"
roomD = "AACC"
rooms = [roomA, roomB, roomC, roomD]

# print(all_possible_hallway("BC.D...D...", RD))

step(hallway, rooms, 0)
# print("res", res)

# hallway = ".........AD"
# rooms = ["A", "BB", "CC", "D"]
# step(hallway, rooms, 0)
