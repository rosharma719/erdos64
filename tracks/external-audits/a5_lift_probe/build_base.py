import sys
sys.path.insert(0, "/home/user/erdos64/verifier")
import cycle_detect as cd

edges_file = "/home/user/erdos64/tracks/global-core-z3-lifts/data/z3_lifts/base0_markstroem.edges"
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

with open("/home/user/erdos64/external_review/a5_lift_probe/base0_markstroem.mat", "w") as out:
    for row in mat:
        out.write(" ".join(map(str, row)) + "\n")

# independently verify: cubic, and cycle spectrum (only C16 among powers of 2)
degs = [len(g[v]) for v in range(n)]
print("degrees:", set(degs))
for L in (4, 8, 16, 24):
    print(f"has C{L}:", cd.has_cycle_len_dfs(g, L))
