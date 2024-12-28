from functools import cache

def parse(inp: str) -> tuple[list[str], list[str]]:
    towels = inp.split("\n\n")[0].split(", ")
    patterns = inp.split("\n\n")[1].strip().split("\n")
    return towels, patterns



def get_arrangment(towels: list[str], pattern: str) -> list[str] | None:
    if pattern == "":
        return []

    for towel in towels:
        if pattern.startswith(towel):
            if (arr:= get_arrangment(towels, pattern[len(towel) :])) is not None:
                return [towel] + arr
    
    return None
towels = []

@cache
def get_arrangments(pattern: str) -> int:
    if pattern == "":
        return 1

    arrangments = 0
    for towel in towels:
        if pattern.startswith(towel):
            arrangments += get_arrangments(pattern[len(towel) :])
    
    return arrangments

def part1(inp: str) -> int:
    towels, patterns = parse(inp)
    count = 0
    for pattern in patterns:
        if (arr:= get_arrangment(towels, pattern)) is not None:
            count += 1
        print(pattern, arr)
    return count


def part2(inp: str) -> int:
    get_arrangments.cache_clear()
    global towels
    towels, patterns = parse(inp)
    count = 0
    for pattern in patterns:
        count += get_arrangments(pattern)
    return count