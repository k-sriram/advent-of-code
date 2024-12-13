from typing import Callable, Iterator

from tqdm import tqdm

debug = False

class Operator:
    def __init__(self, sym: str, op: Callable[[int, int], int]):
        self.sym = sym
        self.op = op

    def __str__(self):
        return self.sym

    def operate(self, a: int, b: int) -> int:
        return self.op(a, b)


def concat_int(a: int, b: int) -> int:
    result = b
    while b > 0:
        b = b // 10
        a *= 10
    return result + a

add = Operator("+", int.__add__)
multiply = Operator("*", int.__mul__)
concat = Operator("||", concat_int)


def parse(inp: str) -> list[tuple[int, list[int]]]:
    eqs = []
    for line in inp.splitlines():
        target = int(line.split(":")[0])
        nos = [int(n) for n in line.split(":")[1].strip().split(" ")]
        eqs.append((target, nos))
    return eqs


def evaluate(eq: list[int | Operator]) -> int:
    agg = 0
    i = 0
    while i < len(eq):
        t = eq[i]
        if isinstance(t, int):
            agg = t
            i += 1
            continue
        tn = eq[i + 1]
        assert isinstance(tn, int)
        agg = t.operate(agg, tn)
        i += 2
    return agg


def insert_operators(nos: list[int], ops: list[Operator]) -> Iterator[list[int | Operator]]:
    t_ops = len(ops)
    n_ops = len(nos) - 1
    for i in range(t_ops**n_ops):
        eq: list[int | Operator] = [nos[0]]
        for j in range(n_ops):
            ni = (i // (t_ops**j)) % t_ops
            eq.extend([ops[ni], nos[j + 1]])
        yield eq


def part1(inp: str) -> int:
    result = 0
    for target, nos in tqdm(parse(inp)):
        for eq in insert_operators(nos, [add, multiply]):
            if evaluate(eq) == target:
                if debug:
                    print(f"{target} = {' '.join(map(str,eq))}")
                result += target
                break
    return result


def part2(inp: str) -> int:
    result = 0
    for target, nos in tqdm(parse(inp)):
        for eq in insert_operators(nos, [add, multiply, concat]):
            if evaluate(eq) == target:
                if debug:
                    print(f"{target} = {' '.join(map(str,eq))}")
                result += target
                break
    return result