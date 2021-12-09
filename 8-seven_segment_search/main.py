from itertools import permutations

numbers = {
    119: 1,
    10010: 2,
    15470: 3,
    1785: 4,
    6630: 5,
    72930: 6,
    238: 7,
    510510: 8,
    46410: 9,
    102102: 0,
}


def get_num(on, mapping):
    product = 1
    for e in on:
        product *= mapping[e]
    if product in numbers:
        return numbers[product]
    return None


def legend(unique):
    for te in permutations(unique[0], 2):
        r = [e for e in unique[1] if e not in te][0]
        r1 = [e for e in unique[2] if e not in te]
        for fe in permutations(r1, 2):
            r2 = [e for e in unique[3] if e not in [r] and e not in te and e not in fe]
            for ee in permutations(r2, 2):
                yield {
                    r: 2,
                    fe[0]: 3,
                    fe[1]: 5,
                    te[0]: 7,
                    ee[0]: 11,
                    ee[1]: 13,
                    te[1]: 17,
                }


def decode(inn):
    unique = list(
        filter(lambda ie: len(ie) in [2, 3, 4, 7], sorted(inn, key=lambda ie: len(ie)))
    )
    for m in legend(unique):
        for word in inn:
            if get_num(word, m) is None:
                break
        else:
            return m


total = 0
with open("1.in") as f:
    lines = f.readlines()

    for line in lines:
        inn, out = [e.split() for e in line.split("|")]

        m = decode(inn)
        s = ""
        for oe in out:
            s += str(get_num(oe, m))
        total += int(s)

print(total)
