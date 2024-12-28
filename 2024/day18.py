def parse(inp: str) -> list[tuple[int, int]]:
    return [tuple(map(int, line.split(","))) for line in inp.splitlines()]


def corr_to_map(corr: list[tuple[int, int]], steps: int) -> list[list[str]]:
    x_max = max(x for x, _ in corr)
    y_max = max(y for _, y in corr)
    map_ = [["." for _ in range(x_max + 1)] for _ in range(y_max + 1)]
    for x, y in corr[:steps]:
        map_[y][x] = "#"
    return map_


def get_shortest_path(map_: list[list[str]]) -> int:
    start = (0, 0)
    end = (len(map_[0]) - 1, len(map_) - 1)
    visited = [(start, 0)]
    i = 0
    while i < len(visited):
        pos, steps = visited[i]
        if pos == end:
            return steps
        x, y = pos
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_pos = (x + dx, y + dy)
            if 0 <= new_pos[0] < len(map_[0]) and 0 <= new_pos[1] < len(map_):
                if map_[new_pos[1]][new_pos[0]] == "." and (
                    new_pos not in [p for p, _ in visited]
                    or steps + 1 < [s for p, s in visited if p == new_pos][0]
                ):
                    visited.append((new_pos, steps + 1))
        i += 1
    return -1


def part1(inp: str) -> int:
    corr = parse(inp)
    map_ = corr_to_map(corr, 1024)
    return get_shortest_path(map_)


def part2(inp: str) -> str:
    corr = parse(inp)
    min_pass = 0
    max_fail = len(corr)
    while max_fail - min_pass > 1:
        mid = (min_pass + max_fail) // 2
        map_ = corr_to_map(corr, mid)
        if get_shortest_path(map_) == -1:
            max_fail = mid
        else:
            min_pass = mid
    return ",".join(map(str, corr[max_fail - 1]))
    