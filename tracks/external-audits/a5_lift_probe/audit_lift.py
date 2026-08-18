"""
Independently materialize the A5-permutation lift of base0_markstroem from a
solver's FOUND assignment, and literally check it for C4/C8/C16/C32/C64 using
our own already-trusted cycle_detect.py -- no code or claims from the
external solver's own output are trusted for the cycle-length verdict.
"""
import sys
# Repo-root resolution added 2026-08-18 during consolidation: these
# scripts moved out of external_review/ and previously hard-coded an
# absolute home directory.  Resolve relative to this file instead.
import os
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO_ROOT, "verifier"))
import cycle_detect as cd

EDGES_FILE = os.path.join(_REPO_ROOT, "data", "z3_lifts", "base0_markstroem.edges")

def load_base():
    with open(EDGES_FILE) as f:
        header = f.readline().split()
        n, m = int(header[0]), int(header[1])
        edges = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            u, v = map(int, line.split())
            edges.append((u, v))
    assert len(edges) == m
    return n, edges

def load_assignment(path):
    """Parse a solver FOUND block: lines 'u v p0 p1 p2 p3 p4'."""
    assign = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("FOUND"):
                continue
            parts = line.split()
            u, v = int(parts[0]), int(parts[1])
            perm = tuple(int(x) for x in parts[2:7])
            assign[(u, v)] = perm
    return assign

def build_lift(n, edges, assign):
    """5 sheets per base vertex; cotree edges use the assigned permutation
    (low->high applies perm forward), tree (unassigned) edges use identity."""
    g = {i: set() for i in range(5 * n)}
    def node(v, s):
        return v * 5 + s
    n_cotree = 0
    for (u, v) in edges:
        lo, hi = (u, v) if u < v else (v, u)
        perm = assign.get((lo, hi))
        if perm is None:
            perm = (0, 1, 2, 3, 4)  # tree edge: identity voltage
        else:
            n_cotree += 1
        for s in range(5):
            a, b = node(lo, s), node(hi, perm[s])
            g[a].add(b)
            g[b].add(a)
    return g, n_cotree

def main():
    assignment_path = sys.argv[1] if len(sys.argv) > 1 else "out.log"
    n, edges = load_base()
    assign = load_assignment(assignment_path)
    g, n_cotree = build_lift(n, edges, assign)
    order = len(g)
    size = sum(len(nb) for nb in g.values()) // 2
    degs = set(len(nb) for nb in g.values())
    print(f"cotree edges assigned: {n_cotree} (expect 13)")
    print(f"lift order={order} size={size} degrees={degs}")
    for L in (4, 8, 16, 32, 64):
        if L > order:
            continue
        has = cd.has_cycle_len_dfs(g, L)
        print(f"has C{L}: {has}")
        if has:
            witness = cd.find_cycle_len_dfs(g, L)
            print(f"  witness (base-vertex, sheet) pairs: {[(v//5, v%5) for v in witness]}")

if __name__ == "__main__":
    main()
