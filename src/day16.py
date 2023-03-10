from typing import Dict, Tuple, List

import networkx as nx

calls = 0


def build_graph(lines):
    """Build a graph from lines where each node has a flow rate and state."""
    G = nx.Graph()

    for line in lines:
        this_node = line[6:8]
        flow = line[23:line.index(";")]
        leads_to = [x.strip() for x in line[line.index("valve") + len("valves"):].split(",")]

        G.add_node(this_node, flow=int(flow), on=False)
        G.add_weighted_edges_from([(this_node, that_node, 1) for that_node in leads_to])

    return G


def remove_node(G, n):
    """Remove a node from the graph and merge any edges from it."""
    edges = list(nx.edges(G, n))

    # for each pair of edges, add a new edge
    pairs = [(a, b) for idx, a in enumerate(edges) for b in edges[idx + 1:]]
    for pair in pairs:
        neighbour1 = pair[0][0] if pair[0][1] == n else pair[0][1]
        neighbour2 = pair[1][0] if pair[1][1] == n else pair[1][1]
        G.add_weighted_edges_from(
            [
                (neighbour1, neighbour2, G.edges[pair[0]]["weight"] + G.edges[pair[1]]["weight"])
            ]
        )

    # removing this node also removes all edges from it
    G.remove_node(n)
    return G


def prune_graph(G):
    """Remove nodes with zero flow (except AA)."""

    nodes = list(G.nodes)
    for n in nodes:
        if G.nodes[n]["flow"] == 0 and n != "AA":
            G = remove_node(G, n)

    return G


def max_pressure(start: str, nodes: Dict[str, int], distances: Dict[str, Dict[str, int]], mins):
    """The max pressure that can be released from a bunch of nodes that are distances apart in mins time."""

    # Out of curiosity, track the number of calls
    global calls
    calls += 1

    # We will activate all of the valves we visit except that the starting node may have no flow
    if nodes[start]:
        mins -= 1
        pressure_from_activating = nodes[start] * mins
    else:
        pressure_from_activating = 0

    # The nodes we might visit next
    other_nodes = nodes.copy()
    # We don't want to return to this node
    other_nodes.pop(start)

    max_pressures = 0
    visited_nodes = []
    for node in other_nodes:

        # Only try other nodes if they are reachable
        if distances[start][node] < mins:
            maximum, nodes = max_pressure(node, other_nodes, distances, mins - distances[start][node])
            if maximum > max_pressures:
                visited_nodes = nodes
                max_pressures = maximum

    visited_nodes.append(start)
    return pressure_from_activating + max_pressures, visited_nodes


def one(lines):
    """Calculate the pressure released."""
    G = build_graph(lines)

    # Shortest paths between nodes
    distances = dict(nx.all_pairs_shortest_path_length(G))

    # Nodes with non-zero flow rate (plus the starting node)
    nodes = {node: G.nodes[node]["flow"] for node in G.nodes if G.nodes[node]["flow"] > 0 or node == "AA"}

    max_p, path = max_pressure("AA", nodes, distances, 30)
    print("path", path[::-1])
    return max_p


def sublists(xs: List) -> List[List]:
    """Generate all pairs of lists that can be made from one list.

    See https://stackoverflow.com/a/29657078"""
    l = len(xs)
    for i in range(1 << l):
        incl, excl = [], []
        for j in range(l):
            if i & (1 << j):
                incl.append(xs[j])
            else:
                excl.append(xs[j])
        yield (incl, excl)


def get_max_pressure_two(distances):
    """Get a function for part II."""
    def max_pressure_two(nodes: Dict[str, int]):
        """Find the best way to assign work to me and the elephant."""

        # 2^n of these!
        node_list = list(nodes.keys())
        node_list.pop(node_list.index("AA"))

        # Generate all of the ways we could divide up the nodes
        # (each node only needs to be turned on once, by the elephant or me)
        possible_splits = sublists(node_list)

        best_pressure = 0
        best_split = None
        for split in possible_splits:

            # e.g. the elephant might get ["AA", "BB", "II", "GG"] and I might get {"AA", "HH"],
            p1, n1 = max_pressure("AA", {"AA": nodes["AA"],
                                         **{key: value for key, value in nodes.items() if key in split[0]}}, distances,
                                  26)
            p2, n2 = max_pressure("AA", {"AA": nodes["AA"],
                                         **{key: value for key, value in nodes.items() if key in split[1]}}, distances,
                                  26)

            if p1 + p2 > best_pressure:
                best_pressure = p1 + p2
                best_split = n1, n2

        return best_pressure, best_split

    return max_pressure_two


def two(lines):
    """Calculate the pressure released by the elephant and you."""
    G = build_graph(lines)

    # Shortest paths between nodes
    distances = dict(nx.all_pairs_shortest_path_length(G))

    # Nodes with non-zero flow rates
    nodes = {node: G.nodes[node]["flow"] for node in G.nodes if G.nodes[node]["flow"] > 0 or node == "AA"}

    max_p, path = get_max_pressure_two(distances)(nodes)
    print("path", path[::-1])
    return max_p


def main():
    with open("../inputs/day16.txt", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
    print("one:", one(lines))
    print("two:", two(lines))


if __name__ == "__main__":
    main()
