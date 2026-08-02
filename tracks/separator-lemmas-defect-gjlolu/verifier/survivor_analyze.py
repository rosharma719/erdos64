#!/usr/bin/env python3
"""survivor_analyze.py '<graph6>' [<graph6> ...]
Full diagnostic on any 4-or-8 survivor (per the survivor-handling protocol):
simplicity, connectedness, degree sequence / cubicity, C4 & C8 absence
(re-verified independently), C16 presence, girth, diameter, |Aut|, and the full
cycle-length spectrum. Also writes g6/s6/edgelist copies. Uses the trusted DFS
detector plus networkx as an independent cross-check."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
from cycle_detect import from_edges, has_cycle_len_dfs, has_cycle_len_nx

def cycle_spectrum(G):
    # all simple-cycle lengths present, via networkx (undirected simple_cycles)
    lengths = set()
    n = G.number_of_nodes()
    for c in nx.simple_cycles(G, length_bound=n):
        if len(c) >= 3:
            lengths.add(len(c))
    return sorted(lengths)

def analyze(g6, idx, outdir):
    G = nx.from_graph6_bytes(g6.encode() if isinstance(g6, str) else g6)
    n = G.number_of_nodes()
    edges = list(G.edges())
    g = from_edges(n, edges)
    degs = sorted((d for _, d in G.degree()), reverse=True)
    rep = {
        "graph6": nx.to_graph6_bytes(G, header=False).decode().strip(),
        "n": n, "m": G.number_of_edges(),
        "simple": (not G.is_multigraph()) and nx.number_of_selfloops(G) == 0,
        "connected": nx.is_connected(G),
        "degree_sequence": degs,
        "cubic": degs == [3] * n,
        "has_C4_dfs": has_cycle_len_dfs(g, 4), "has_C4_nx": has_cycle_len_nx(g, 4),
        "has_C8_dfs": has_cycle_len_dfs(g, 8), "has_C8_nx": has_cycle_len_nx(g, 8),
        "has_C16_dfs": has_cycle_len_dfs(g, 16) if n >= 16 else False,
        "girth": (min(cycle_spectrum(G)) if G.number_of_edges() else None),
        "diameter": (nx.diameter(G) if nx.is_connected(G) else None),
        "aut_group_size": sum(1 for _ in GraphMatcher(G, G).isomorphisms_iter()),
        "cycle_length_spectrum": cycle_spectrum(G),
    }
    rep["is_4or8_survivor"] = (not rep["has_C4_dfs"]) and (not rep["has_C8_dfs"])
    rep["erdos_gyarfas_counterexample"] = rep["is_4or8_survivor"] and not rep["has_C16_dfs"]
    if outdir:
        os.makedirs(outdir, exist_ok=True)
        base = os.path.join(outdir, f"survivor_{idx}")
        with open(base + ".g6", "w") as f: f.write(rep["graph6"] + "\n")
        with open(base + ".s6", "w") as f: f.write(nx.to_sparse6_bytes(G, header=False).decode())
        with open(base + ".edgelist", "w") as f:
            for a, b in edges: f.write(f"{a} {b}\n")
    return rep

if __name__ == "__main__":
    import json
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    outdir = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--out=")), None)
    for i, g6 in enumerate(args):
        print(json.dumps(analyze(g6, i, outdir), indent=2))
