def parse(inp: str) -> list[list[str]]:
    return [list(line.strip()) for line in inp.splitlines()]


def expand(grid: list[list[str]], pad=1) -> list[list[str]]:
    width, height = len(grid[0]), len(grid)

    ngrid = [["."] * (width + 2 * pad) for _ in range(pad)]
    for row in grid:
        ngrid.append(["."] * pad + row + ["."] * pad)
    ngrid.extend([["."] * (width + 2 * pad) for _ in range(pad)])
    return ngrid


neighbours = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]


def check_dir(
    grid: list[list[str]], x: int, y: int, dx: int, dy: int, word: str = "XMAS"
) -> int:
    if not word:
        return 1
    if grid[y][x] != word[0]:
        return 0
    return check_dir(grid, x + dx, y + dy, dx, dy, word[1:])


def part1(inp: str) -> int:
    grid = expand(parse(inp), 3)
    n_xmas = 0
    for j in range(3, len(grid) - 3):
        for i in range(3, len(grid[0]) - 3):
            for dx, dy in neighbours:
                if check_dir(grid, i, j, dx, dy):
                    n_xmas += 1
    return n_xmas


def check_xmas(grid: list[list[str]], x: int, y: int) -> bool:
    if grid[y][x] != "A":
        return False
    x1 = [grid[y - 1][x - 1], grid[y + 1][x + 1]]
    x2 = [grid[y - 1][x + 1], grid[y + 1][x - 1]]
    return all(d.count("S") == 1 and d.count("M") == 1 for d in (x1, x2))


def part2(inp: str) -> int:
    grid = expand(parse(inp), 1)
    n_xmas = 0
    for j in range(1, len(grid) - 1):
        for i in range(1, len(grid[0]) - 1):
            n_xmas += int(check_xmas(grid, i, j))
    return n_xmas