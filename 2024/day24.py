
from collections import defaultdict
from typing import Callable


Gate = tuple[str, str, str, Callable[[int, int], int]]


def AND(a: int, b: int) -> int:
    return a & b


def OR(a: int, b: int) -> int:
    return a | b


def XOR(a: int, b: int) -> int:
    return a ^ b


Gatefuncs = {
    "AND": AND,
    "OR": OR,
    "XOR": XOR,
}


def print_gate(gate: Gate) -> None:
    print(f"{gate[0]} {gate[3].__name__} {gate[1]} -> {gate[2]}")


def parse(inp: str) -> tuple[dict[str, int], list[Gate]]:
    wireline, gatelines = inp.split("\n\n")[:2]
    wires = {}
    for line in wireline.splitlines():
        key, val = line.split(": ")
        wires[key] = int(val)
    gates = []
    for line in gatelines.splitlines():
        a, op, b, _, c = line.split()
        gates.append((a, b, c, Gatefuncs[op]))
    return wires, gates


def process_gates(wires: dict[str, int], gates: list[Gate]) -> None:
    known_wires = list(wires.keys())
    gate_inp = defaultdict(list)
    for gate in gates:
        gate_inp[gate[0]].append(gate)
        gate_inp[gate[1]].append(gate)
    i = 0
    while i < len(known_wires):
        wire = known_wires[i]
        for gate in gate_inp[wire]:
            if gate[0] in wires and gate[1] in wires and gate[2] not in wires:
                wires[gate[2]] = gate[3](wires[gate[0]], wires[gate[1]])
                known_wires.append(gate[2])
        i += 1


def calc_wire_score(wires: dict[str, int], var: str = "z") -> int:
    total = 0
    for key, val in wires.items():
        if not key.startswith(var):
            continue
        total += int(val * 2 ** int(key[1:]))
    return total


def check_adder(gates: list[Gate]) -> None:
    zmax = max(int(wire[2][1:]) for wire in gates if wire[2].startswith("z"))
    wire_names = {}
    for gate in gates:
        if set(gate[:2]) == {"x00", "y00"} and gate[3] is Gatefuncs["AND"]:
            wire_names["c01"] = gate[2]
    for i in range(1, zmax):
        gate_a, gate_b, gate_d, gate_z, gate_c = None, None, None, None, None
        try:
            for gate in gates:
                if (
                    set(gate[:2]) == {f"x{i:02}", f"y{i:02}"}
                    and gate[3] is Gatefuncs["XOR"]
                ):
                    gate_a = gate
                if (
                    set(gate[:2]) == {f"x{i:02}", f"y{i:02}"}
                    and gate[3] is Gatefuncs["AND"]
                ):
                    gate_b = gate
            if gate_a is None or gate_b is None:
                raise ValueError(f"No A or B gate found at {i}")
            for gate in gates:
                if (
                    set(gate[:2]) == {wire_names[f"c{i:02}"], gate_a[2]}
                    and gate[3] is Gatefuncs["AND"]
                ):
                    gate_d = gate
                if (
                    set(gate[:2]) == {wire_names[f"c{i:02}"], gate_a[2]}
                    and gate[3] is Gatefuncs["XOR"]
                ):
                    if gate[2] == f"z{i:02}":
                        gate_z = gate
                    else:
                        print_gate(gate)
        except KeyError:
            print(wire_names[f"c{i:02}"])
            if gate_a is not None:
                print_gate(gate_a)
            if gate_b is not None:
                print_gate(gate_b)
            if gate_d is not None:
                print_gate(gate_d)
            if gate_z is not None:
                print_gate(gate_z)
            raise
        if gate_d is None:
            print_gate(gate_a)
            print_gate(gate_b)
            print(wire_names[f"c{i:02}"])
            raise ValueError(f"No D (A&C) gate found at {i}")
        if gate_z is None:
            print_gate(gate_a)
            print_gate(gate_b)
            print_gate(gate_d)
            print(wire_names[f"c{i:02}"])
            raise ValueError(f"No Z (A^C) gate found at {i}")
        for gate in gates:
            if set(gate[:2]) == {gate_b[2], gate_d[2]} and gate[3] is Gatefuncs["OR"]:
                gate_c = gate
        if gate_c is None:
            print_gate(gate_a)
            print_gate(gate_b)
            print_gate(gate_d)
            print(wire_names[f"c{i:02}"])
            raise ValueError(f"No C (B|D) gate found at {i}")
        wire_names[f"c{i+1:02}"] = gate_c[2]


def part1(inp: str) -> int:
    wires, gates = parse(inp)
    process_gates(wires, gates)
    return calc_wire_score(wires)


def part2(inp: str) -> str:
    wires, gates = parse(inp)
    swaps = [("tst", "z05"), ("sps", "z11"), ("frt", "z23"), ("cgh", "pmd")]
    for i, gate in enumerate(gates):
        for swap in swaps:
            if gate[2] == swap[0]:
                gates[i] = gate[:2] + (swap[1], gate[3])
            elif gate[2] == swap[1]:
                gates[i] = gate[:2] + (swap[0], gate[3])
    process_gates(wires, gates)
    x = calc_wire_score(wires, "x")
    y = calc_wire_score(wires, "y")
    z = calc_wire_score(wires, "z")
    assert x + y == z, f"{x} + {y} != {z} == {x + y}"
    flat_swaps = sorted(item for sublist in swaps for item in sublist)
    return ",".join(flat_swaps)
    