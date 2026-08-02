import importlib.util
import sys
sys.path.insert(0, "/home/user/erdos64/tracks/graph-counterexample-q6-xerdjz/verifier")
import networkx as nx
from order30_quotient_marking_census import (
    triangle_expand, cycle_masks_and_lengths, eliminate_by_interval, all_markings
)
import numpy as np

spec = importlib.util.spec_from_file_location("trusted_cycle_detect", "/home/user/erdos64/verifier/cycle_detect.py")
cd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cd)

def nx_to_g(G):
    """Relabel to plain ints 0..n-1 (triangle_expand's marked-vertex stubs are
    tuples, which our trusted detector's sorted(g.keys()) can't compare)."""
    nodes = list(G.nodes())
    idx = {v: i for i, v in enumerate(nodes)}
    return {idx[v]: {idx[u] for u in G.neighbors(v)} for v in nodes}

def check_quotient(name, Q, k):
    n = Q.number_of_nodes()
    cmasks, clens = cycle_masks_and_lengths(Q)
    markings = all_markings(n, k)
    eliminated = eliminate_by_interval(cmasks, clens, markings)
    mismatches = 0
    for idx in range(markings.shape[0]):
        mask = int(markings[idx])
        marked = {v for v in range(n) if mask & (1 << v)}
        lifted = triangle_expand(Q, marked)
        g = nx_to_g(lifted)
        # ground truth: does the literal graph have a C4, C8, or C16, via our
        # own already-validated detector (independent implementation)?
        has_forbidden = any(cd.has_cycle_len_dfs(g, L) for L in (4, 8, 16) if L <= lifted.number_of_nodes())
        predicted_eliminated = bool(eliminated[idx])
        # predicted_eliminated should be True iff has_forbidden is True (exact claim)
        if predicted_eliminated != has_forbidden:
            mismatches += 1
            print(f"MISMATCH {name} marked={sorted(marked)} predicted_elim={predicted_eliminated} actual_has_forbidden={has_forbidden}")
    print(f"{name}: {markings.shape[0]} markings checked, {mismatches} mismatches")
    return mismatches

total_mm = 0
# K4: cubic, 4 vertices. k must be <=4; try k=1,2 (can't do triangle-lift with too few non-marked)
K4 = nx.complete_graph(4)
total_mm += check_quotient("K4 k=1", K4, 1)
total_mm += check_quotient("K4 k=2", K4, 2)

# K33 (bipartite cubic, 6 vertices)
K33 = nx.complete_bipartite_graph(3, 3)
total_mm += check_quotient("K33 k=1", K33, 1)
total_mm += check_quotient("K33 k=2", K33, 2)
total_mm += check_quotient("K33 k=3", K33, 3)

# Petersen graph (10 vertices, cubic, girth 5)
P = nx.petersen_graph()
total_mm += check_quotient("Petersen k=2", P, 2)
total_mm += check_quotient("Petersen k=3", P, 3)

# Cubic prism graph K3 x K2 (triangular prism, 6 vertices)
prism = nx.Graph()
prism.add_edges_from([(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)])
total_mm += check_quotient("Prism k=2", prism, 2)
total_mm += check_quotient("Prism k=3", prism, 3)

print(f"\nTOTAL MISMATCHES: {total_mm}")
assert total_mm == 0, "interval elimination logic disagrees with ground truth!"
print("PASS: interval elimination is exact on all tested small quotients")
