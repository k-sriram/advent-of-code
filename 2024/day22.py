from collections import defaultdict

def parse(inp: str) -> list[int]:
    return [int(line) for line in inp.splitlines()]


def get_next_secret(num: int) -> int:
    num = ((num * 64) ^ num) % 16777216
    num = ((num // 32) ^ num) % 16777216
    num = ((num * 2048) ^ num) % 16777216
    return num


def part1(inp: str) -> int:
    nums = parse(inp)
    total = 0
    for num in nums:
        for _ in range(2000):
            num = get_next_secret(num)
        total += num
    return total


def get_price_sequence(num: int) -> list[int]:
    prices = []
    for _ in range(2001):
        prices.append(num % 10)
        num = get_next_secret(num)
    return prices


def calc_diff_price(prices: list[int]) -> dict[tuple[int, int, int, int], int]:
    diff = [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]
    diff_tups = [
        (diff[i], diff[i + 1], diff[i + 2], diff[i + 3]) for i in range(len(diff) - 3)
    ]
    diff_prices = defaultdict(int)
    for i, dt in enumerate(diff_tups):
        if dt not in diff_prices:
            diff_prices[dt] = prices[i + 4]
    return diff_prices


def part2(inp: str) -> int:
    nums = parse(inp)
    diff_prices = []
    for num in nums:
        prices = get_price_sequence(num)
        diff_prices.append(calc_diff_price(prices))
    all_diffs = set()
    for d in diff_prices:
        all_diffs.update(d.keys())
    sum_diffs = [sum([dp[d] for dp in diff_prices]) for d in all_diffs]
    return max(sum_diffs)