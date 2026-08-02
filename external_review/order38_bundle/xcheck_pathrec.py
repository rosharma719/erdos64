import random
import subprocess
import sys
sys.path.insert(0, "/home/user/erdos64/verifier")
import cycle_detect as cd

def random_graph_adj(n, p, rng):
    g = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                g[i].add(j)
                g[j].add(i)
    return g

def matrix_lines(n, g):
    rows = []
    for i in range(n):
        row = [1 if j in g[i] else 0 for j in range(n)]
        rows.append(" ".join(map(str, row)))
    return "\n".join(rows)

def main():
    rng = random.Random(20260802)
    trials = 300
    blocks = []
    expected = []
    for _ in range(trials):
        n = rng.randint(5, 24)
        p = rng.uniform(0.15, 0.6)
        g = random_graph_adj(n, p, rng)
        L = rng.randint(3, n)
        blocks.append(f"{n}\n{matrix_lines(n, g)}\n{L}\n")
        expected.append(cd.has_cycle_len_dfs(g, L))

    inp = "".join(blocks)
    out = subprocess.run(["./test_pathrec"], input=inp, capture_output=True, text=True, check=True).stdout
    lines = [l for l in out.strip().splitlines() if l.strip()]
    assert len(lines) == trials, f"{len(lines)} vs {trials}"
    disagreements = 0
    for i, line in enumerate(lines):
        L_out, has = line.split()
        has = bool(int(has))
        if has != expected[i]:
            disagreements += 1
            print(f"DISAGREE trial={i} L={L_out} cpp={has} py={expected[i]}")
    print(f"checked {trials} (graph,L) pairs, {disagreements} disagreements")
    assert disagreements == 0
    print("PASS: order38 pathrec/has_cycle_len primitive agrees with trusted detector")

if __name__ == "__main__":
    main()
