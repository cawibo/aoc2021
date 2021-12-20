from math import floor, ceil
from itertools import permutations


def is_number(char):
    return char in set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])


def is_left(snailfish, start):
    return snailfish[start - 1] == "["


def get_pair_length(pair):
    return len(str(pair))


def get_number_left(snailfish, start):
    result = []
    for char in reversed(snailfish[: start + 1]):
        if is_number(char):
            result.append(char)
        else:
            break
    return "".join(reversed(result))


def get_number_right(snailfish, start):
    result = []
    for char in snailfish[start:]:
        if is_number(char):
            result.append(char)
        else:
            break
    return "".join(result)


def add_num_left(snailfish, index, num):
    old_number = get_number_left(snailfish, index)
    new_number = int(old_number) + num

    return snailfish[: index + 1 - len(old_number)] + str(new_number) + snailfish[
        index + +1 :
    ], len(str(new_number))


def add_num_right(snailfish, index, num):
    old_number = get_number_right(snailfish, index)
    new_number = int(old_number) + num

    return snailfish[:index] + str(new_number) + snailfish[index + len(old_number) :]


def split_num(num):
    floored = floor(num / 2.0)
    ceiling = ceil(num / 2.0)
    return "[{},{}]".format(floored, ceiling)


def reduce_single(snailfish):
    depth = 0
    action_made = None
    for ci, ce in enumerate(snailfish):
        if ce == "[":
            depth += 1
        elif ce == "]":
            depth -= 1

        if depth == 5:  # explode
            action_made = "exploded"
            pair = [int(e.strip("[]")) for e in snailfish[ci:].split(",")[:2]]
            length = get_pair_length(pair)
            if is_left(snailfish, ci):
                snailfish = snailfish[:ci] + str(0) + snailfish[ci + length - 1 :]
            else:
                snailfish = snailfish[:ci] + str(0) + snailfish[ci + length - 1 :]
            # left
            padding = None
            for i in range(ci - 1, 0, -1):
                if is_number(snailfish[i]):
                    snailfish, padding = add_num_left(snailfish, i, pair[0])
                    break
            # right
            padding = 1 if padding is None else padding
            for i in range(ci + padding, len(snailfish)):
                if is_number(snailfish[i]):
                    snailfish = add_num_right(snailfish, i, pair[1])
                    break
            break

    if action_made is None:
        for ci, ce in enumerate(snailfish):
            if is_number(ce):
                num_str = get_number_right(snailfish, ci)
                num = int(num_str)
                if num >= 10:
                    action_made = "splitted"
                    pair = split_num(num)

                    num_length = len(num_str)
                    before = snailfish[:ci]
                    after = snailfish[ci + num_length :]
                    snailfish = before + pair + after
                    break

    return snailfish, action_made


def magnitude(snailfish):
    def inner(snailfish):
        if isinstance(snailfish, int):
            return snailfish
        left = 3 * inner(snailfish[0])
        right = 2 * inner(snailfish[1])

        return left + right

    return inner(eval(snailfish))


def reduce(snailfish):
    while True:
        snailfish, action_made = reduce_single(snailfish)
        if action_made is None:
            break
    return snailfish


def add(left, right):
    tmp = "[" + left + "," + right + "]"
    return reduce(tmp)


def add_all(terms):
    total = terms[0]
    for term in terms[1:]:
        print(" ", total)
        print("+", term)
        total = add(total, term)
        print("=", total)
        print()
    return total


assert reduce_single("[[[[14,15],[15,14]],[[7,0],16]],[[[[4,2],2],6],[8,7]]]") == (
    "[[[[14,15],[15,14]],[[7,0],20]],[[[0,4],6],[8,7]]]",
    "exploded",
)

assert (
    reduce(
        "[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]"
    )
    == "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"
)

assert (
    reduce(
        "[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]"
    )
    == "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"
)

assert (
    reduce(
        "[[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]],[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]]"
    )
    == "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]"
)

assert (
    reduce(
        "[[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]]"
    )
    == "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]"
)

assert (
    reduce(
        "[[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]"
    )
    == "[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]"
)

assert (
    reduce(
        "[[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]],[[2,[2,2]],[8,[8,1]]]]"
    )
    == "[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]"
)

assert (
    reduce(
        "[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]"
    )
    == "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"
)

assert (
    add("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
)

assert reduce_single("[[[[14,15],[15,14]],[[7,0],16]],[[[[4,2],2],6],[8,7]]]") == (
    "[[[[14,15],[15,14]],[[7,0],20]],[[[0,4],6],[8,7]]]",
    "exploded",
)
assert reduce_single("[[[[[9,8],1],2],3],4]") == ("[[[[0,9],2],3],4]", "exploded")
assert reduce_single("[7,[6,[5,[4,[3,2]]]]]") == ("[7,[6,[5,[7,0]]]]", "exploded")
assert reduce_single("[[6,[5,[4,[3,2]]]],1]") == ("[[6,[5,[7,0]]],3]", "exploded")
assert reduce_single("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]") == (
    "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
    "exploded",
)
assert reduce_single("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]") == (
    "[[3,[2,[8,0]]],[9,[5,[7,0]]]]",
    "exploded",
)
assert reduce_single("[[[[0,7],4],[15,[0,13]]],[1,1]]") == (
    "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]",
    "splitted",
)

assert split_num(10) == "[5,5]"
assert split_num(11) == "[5,6]"
assert split_num(12) == "[6,6]"
assert split_num(13) == "[6,7]"

assert (
    add("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
)


with open("ex.in") as f:
    res = add_all(f.read().split("\n"))
    print("res ", res)
    mag = magnitude(res)
    print(mag)

with open("ex.in") as f:
    P = permutations(f.read().split("\n"), 2)
    mag = 0
    for p in P:
        mag = max(mag, magnitude(add_all(p)))
    print("mag", mag)
