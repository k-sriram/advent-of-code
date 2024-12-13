def parse(inp: str) -> list[list[int]]:
    return [[int(c) for c in line] for line in inp.splitlines()]


neighbours = [(-1, 0), (0, -1), (1, 0), (0, 1)]


def get_destinations(map_: list[list[int]], x: int, y: int) -> set[tuple[int, int]]:
    alt = map_[y][x]
    dest = set()
    if alt == 9:
        return {(x, y)}
    for dx, dy in neighbours:
        nx, ny = x + dx, y + dy
        if nx < 0 or ny < 0 or nx >= len(map_[0]) or ny >= len(map_):
            continue
        if map_[ny][nx] == alt + 1:
            dest.update(get_destinations(map_, nx, ny))
    return dest


def part1(inp: str) -> int:
    map_ = parse(inp)
    total = 0
    for y, row in enumerate(map_):
        for x, a in enumerate(row):
            if a == 0:
                total += len(get_destinations(map_, x, y))
    return total

def rate_map(map_: list[list[int]]) -> list[list[int]]:
    w, h = len(map_[0]), len(map_)
    rating = [[0] * w for _ in range(h)]

    for alt_check in range(9,-1,-1):
        # print(f"Before processing {alt_check}")
        # print_map(rating, 3)
        for y, row in enumerate(map_):
            for x, alt in enumerate(row):
                if alt != alt_check:
                    continue
                if alt_check == 9:
                    rating[y][x] = 1
                    continue
                for dx, dy in neighbours:
                    nx, ny = x + dx, y + dy
                    if nx < 0 or ny < 0 or nx >= len(map_[0]) or ny >= len(map_):
                        continue
                    if map_[ny][nx] == alt_check + 1:
                        rating[y][x] += rating[ny][nx]
    return rating


def print_map(map_:list[list[int]], space: int = 2):
    for row in map_:
        for a in row:
            a = a % (10**(space-1))
            print(f"{a:{space}}", end="")
        print()


def part2(inp: str) -> int:
    map_ = parse(inp)
    rating = rate_map(map_)
    # print_map(rating, 5)
    total_rating = 0
    for y,row in enumerate(rating):
        for x,r in enumerate(row):
            if map_[y][x] == 0:
                total_rating += r
    return total_rating