from itertools import product


def parse(inp: str) -> tuple[list[tuple[int, int, int, int, int]], list[tuple[int, int, int, int, int]]]:
    locks, keys = [], []
    cur = []
    inp = inp + "\n\n"
    for line in inp.splitlines():
        if line == "":
            if cur == []:
                continue
            if len(cur) != 7:
                raise ValueError("Invalid input")
            if cur[0] == "....." and cur[-1] == "#####":
                k = [0,0,0,0,0]
                for i in range(1, len(cur) - 1):
                    for j in range(5):
                        if cur[i][j] == "#":
                            k[j] += 1
                keys.append(tuple(k))
            if cur[0] == "#####" and cur[-1] == ".....":
                k = [0,0,0,0,0]
                for i in range(1, len(cur) - 1):
                    for j in range(5):
                        if cur[i][j] == ".":
                            k[j] -= 1
                locks.append(tuple(k))
            cur = []
        else:
            cur.append(line)
    return locks, keys


def part1(inp: str) -> int:
    locks, keys = parse(inp)
    print(len(locks), len(keys))
    print(locks[0], "...", locks[-1])
    print(keys[0], "...", keys[-1])
    total = 0
    for lock, key in product(locks, keys):
        if all(l + k <= 0 for l, k in zip(lock, key)):
            total += 1
    return total