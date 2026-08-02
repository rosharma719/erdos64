#!/usr/bin/env python3
"""Split a biconnected cubic g6 catalog into 3-connected vs strictly-2-connected,
by exact nx.node_connectivity(G) >= 3, matching the method used for the
order-30 quotient census's order-16/18/20 catalogs (see order30_quotient_census.md).
"""
import sys
import gzip
import networkx as nx

inp, out3, out2 = sys.argv[1], sys.argv[2], sys.argv[3]
opener = gzip.open if inp.endswith(".gz") else open
n3 = n2 = 0
with opener(inp, "rt") as f, open(out3, "w") as f3, open(out2, "w") as f2:
    for i, line in enumerate(f):
        line = line.strip()
        if not line:
            continue
        g = nx.from_graph6_bytes(line.encode())
        if nx.node_connectivity(g) >= 3:
            f3.write(line + "\n")
            n3 += 1
        else:
            f2.write(line + "\n")
            n2 += 1
        if (i + 1) % 100000 == 0:
            print(f"  processed {i+1}, 3-connected={n3} strict2={n2}", file=sys.stderr)
print(f"done: 3-connected={n3} strictly-2-connected={n2} total={n3+n2}")
