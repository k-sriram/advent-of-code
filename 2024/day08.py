from collections import defaultdict

import numpy as np


def parse(inp: str) -> list[list[str]]:
    return [list(line) for line in inp.splitlines()]


def find_antennas(map_: list[list[str]]) -> dict[str, list[tuple[int, int]]]:
    antennas = defaultdict(list)
    for j, row in enumerate(map_):
        for i, c in enumerate(row):
            if c == ".":
                continue
            # print(f"{c} at ({i}, {j})")
            antennas[c].append((i, j))
    return dict(antennas)


def calc_antinodes(
    pos1: tuple[int, int], pos2: tuple[int, int]
) -> list[tuple[int, int]]:
    return [
        (2 * pos1[0] - pos2[0], 2 * pos1[1] - pos2[1]),
        (2 * pos2[0] - pos1[0], 2 * pos2[1] - pos1[1]),
    ]


def calc_resonant_antinodes(
    w: int, h: int, pos1: tuple[int, int], pos2: tuple[int, int]
) -> list[tuple[int, int]]:
    diff = (pos2[0] - pos1[0], pos2[1] - pos1[1])
    if diff[0] == 0:
        return [(pos1[0], j) for j in range(h)]
    elif diff[1] == 0:
        return [(i, pos1[1]) for i in range(w)]
    else:
        gcd = np.gcd(*diff)
        lcd: tuple[int, int] = (diff[0] // gcd, diff[1] // gcd)
    i = 0
    anodes = []
    while True:
        nnode = (pos1[0] + i * lcd[0], pos1[1] + i * lcd[1])
        if i > 100:
            raise ValueError
        if nnode[0] < 0 or nnode[0] >= w or nnode[1] < 0 or nnode[1] >= h:
            break
        anodes.append(nnode)
        i += 1
    i = -1
    while True:
        nnode = (pos1[0] + i * lcd[0], pos1[1] + i * lcd[1])
        if nnode[0] < 0 or nnode[0] >= w or nnode[1] < 0 or nnode[1] >= h:
            break
        anodes.append(nnode)
        i -= 1
        if i < -100:
            raise ValueError
    return anodes


def mark_antinodes(
    map_: list[list[str]], antennas: dict[str, list[tuple[int, int]]]
) -> list[list[str]]:
    h, w = len(map_), len(map_[0])
    nmap = [["."] * w for _ in range(h)]
    for t_antennas in antennas.values():
        for i, first in enumerate(t_antennas):
            for second in t_antennas[i + 1 :]:
                antinodes = calc_antinodes(first, second)
                for anode in antinodes:
                    if (
                        anode[0] >= 0
                        and anode[0] < w
                        and anode[1] >= 0
                        and anode[1] < h
                    ):
                        nmap[anode[1]][anode[0]] = "#"
    return nmap


def mark_resonant_antinodes(
    map_: list[list[str]], antennas: dict[str, list[tuple[int, int]]]
) -> list[list[str]]:
    h, w = len(map_), len(map_[0])
    nmap = [["."] * w for _ in range(h)]
    for t_antennas in antennas.values():
        for i, first in enumerate(t_antennas):
            for second in t_antennas[i + 1 :]:
                antinodes = calc_resonant_antinodes(w, h, first, second)
                for anode in antinodes:
                    nmap[anode[1]][anode[0]] = "#"
    return nmap

def part1(inp: str) -> int:
    map_ = parse(inp)
    antennas = find_antennas(map_)
    nmap = mark_antinodes(map_, antennas)
    # for row in nmap:
    #     print("".join(row))
    return sum([row.count("#") for row in nmap])


def part2(inp: str) -> int:
    map_ = parse(inp)
    antennas = find_antennas(map_)
    nmap = mark_resonant_antinodes(map_, antennas)
    for row in nmap:
        print("".join(row))
    return sum([row.count("#") for row in nmap])