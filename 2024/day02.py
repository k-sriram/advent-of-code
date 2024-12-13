import numpy as np

def parse(inp: str) -> list[list[int]]:
    return [[int(L) for L in line.split()] for line in inp.splitlines()]


def is_report_safe(report: list[int]) -> bool:
    diff = np.diff(np.array(report))
    abs_diff = np.abs(diff)
    signs = np.sign(diff)
    # print(f"Report: {report}")
    # print(f"allSame: {np.all(signs == signs[0])}")
    # print(f"mindiff: {np.all(abs_diff > 0)}")
    # print(f"maxdiff: {np.all(abs_diff <= 3)}")
    return bool(
        np.all(signs == signs[0]) and np.all(abs_diff > 0) and np.all(abs_diff <= 3)
    )

def part1(inp: str) -> int:
    reports = parse(inp)
    return sum(is_report_safe(report) for report in reports)

def is_dampened_report_safe(report: list[int], damps: int) -> bool:
    diff = np.diff(np.array(report))
    sign = np.sign(np.sum(np.sign(diff)))
    debug = False
    for i, d in enumerate(diff):
        if np.abs(d) == 0 or np.abs(d) > 3 or (sign is not None and sign != np.sign(d)):
            if damps == 0:
                if debug:
                    print(f"Report[{damps}]: {report}: bad")
                return False
            l1 = report.copy()
            l1.pop(i)
            ans = is_dampened_report_safe(l1, damps - 1)
            if ans:
                if debug:
                    print(f"Report[{damps}]: {report} -> {l1}: good")
            elif i < len(diff):
                l2 = report.copy()
                l2.pop(i + 1)
                ans = is_dampened_report_safe(l2, damps - 1)
                if ans and debug:
                    print(f"Report[{damps}]: {report} -> {l2}: good")
            if (not ans) and debug:
                print(f"Report[{damps}]: {report}: bad")
            return ans
    if debug:
        print(f"Report[{damps}]: {report} : good")
    return True

def part2(inp: str) -> int:
    reports = parse(inp)
    return sum(is_dampened_report_safe(report, 1) for report in reports)