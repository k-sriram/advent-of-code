def parse(inp: str) -> list[list[str]]:
    return [list(line) for line in inp.splitlines()]


def get_start_pos(grid: list[list[str]]) -> tuple[int, int]:
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "S":
                return x, y
    raise ValueError("No start position found")


def get_path(grid: list[list[str]]) -> dict[tuple[int, int], int]:
    w, h = len(grid[0]), len(grid)
    start = get_start_pos(grid)
    path = {start: 0}
    x, y = start
    lx, ly = None, None
    i = 1
    while True:
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= w or ny < 0 or ny >= h:
                continue
            if grid[ny][nx] == "E":
                path[(nx, ny)] = i
                return path
            if grid[ny][nx] == "." and (nx, ny) != (lx, ly):
                path[(nx, ny)] = i
                lx, ly = x, y
                x, y = nx, ny
                i += 1
                break
        else:
            raise ValueError("No path found")


def get_good_shortcuts(
    path: dict[tuple[int, int], int], max_shortcut: int, min_save: int
) -> int:
    gs = 0
    neighbors = set()
    for dxpy in range(-max_shortcut, max_shortcut + 1):
        for dxmy in range(-max_shortcut, max_shortcut + 1):
            dx, dy = (dxpy + dxmy) // 2, (dxpy - dxmy) // 2
            d = abs(dx) + abs(dy)
            if d > max_shortcut:
                continue
            neighbors.add(((dx, dy), d))
    for (x, y), i in path.items():
        for (dx, dy), d in neighbors:
            nx, ny = x + dx, y + dy
            if path.get((nx, ny), 0) >= i + d + min_save:
                gs += 1
    return gs


def part1(inp: str) -> int:
    grid = parse(inp)
    path = get_path(grid)
    good_shortcuts = get_good_shortcuts(path, 2, 100)
    return good_shortcuts


def part2(inp: str) -> int:
    grid = parse(inp)
    path = get_path(grid)
    good_shortcuts = get_good_shortcuts(path, 20, 100)
    return good_shortcuts
