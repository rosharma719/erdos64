import os
import sys
# Repo-root resolution added 2026-08-18 during consolidation: these
# scripts moved out of external_review/ and previously hard-coded an
# absolute home directory.  Resolve relative to this file instead.
import os
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO_ROOT, "verifier"))
import cycle_detect as cd

edges_file = os.path.join(_REPO_ROOT, "data", "z3_lifts", "base0_markstroem.edges")
with open(edges_file) as f:
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
mat = [[0]*n for _ in range(n)]
g = {i: set() for i in range(n)}
for u, v in edges:
    mat[u][v] = mat[v][u] = 1
    g[u].add(v); g[v].add(u)

# Path fixed 2026-08-18 during consolidation (tree moved to
# tracks/external-audits/); write next to this script.
_HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_HERE, "base0_markstroem.mat"), "w") as out:
    for row in mat:
        out.write(" ".join(map(str, row)) + "\n")

# independently verify: cubic, and cycle spectrum (only C16 among powers of 2)
degs = [len(g[v]) for v in range(n)]
print("degrees:", set(degs))
for L in (4, 8, 16, 24):
    print(f"has C{L}:", cd.has_cycle_len_dfs(g, L))
