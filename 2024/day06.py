def parse(inp: str) -> list[list[str]]:
    return [list(c) for c in inp.splitlines()]


pts = ["^", ">", "v", "<"]
dirs = [[0, -1], [1, 0], [0, 1], [-1, 0]]


def get_pos(map_: list[list[str]]) -> tuple[int, int, int]:
    for j, row in enumerate(map_):
        for d, p in enumerate(pts):
            if p in row:
                return (row.index(p), j, d)

    raise ValueError


def move(
    map_: list[list[str]], pos: tuple[int, int, int], mark: bool = True
) -> tuple[bool, tuple[int, int, int]]:
    i, j, d = pos
    if mark:
        map_[j][i] = "X"
    ni, nj = i + dirs[d][0], j + dirs[d][1]
    if ni < 0 or ni >= len(map_[0]) or nj < 0 or nj >= len(map_):
        return False, pos
    if map_[nj][ni] == "#":
        d = (d + 1) % 4
        return True, (i, j, d)
    else:
        return True, (ni, nj, d)


def count_X(map_: list[list[str]]) -> int:
    return sum(row.count("X") for row in map_)


def part1(inp: str) -> int:
    map_ = parse(inp)
    pos = get_pos(map_)
    while True:
        is_move, pos = move(map_, pos)
        if not is_move:
            break
    return count_X(map_)

def is_in_loop(map_:list[list[str]], pos: tuple[int, int, int]) -> bool:
    visited = [pos]
    while True:
        is_move, pos = move(map_, pos, False)
        i, j, d = pos
        if map_[j][i] == ".":
            map_[j][i] = ["|", "-", "|", "-"][d]
        if not is_move:
            return False
        if pos in visited:
            return True
        visited.append(pos)


def part2(inp: str) -> int:
    map_ = parse(inp)
    smap = [row.copy() for row in map_]
    pos = get_pos(map_)
    startpos = pos
    while True:
        is_move, pos = move(map_, pos)
        if not is_move:
            break
    loops = 0

    obstacles = []
    for j in range(len(map_[0])):
        for i in range(len(map_)):
            if map_[j][i] == "X" and (startpos[0] != i or startpos[1] != j):
                obstacles.append((i,j))
    for i, j in tqdm(obstacles):
        tmap = [row.copy() for row in smap]
        tmap[j][i] = "#"
        if is_in_loop(tmap, startpos):
            loops += 1
            # tmap[j][i] = "O"
            # print(f"At {i},{j}")
            # for row in tmap:
            #     print("".join(row))
            # print("")
    return loops