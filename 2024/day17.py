from dataclasses import dataclass

@dataclass
class Program:
    ins: list[int]
    init_a: int
    init_b: int
    init_c: int

    def run(self) -> list[int]:
        ip, a, b, c = 0, self.init_a, self.init_b, self.init_c
        out = []

        def combo(operand: int) -> int:
            return operand if operand <= 3 else [a, b, c][operand - 4]

        while ip < len(self.ins):
            opcode = self.ins[ip]
            operand = self.ins[ip + 1]
            if opcode == 0:
                a = a // (2 ** combo(operand))
            elif opcode == 1:
                b = b ^ operand
            elif opcode == 2:
                b = combo(operand) % 8
            elif opcode == 3:
                if a != 0:
                    ip = operand
                    continue
            elif opcode == 4:
                b = b ^ c
            elif opcode == 5:
                out.append(combo(operand) % 8)
            elif opcode == 6:
                b = a // (2 ** combo(operand))
            elif opcode == 7:
                c = a // (2 ** combo(operand))
            ip += 2
        return out


def parse(inp: str) -> Program:
    line_iter = iter(inp.splitlines())
    a = int(next(line_iter).split(":")[1].strip())
    b = int(next(line_iter).split(":")[1].strip())
    c = int(next(line_iter).split(":")[1].strip())
    next(line_iter)
    program = [int(i) for i in next(line_iter).split(":")[1].strip().split(",")]
    return Program(program, a, b, c)


def part1(inp: str) -> str:
    program = parse(inp)
    return ",".join(map(str, program.run()))


def part2(inp: str) -> int:
    program = parse(inp)
    # Determine the modulus
    for i in range(10):
        modulus = 2**i
        program.init_a = modulus
        if len(program.run()) > 1:
            break
    assert isinstance(modulus, int)
    proc_a = {}
    for a in range(1024):
        program.init_a = a
        proc_a[a] = program.run()[0]

    target = program.ins[::-1]
    to_visit = [(0, 0)]
    i = 0
    while i < len(to_visit):
        a, index_a = to_visit[i]
        if index_a == len(target):
            return a
        for rem in range(modulus):
            new_a = a * modulus + rem
            if proc_a[new_a % 1024] == target[index_a]:
                to_visit.append((new_a, index_a + 1))
        i += 1
    raise ValueError("No solution found")