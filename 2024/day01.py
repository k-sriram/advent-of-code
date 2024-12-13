def day1_part1(inp: str) -> int:
    list1, list2 = zip(*(map(int,i.split()) for i in inp.splitlines()))
    diff = 0
    for i, j in zip(sorted(list1), sorted(list2)):
        diff += abs(i-j)
    return diff

def day1_part2(inp: str) -> int:
    list1, list2 = zip(*(map(int,i.split()) for i in inp.splitlines()))
    similarity = 0
    for i in list1:
        similarity += i * list2.count(i)
    return similarity