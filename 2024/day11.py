from functools import cache


def parse(inp: str) -> list[int]:
    return [int(x) for x in inp.strip().split(" ")]


def blink(stones: list[int]) -> list[int]:
    new_stones = []
    for i in stones:
        if i == 0:
            # print("0 -> 1")
            new_stones.append(1)
        elif (s := len(str(i))) % 2 == 0:
            new_stones.extend([int(str(i)[: s // 2]), int(str(i)[s // 2 :])])
            # print(f"{i} -> {new_stones[-2]} {new_stones[-1]}")
        else:
            new_stones.append(i * 2024)
            # print(f"{i} -> {i*2024}")
    return new_stones


def part1(inp: str) -> int:
    stones = parse(inp)
    for _ in range(25):
        # print(stones)
        stones = blink(stones)
    # print(stones)
    return len(stones)


@cache
def blink_1s(no: int, depth: int) -> int:
    if depth == 0:
        return 1
    if no == 0:
        return blink_1s(1, depth - 1)
    str_no = str(no)
    l_str_no = len(str_no)
    if l_str_no % 2 == 0:
        return blink_1s(int(str_no[: l_str_no // 2]), depth - 1) + blink_1s(
            int(str_no[l_str_no // 2 :]), depth - 1
        )
    return blink_1s(no * 2024, depth - 1)


def part2(inp: str) -> int:
    stones = parse(inp)
    total = 0
    for no in stones:
        total += blink_1s(no, 75)
    return total
