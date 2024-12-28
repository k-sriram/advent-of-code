from functools import cache

def parse(inp: str) -> list[str]:
    return inp.splitlines()


def num_to_dir(code: str) -> str:
    x, y = 2, 3
    buttons = {
        "7": (0, 0),
        "8": (1, 0),
        "9": (2, 0),
        "4": (0, 1),
        "5": (1, 1),
        "6": (2, 1),
        "1": (0, 2),
        "2": (1, 2),
        "3": (2, 2),
        "0": (1, 3),
        "A": (2, 3),
    }
    return move_finger(code, x, y, buttons)


def move_finger(code, x, y, buttons):
    out = ""
    for c in code:
        tx, ty = buttons[c]
        dx, dy = tx - x, ty - y
        if y == 3 and ty < 3 and x > 0 and tx == 0:
            out += "^" * -dy
            out += "<" * -dx
        elif dy > 0 and dx > 0 and (x != 0 or ty != 3):
            out += "v" * dy
            out += ">" * dx
        elif dy < 0 and dx > 0:
            out += "^" * -dy
            out += ">" * dx
        else:
            if dx > 0:
                out += ">" * dx
            elif dx < 0:
                out += "<" * -dx
            if dy > 0:
                out += "v" * dy
            elif dy < 0:
                out += "^" * -dy
        out += "A"
        x, y = tx, ty
    return out

mov_pattern = {
    "AA": "A",
    "A^": "<A",
    "Av": "<vA",
    "A>": "vA",
    "A<": "v<<A",
    "^A": ">A",
    "^^": "A",
    "^v": "vA",
    "^>": "v>A",
    "^<": "v<A",
    "vA": "^>A",
    "v^": "^A",
    "vv": "A",
    "v>": ">A",
    "v<": "<A",
    ">A": "^A",
    ">^": "<^A",
    ">v": "<A",
    ">>": "A",
    "><": "<<A",
    "<A": ">>^A",
    "<^": ">^A",
    "<v": ">A",
    "<>": ">>A",
    "<<": "A",
}

def dir_to_dir(code: str) -> str:
    code = "A" + code
    out = ""
    for i in range(len(code)-1):
        out += mov_pattern[code[i:i+2]]
    return out


def revers_dir(code: str) -> str:
    x, y = 2, 0
    buttons = {(0, 1): "<", (1, 0): "^", (1, 1): "v", (2, 0): "A", (2, 1): ">"}
    out = ""
    for c in code:
        if c == ">":
            x += 1
        elif c == "<":
            x -= 1
        elif c == "^":
            y -= 1
        elif c == "v":
            y += 1
        elif c == "A":
            out += buttons[(x, y)]
    return out

@cache
def len_code(code: str, depth: int) -> int:
    if depth == 0:
        return len(code)
    code = dir_to_dir(code)
    L = 0
    for subcode in code.split("A")[:-1]:
        subcode = subcode + "A"
        L += len_code(subcode, depth-1)
    return L

def part1(inp: str) -> int:
    codes = parse(inp)
    total = 0
    for code in codes:
        r1code = num_to_dir(code)
        r2code = dir_to_dir(r1code)
        r3code = dir_to_dir(r2code)
        total += len(r3code) * int(code[:-1])
    return total


def part2(inp: str) -> int:
    codes = parse(inp)
    total = 0
    for code in codes:
        r1code = num_to_dir(code)
        total += len_code(r1code, 25) * int(code[:-1])
    return total