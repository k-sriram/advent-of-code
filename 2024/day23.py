def parse(inp: str) -> list[tuple[str, str]]:
    connections = []
    for line in inp.splitlines():
        a, b = line.split("-")
        connections.append((min(a, b), max(a, b)))
        connections.sort()
    return connections


def get_nodes(conn: list[tuple[str, str]]) -> list[str]:
    nodes = set()
    for c in conn:
        for n in c:
            nodes.add(n)
    return sorted(nodes)


def get_triangles(conn: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    nodes = get_nodes(conn)
    triangles = []
    for a, b in conn:
        for c in nodes[nodes.index(b) + 1 :]:
            if (a, c) in conn and (b, c) in conn:
                triangles.append((a, b, c))
    return triangles


def bigger_cluster(cluster: list[tuple[str, ...]]) -> list[tuple[str, ...]]:
    new_cluster = []
    for i, clus0 in enumerate(cluster):
        for clus1 in cluster[i + 1 :]:
            if clus1[:-1] != clus0[:-1]:
                continue
            n_clus = clus0 + (clus1[-1],)
            if all(
                n_clus[:i] + n_clus[i + 1 :] in cluster
                for i in range(len(n_clus) - 3, -1, -1)
            ):
                new_cluster.append(n_clus)
    return new_cluster


def part1(inp: str) -> int:
    conn = parse(inp)
    triangles = get_triangles(conn)
    t_triangles = [t for t in triangles if any(n[0] == "t" for n in t)]
    return len(t_triangles)


def part2(inp: str) -> str:
    conn = parse(inp)
    clusters = get_triangles(conn)
    i = 3
    while clusters:
        big_cluster = clusters[0]
        print(i, (len(clusters)))
        clusters = bigger_cluster(clusters)
        i += 1
    return ",".join(sorted(big_cluster))