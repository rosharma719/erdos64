import random, subprocess, sys
sys.path.insert(0, "/home/user/erdos64/verifier")
import cycle_detect as cd

def random_graph_adj(n, p, rng):
    g = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                g[i].add(j); g[j].add(i)
    return g

def matrix_lines(n, g):
    return "\n".join(" ".join(str(1 if j in g[i] else 0) for j in range(n)) for i in range(n))

def main():
    rng = random.Random(999331)
    trials = 60
    blocks, expected = [], []
    for _ in range(trials):
        n = rng.randint(28, 38)
        p = rng.uniform(0.12, 0.22)
        g = random_graph_adj(n, p, rng)
        L = rng.choice([31, 32, n, n-1, 15, 16])
        L = min(L, n)
        blocks.append(f"{n}\n{matrix_lines(n, g)}\n{L}\n")
        expected.append(cd.has_cycle_len_dfs(g, L))
    inp = "".join(blocks)
    out = subprocess.run(["./test_pathrec"], input=inp, capture_output=True, text=True, check=True, timeout=600).stdout
    lines = [l for l in out.strip().splitlines() if l.strip()]
    assert len(lines) == trials
    dis = 0
    for i, line in enumerate(lines):
        L_out, has = line.split(); has = bool(int(has))
        if has != expected[i]:
            dis += 1; print(f"DISAGREE trial={i} L={L_out} cpp={has} py={expected[i]}")
    print(f"checked {trials} (graph,L) pairs at n up to 38 incl. L=31/32, {dis} disagreements")
    assert dis == 0
    print("PASS: primitive agrees at n up to 38, L up to 32")

if __name__ == "__main__":
    main()
