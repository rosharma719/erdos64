#!/usr/bin/env python3
"""Independent NetworkX recount for a saved Type-T matching near miss."""

import argparse
import collections
import hashlib
import json

import networkx as nx

from type_t_port_core_export import build_core


def norm_edge(u, v):
    return (u, v) if u < v else (v, u)


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("input")
parser.add_argument("--output")
args = parser.parse_args()
path = args.input
payload = json.load(open(path))
q = payload["parameters"]
core = build_core(q["j"], q["a"], q["c"])
matching = [norm_edge(*item) for item in payload["matching_edges"]]
deficient = set(core.deficient_vertices())

assert len(matching) == len(set(matching)) == len(deficient) // 2 == 78
assert set(v for edge in matching for v in edge) == deficient
assert not set(matching).intersection(core.edges)

graph = nx.Graph()
graph.add_nodes_from(range(core.order))
graph.add_edges_from(core.edges)
graph.add_edges_from(matching)
assert nx.is_connected(graph)
assert nx.number_of_selfloops(graph) == 0
assert graph.number_of_edges() == len(core.edges) + len(matching)
degrees = collections.Counter(dict(graph.degree()).values())
assert degrees == {3: core.order - 1, 4: 1}

# NetworkX's bounded Johnson iterator is independent of the repository DFS.
spectrum = collections.Counter()
participation = collections.Counter()
matching_set = set(matching)
for cycle in nx.simple_cycles(graph, length_bound=16):
    length = len(cycle)
    if length in (4, 8, 16):
        spectrum[length] += 1
        if length == 16:
            edges = {
                norm_edge(cycle[i], cycle[(i + 1) % length])
                for i in range(length)
            }
            participation.update(edges & matching_set)

raw = open(path, "rb").read()
matching_blob = json.dumps(sorted(matching), separators=(",", ":")).encode()
graph6 = nx.to_graph6_bytes(graph, header=False).strip()
sparse6 = nx.to_sparse6_bytes(graph, header=False).strip()
result = {
    "source": path,
    "source_sha256": hashlib.sha256(raw).hexdigest(),
    "matching_sha256": hashlib.sha256(matching_blob).hexdigest(),
    "graph6_sha256": hashlib.sha256(graph6).hexdigest(),
    "graph6": graph6.decode(),
    "sparse6": sparse6.decode(),
    "order": graph.number_of_nodes(),
    "size": graph.number_of_edges(),
    "connected": nx.is_connected(graph),
    "degree_counts": dict(sorted(degrees.items())),
    "networkx_exact_profile": {str(k): spectrum[k] for k in (4, 8, 16)},
    "C16_matching_edge_participation": {
        "edges": len(participation),
        "minimum": min(participation.values()),
        "median": sorted(participation.values())[len(participation) // 2],
        "maximum": max(participation.values()),
    },
}
rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
if args.output:
    with open(args.output, "w") as destination:
        destination.write(rendered)
else:
    print(rendered, end="")
