import re

mul_re = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

def part1(inp: str) -> int:
    # get all matches
    matches = mul_re.findall(inp)
    res = sum([int(a) * int(b) for a, b in matches])
    return res


def part2(inp: str) -> int:
    # get all matches
    sections = inp.split("don't()")
    dos = [sections[0]]
    for sec in sections[1:]:
        if "do()" in sec:
            dos.extend(sec.split("do()")[1:])
    res = 0
    print(sections)
    print(dos)
    for sec in dos:
        matches = mul_re.findall(sec)
        res += sum([int(a) * int(b) for a, b in matches])
    return res