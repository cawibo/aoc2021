h2b = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def to_bin(hex):
    result = []

    for char in hex:
        result.append(h2b[char])

    return [c for c in "".join(result)]


def eat(stream, length):
    for _ in range(length):
        stream.pop(0)


def read_version(stream):
    version = stream[:3]
    eat(stream, 3)

    return int("".join(version), 2)


def read_type(stream):
    tpe = stream[:3]
    eat(stream, 3)

    return int("".join(tpe), 2)


def read_literal_group(stream):
    eat(stream, 1)  # leading 1 or 0
    group = stream[:4]
    eat(stream, 4)

    return "".join(group)


def read_literal(stream):
    literal = []

    count = 1
    while stream[0] == "1":
        count += 1
        literal_group = read_literal_group(stream)
        literal.append(literal_group)

    # 0-prefixed group
    literal_group = read_literal_group(stream)
    literal.append(literal_group)

    res = int("".join(literal), 2)
    return res


def read_length_type(stream):
    length_type = stream[0]
    eat(stream, 1)

    return length_type


def read_operator_size(stream):
    size = stream[:15]
    eat(stream, 15)

    return int("".join(size), 2)


def read_operator_number(stream):
    number = stream[:11]
    eat(stream, 11)

    return int("".join(number), 2)


def read_operator_0(stream):
    size = read_operator_size(stream)

    subpackets = []
    stream_length_before = len(stream)
    while stream_length_before - size < len(stream):
        subpacket = read_packet(stream)
        subpackets.append(subpacket)

    return subpackets


def read_operator_1(stream):
    number = read_operator_number(stream)

    subpackets = []
    for _ in range(number):
        subpacket = read_packet(stream)
        subpackets.append(subpacket)

    return subpackets


def read_operator(stream):
    length_type = read_length_type(stream)

    if length_type == "0":
        subpackets = read_operator_0(stream)
    else:
        subpackets = read_operator_1(stream)

    return subpackets


def product(numbers):
    result = 1
    for number in numbers:
        result *= number
    return result


def read_packet(stream):
    version = read_version(stream)
    tpe = read_type(stream)

    global cumulative_version_numbers
    cumulative_version_numbers += version

    # literal
    if tpe == 4:
        return read_literal(stream)

    # operator
    else:
        numbers = read_operator(stream)

        if tpe == 0:
            return sum(numbers)
        elif tpe == 1:
            return product(numbers)
        elif tpe == 2:
            return min(numbers)
        elif tpe == 3:
            return max(numbers)
        elif tpe == 5:
            return int(1 if numbers[0] > numbers[1] else 0)
        elif tpe == 6:
            return int(1 if numbers[0] < numbers[1] else 0)
        elif tpe == 7:
            return int(numbers[0] == numbers[1])


cumulative_version_numbers = 0

with open("1.in") as f:
    hx = f.read()
    bn = to_bin(hx)
    result = read_packet(bn)
    print("part1:", cumulative_version_numbers)
    print("part2:", result)
