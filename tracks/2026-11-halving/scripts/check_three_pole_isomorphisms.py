#!/usr/bin/env python3
"""Port-marked isomorphism checks for the clean 3-pole classification.

Two separate claims are checked, and kept separate:
  (1) Identification: every rooted survivor of the pass VI Hamiltonian census
      (root_switching_certificates.json), with its root deleted, is isomorphic
      to one of the three clean poles in clean_three_poles_n_le_19.g6.
  (2) Agreement: the representatives in the audit file clean_pole_small_audit.json
      match the same three poles.
Neither check establishes uniqueness at 15 vertices. Uniqueness rests on the
exhaustive census recorded in three_pole_census_manifest.md.
Ports are marked explicitly (degree-2 vertices) even though any isomorphism of
such poles preserves them.
Usage: python3 check_three_pole_isomorphisms.py   (run from this directory)
"""
import json, os, sys
import networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = ["uniform H7", "skew H7", "H15"]
def marked(G):
    H = G.copy()
    for v in H: H.nodes[v]["port"] = H.degree(v) == 2
    return H
def load_ours():
    poles = [nx.from_graph6_bytes(l.strip().encode()) for l in open(os.path.join(HERE, "clean_three_poles_n_le_19.g6")) if l.strip()]
    assert len(poles) == 3
    for P in poles: assert sum(1 for v in P if P.degree(v) == 2) == 3
    return poles
def match(G, ours):
    return [NAMES[i] for i, H in enumerate(ours)
            if nx.is_isomorphic(marked(G), marked(H), node_match=lambda a, b: a["port"] == b["port"])]
def main():
    ours = load_ours(); ok = True
    print("(1) Hamiltonian census survivors, each root-critical vertex deleted:")
    cert = json.load(open(os.path.join(HERE, "root_switching_certificates.json")))["survivors"]
    for n in ("8", "16"):
        for s in cert[n]:
            S = nx.from_graph6_bytes(s["graph6"].encode())
            for r in s["root_critical_vertices"]:
                P = S.copy(); P.remove_node(r); m = match(P, ours)
                ok &= len(m) == 1
                print(f"   n={n} {s['graph6']} root {r}: {m}")
    print("(2) audit representatives:")
    audit = json.load(open(os.path.join(HERE, "clean_pole_small_audit.json")))
    reps = audit["census"]["7"]["representatives"] + [audit["one_known_15_vertex_example"]]
    for r in reps:
        G = nx.from_graph6_bytes(r["graph6"].encode())
        assert r["ports"] == sorted(v for v in G if G.degree(v) == 2), "stored ports are not the degree-2 vertices"
        m = match(G, ours); ok &= len(m) == 1
        print(f"   {r['graph6']}: {m}")
    print("ALL MATCH" if ok else "MISMATCH"); sys.exit(0 if ok else 1)
if __name__ == "__main__": main()
