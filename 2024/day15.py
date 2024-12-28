import re

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.ndimage import gaussian_filter
from tqdm import tqdm


bx, by = 101, 103


class Robot:
    def __init__(self, px: int, py: int, vx: int, vy: int):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy

    def update(self, cycles: int):
        self.px = (self.px + self.vx * cycles) % bx
        self.py = (self.py + self.vy * cycles) % by


robot_re = re.compile(r"^p=(\d+),(\d+) v=(-?\d+),(-?\d+)$")


def parse(inp: str) -> list[Robot]:
    robots = []
    for line in inp.strip().split("\n"):
        m = robot_re.match(line)
        if m:
            px, py, vx, vy = map(int, m.groups())
            robots.append(Robot(px, py, vx, vy))
    return robots


def count_in_quadrants(robots: list[Robot]) -> tuple[int, int, int, int]:
    q1, q2, q3, q4 = 0, 0, 0, 0
    for r in robots:
        if r.px < bx // 2:
            if r.py < by // 2:
                q1 += 1
            elif r.py > by // 2:
                q3 += 1
        elif r.px > bx // 2:
            if r.py < by // 2:
                q2 += 1
            elif r.py > by // 2:
                q4 += 1
    return q1, q2, q3, q4


def robots_to_str(robots: list[Robot]) -> str:
    grid = np.zeros((by, bx), dtype=int)
    out = ""
    for r in robots:
        grid[r.py, r.px] = 1
    for row in grid:
        out = out + "".join(str(min(9, x)) if x else "." for x in row) + "\n"
    return out


def robots_to_arr(robots: list[Robot]) -> np.ndarray:
    grid = np.zeros((by, bx))
    for r in robots:
        grid[r.py, r.px] = 1.0
    return grid


def part1(inp: str) -> int:
    robots = parse(inp)
    for r in robots:
        r.update(100)
    q1, q2, q3, q4 = count_in_quadrants(robots)
    print(q1, q2, q3, q4)
    return q1 * q2 * q3 * q4


def easter_heuristic(robots: list[Robot]) -> float:
    xm, ym = bx // 2, by // 2
    heur = 0
    for r in robots:
        heur += (r.px - xm) ** 2 + (r.py - ym) ** 2
    return heur


ctree_img = Image.open("ctree.bmp")
ctree_arr = np.array(ctree_img.getdata()).reshape(ctree_img.size[1], ctree_img.size[0])
ctree_arr = gaussian_filter(ctree_arr, 5)
ctree_arr = ctree_arr / ctree_arr.max()


def image_heuristic(robots: list[Robot]) -> float:
    grid = robots_to_arr(robots)
    grid = gaussian_filter(grid, 5)
    return (ctree_arr * grid).sum()


def part2(inp: str) -> int:
    robots = parse(inp)
    sr = []
    heuristic = []
    for i in tqdm(range(10000)):
        heuristic.append(easter_heuristic(robots))
        if heuristic[-1] < 500_000:
            print(robots_to_str(robots))
        for r in robots:
            r.update(1)
    plt.plot(range(len(heuristic)), heuristic)
    plt.show()
    print(min(heuristic))

    return np.argmin(heuristic)
