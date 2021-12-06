def step(state):
    next_state = state[1:] + [state[0]]
    next_state[6] += state[0]

    return next_state


def solve(initial, days=256):
    state = [0] * 9
    for e in initial:
        state[e] += 1

    for _ in range(days):
        state = step(state)

    return sum(state)


with open("1.in") as f:
    initial = [int(e) for e in f.readline().strip().split(",")]
    res = solve(initial)
    print(res)
