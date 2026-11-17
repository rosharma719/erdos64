"""Generate all 3-connected cubic graphs up to order N by bridging two distinct
edges (adjacent allowed) starting from K4, with isomorphism deduplication.
Writes gen3c_n{n}.g6.  Known counts (OEIS A204198): 1,2,4,14,57,341,2828,30468.
"""
import sys, itertools, networkx as nx
from collections import defaultdict

N = int(sys.argv[1]); out = sys.argv[2]

def bridge(g, e, f):
    h = g.copy(); n = len(g); x, y = n, n + 1
    (a, b), (c, d) = e, f
    h.remove_edge(a, b); h.remove_edge(c, d)
    h.add_edges_from([(a, x), (x, b), (c, y), (y, d), (x, y)])
    return h

import numpy as np
def key(g):
    A = nx.to_numpy_array(g)
    ev = tuple(np.round(np.linalg.eigvalsh(A), 6))
    A2 = A @ A; A3 = A2 @ A; A4 = A3 @ A
    loc = tuple(sorted(zip(np.round(np.diag(A3)).astype(int), np.round(np.diag(A4)).astype(int), np.round(np.diag(A4@A)).astype(int))))
    return (ev, loc)

level = [nx.complete_graph(4)]
counts = {4: 1}
with open(f"{out}/gen3c_n4.g6", "w") as fh:
    fh.write(nx.to_graph6_bytes(level[0], header=False).decode())
for n in range(6, N + 1, 2):
    buckets = defaultdict(list); new = []
    for g in level:
        for e, f in itertools.combinations(list(g.edges()), 2):
            h = bridge(g, e, f)
            k = key(h)
            if any(nx.is_isomorphic(h, o) for o in buckets[k]):
                continue
            buckets[k].append(h); new.append(h)
    level = new; counts[n] = len(level)
    assert all(nx.node_connectivity(h) >= 3 for h in level)
    with open(f"{out}/gen3c_n{n}.g6", "w") as fh:
        for h in level:
            fh.write(nx.to_graph6_bytes(nx.convert_node_labels_to_integers(h), header=False).decode())
    print(n, len(level), flush=True)
