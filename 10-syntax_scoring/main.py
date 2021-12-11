illegals = []

match = {")": "(", "]": "[", "}": "{", ">": "<"}
score = {")": 3, "]": 57, "}": 1197, ">": 25137}
score2 = {"(": 1, "[": 2, "{": 3, "<": 4}

auto_scores = []
with open("1.in") as f:
    for line in f.readlines():
        scope = ""

        for char in line.strip():
            if char in "({[<":
                scope += char
            else:
                if scope[-1] == match[char]:
                    scope = scope[:-1]
                else:
                    illegals.append(score[char])
                    break

        else:
            num = 0
            for char in scope[::-1]:
                num *= 5
                num += score2[char]
            auto_scores.append(num)

    print("part1", sum(illegals))
    middle = len(auto_scores) // 2
    print("part2", sorted(auto_scores)[middle])
