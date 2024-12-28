debug = False

def parse(inp: str) -> list[list[str]]:
    return [list(line) for line in inp.splitlines()]


def get_start(map_: list[list[str]]) -> tuple[int, int]:
    for y, line in enumerate(map_):
        for x, c in enumerate(line):
            if c == "S":
                return x, y
    raise ValueError("No start found")


dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def get_best_paths(
    map_: list[list[str]], return_all: bool = True
) -> list[list[tuple[int, tuple[int, int], tuple[int, int]]]]:
    start = get_start(map_)
    to_visit = [[(0, start, dirs[2])]]
    visited = {(to_visit[0][-1][1], to_visit[0][-1][2]): 0}

    merged_paths = []

    end_paths = []

    while to_visit:
        path = to_visit.pop(0)
        x, y = path[-1][1]
        if map_[y][x] == "E":
            end_paths.append(path)
            continue
        for dx, dy in dirs:
            if dx + path[-1][2][0] == 0 and dy + path[-1][2][1] == 0:
                continue
            new_path = path.copy()
            if dx == path[-1][2][0] and dy == path[-1][2][1]:
                score = path[-1][0] + 1
                new_x, new_y = x + dx, y + dy
                if map_[new_y][new_x] == "#":
                    continue
            else:
                score = path[-1][0] + 1000
                new_x, new_y = x, y
            new_path.append((score, (new_x, new_y), (dx, dy)))
            if ((new_x, new_y), (dx, dy)) not in visited or visited[
                ((new_x, new_y), (dx, dy))
            ] > score:
                to_visit.append(new_path)
                to_visit.sort(key=lambda x: x[-1][0])
                visited[((new_x, new_y), (dx, dy))] = score
            elif visited[((new_x, new_y), (dx, dy))] == score:
                merged_paths.append(new_path)
    shortest_distance = min([p[-1][0] for p in end_paths])
    end_paths = [p for p in end_paths if p[-1][0] == shortest_distance]

    if return_all:
        num_end = 0
        while num_end < len(end_paths):
            num_end = len(end_paths)
            for path in end_paths.copy():
                for i, point in enumerate(path):
                    for im, m in enumerate(merged_paths.copy()):
                        if point == m[-1]:
                            end_paths.append(m + path[i + 1 :])
                            merged_paths.pop(im)
            

    return end_paths


def part1(inp: str) -> int:
    map_ = parse(inp)
    paths = get_best_paths(map_, return_all=False)
    return paths[0][-1][0]


def part2(inp: str) -> int:
    map_ = parse(inp)
    paths = get_best_paths(map_)
    for path in paths:
        for _, (x, y), _ in path:
            map_[y][x] = "O"

    if debug:
        for line in map_:
            print("".join(line))

    good_points = sum([line.count("O") for line in map_])
    return good_points