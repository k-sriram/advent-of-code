def parse(inp: str) -> tuple[list[tuple[int,int]], list[list[int]]]:
    rules = []
    pages = []
    mode = "rules"
    for line in inp.splitlines():
        if not line:
            mode = "pages"
            continue
        if mode == "rules":
            rules.append((int(line.split("|")[0]),int(line.split("|")[1])))
        if mode == "pages":
            pages.append([int(n) for n in line.split(",")])
    return rules, pages

def is_ordered(rules:list[tuple[int,int]], page: list[int]) -> bool:
    for a, b in rules:
        if a in page and b in page:
            if page.index(a) > page.index(b):
                return False
    return True

def middlenum(page: list[int]) -> int:
    return page[len(page)//2]

def part1(inp: str) -> int:
    rules, pages = parse(inp)
    return sum([middlenum(page) for page in pages if is_ordered(rules, page)])

def check_xmas(grid: list[list[str]], x: int, y: int) -> bool:
    if grid[y][x] != "A":
        return False
    x1 = [grid[y - 1][x - 1], grid[y + 1][x + 1]]
    x2 = [grid[y - 1][x + 1], grid[y + 1][x - 1]]
    return all(d.count("S") == 1 and d.count("M") == 1 for d in (x1, x2))

def order_page(rules:list[tuple[int,int]], page: list[int]) -> list[int]:
    for a, b in rules:
        if a in page and b in page:
            if (ia:=page.index(a)) > (ib:=page.index(b)):
                page[ia], page[ib] = page[ib], page[ia]
    if is_ordered(rules, page):
        return page
    else:
        return order_page(rules, page)

def part2(inp: str) -> int:
    rules, pages = parse(inp)
    result = 0
    for page in pages:
        if not is_ordered(rules, page):
            corr_page = order_page(rules, page.copy())
            # print(f"{page} -> {corr_page} : {middlenum(corr_page)}")
            result += middlenum(corr_page)
    return result