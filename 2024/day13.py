import re
from dataclasses import dataclass


@dataclass
class ClawMachine:
    a: tuple[int, int]
    b: tuple[int, int]
    p: tuple[int, int]


machine_re = re.compile(
    r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
)


def parse(inp: str) -> list[ClawMachine]:
    machines = []
    for m in machine_re.finditer(inp):
        a = (int(m.group(1)), int(m.group(2)))
        b = (int(m.group(3)), int(m.group(4)))
        p = (int(m.group(5)), int(m.group(6)))
        machines.append(ClawMachine(a, b, p))
    return machines


def solve(m: ClawMachine) -> tuple[int, int] | None:
    num = m.p[0] * m.a[1] - m.p[1] * m.a[0]
    if (den := m.b[0] * m.a[1] - m.b[1] * m.a[0]) == 0:
        if num == 0:
            raise ValueError("Many solutions")
        return None  # No solution
    b, remb = divmod(num, den)
    a, rema = divmod((m.p[0] - m.b[0] * b), m.a[0])
    if remb != 0 or rema != 0:
        return None  # No integer solution
    return (a, b)


def part1(inp: str) -> int:
    machines = parse(inp)
    total = 0
    for m in machines:
        sol = solve(m)
        if sol is None:
            continue
        total += 3 * sol[0] + sol[1]
    return total


def part2(inp: str) -> int:
    machines = parse(inp)
    total = 0
    for m in machines:
        m.p = (m.p[0] + 10000000000000, m.p[1] + 10000000000000)
        sol = solve(m)
        if sol is None:
            continue
        total += 3 * sol[0] + sol[1]
    return total