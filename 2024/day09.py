from tqdm import tqdm

debug = False

def parse(inp: str) -> list[int | None]:
    i = 0
    f = True
    disk = []
    for s in map(int, inp.strip()):
        if f:
            disk.extend([i] * s)
            i += 1
        else:
            disk.extend([None] * s)
        f = not f
    return disk


def compress_disk(disk: list[int | None]):
    while None in disk:
        last = disk.pop()
        if last is None:
            continue
        disk[disk.index(None)] = last

def checksum(disk: list[int | None]) -> int:
    return sum([i*a if a is not None else 0 for i,a in enumerate(disk)])

def print_disk(disk: list[int | None]):
    s = "".join(["." if c is None else str(c) for c in disk])
    print(s)

def part1(inp: str) -> int:
    disk = parse(inp)
    compress_disk(disk)
    if debug:
        print_disk(disk)
    return checksum(disk)

def get_first_block(disk: list[int | None], size: int) -> int | None:
    in_empty = False
    cur_id = None
    L = 0
    for i, c in enumerate(disk):
        if c is None:
            if in_empty:
                L += 1
            else:
                cur_id = i
                L = 1
                in_empty = True
            if L >= size:
                return cur_id
        else:
            in_empty = False
    return None


def compress_unfragmented(disk: list[int | None]):
    files = max(filter(lambda x: x is not None, disk))  # type: ignore
    for fid in tqdm(range(files, -1, -1)):
        pos = disk.index(fid)
        size = disk.count(fid)
        empty_block = get_first_block(disk, size)
        if empty_block is None or empty_block > pos:
            continue
        disk[pos:pos+size] = [None] * size
        disk[empty_block: empty_block + size] = [fid] * size

def part2(inp: str) -> int:
    disk = parse(inp)
    compress_unfragmented(disk)
    if debug:
        print_disk(disk)
    return checksum(disk)