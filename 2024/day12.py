def parse(inp: str) -> list[list[str]]:
    return [list(line) for line in inp.splitlines()]


def fill_region(map_: list[list[str]], x: int, y: int) -> list[tuple[int, int]]:
    c = map_[y][x]
    visited = [(x, y)]
    i = 0
    while i < len(visited):
        tx, ty = visited[i]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = tx + dx, ty + dy
            if nx < 0 or ny < 0 or nx >= len(map_[0]) or ny >= len(map_):
                continue
            if map_[ny][nx] != c or (nx, ny) in visited:
                continue
            visited.append((nx, ny))
        i += 1
    return visited


def get_regions(map_: list[list[str]]) -> list[list[tuple[int, int]]]:
    checked = [[False] * len(map_[0]) for _ in map_]
    regions = []
    for j, row in enumerate(map_):
        for i, _ in enumerate(row):
            if checked[j][i]:
                continue
            this_region = fill_region(map_, i, j)
            for tx, ty in this_region:
                checked[ty][tx] = True
            regions.append(this_region)
    return regions


def perimeter(region: list[tuple[int, int]]) -> int:
    perimeter = 0
    for tx, ty in region:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = tx + dx, ty + dy
            if (nx, ny) not in region:
                perimeter += 1
    return perimeter


def sides(region: list[tuple[int, int]]) -> int:
    region = sorted(region)
    sides = 0
    for tx, ty in region:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = tx + dx, ty + dy
            if (nx, ny) in region:
                continue
            if dy == 0 and ((tx, ty - 1) in region) and ((nx, ny - 1) not in region):
                continue
            if dx == 0 and ((tx - 1, ty) in region) and ((nx - 1, ny) not in region):
                continue
            sides += 1
    return sides


def part1(inp: str) -> int:
    map_ = parse(inp)
    regions = get_regions(map_)
    total = 0
    for reg in regions:
        total += perimeter(reg) * len(reg)
    return total


def part2(inp: str) -> int:
    map_ = parse(inp)
    regions = get_regions(map_)
    total = 0
    for reg in regions:
        total += sides(reg) * len(reg)
    return total
