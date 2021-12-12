# INPUT
T = """xz-end
CJ-pt
pt-QW
hn-SP
pw-CJ
SP-end
hn-pt
GK-nj
fe-nj
CJ-nj
hn-ZZ
hn-start
hn-fe
ZZ-fe
SP-nj
SP-xz
ZZ-pt
nj-ZZ
start-ZZ
hn-GK
CJ-end
start-fe
CJ-xz"""

# parse transitions
ts = {}
for t in T.split("\n"):
    o, d = t.split("-")
    if o in ts:
        ts[o].append(d)
    else:
        ts[o] = [d]
    if d in ts:
        ts[d].append(o)
    else:
        ts[d] = [o]


def valid(path, d):

    if d in ["start", "end"] or d.upper() == d:
        return True

    if path.count(d) == 2:
        return False

    s = set()
    for state in path:
        if state in ["start", "end"] or state.upper() == state:
            continue
        if state in s and d in path:
            return False
        s.add(state)
    return True


def explore(current, path):
    path = path + [current]

    if current == "end":
        return 1

    if current not in ts:
        return 0

    ds = [d for d in ts[current] if d != "start" and valid(path, d)]

    path_count = 0
    for d in ds:
        path_count += explore(d, path)

    return path_count


res = explore("start", [])

print(res)
