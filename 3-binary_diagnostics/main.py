# task 1
with open("1.in") as f:
    lines = f.readlines()
    N = len(lines)
    B = [0] * len(lines[0].strip())

    for line in lines:
        for i, val in enumerate(line):
            if val == "1":
                B[i] += 1

    gamma = [int(val >= N / 2) for val in B]
    epsilon = [val ^ 1 for val in gamma]

    print(gamma, epsilon)

    gamma = int("".join([str(e) for e in gamma]), 2)
    epsilon = int("".join([str(e) for e in epsilon]), 2)

    print(gamma * epsilon)

# task 2
def most(lines, index=0):
    if len(lines) == 1:
        return int(lines[0], 2)

    is_one = sum([line[index] == "1" for line in lines]) >= len(lines) / 2

    if is_one:
        return most([line for line in lines if line[index] == "1"], index + 1)
    else:
        return most([line for line in lines if line[index] == "0"], index + 1)


def least(lines, index=0):
    if len(lines) == 1:
        return int(lines[0], 2)

    is_one = sum([line[index] == "1" for line in lines]) >= len(lines) / 2

    if not is_one:
        return least([line for line in lines if line[index] == "1"], index + 1)
    else:
        return least([line for line in lines if line[index] == "0"], index + 1)


with open("1.in") as f:
    lines = [line.strip() for line in f.readlines()]

    m = most(lines)
    l = least(lines)

    print(m * l)
