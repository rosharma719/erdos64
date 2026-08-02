"""
Track C additive-combinatorics study for Erdős #64.

A "book"/generalized theta of k internally-disjoint u-v paths with lengths
l_1..l_k realizes every cycle length l_i + l_j (i<j). Avoiding all power-of-two
cycles from such a book means: no two path lengths sum to a power of two.

Central question: how large can a set S of positive integers be with no two
DISTINCT elements summing to a power of two? If the max grows linearly in N
(positive density), then the pure additive/theta mechanism CANNOT by itself force
a power-of-two cycle from boundedly-many paths -- a decisive strategic fact.

We compute alpha(H_N) = max independent set of H_N, where V={1..N} and i~j iff
i+j is a power of two. Exact via CP-SAT.
"""
from ortools.sat.python import cp_model


def powers_of_two_upto(m):
    p, out = 1, []
    while p <= m:
        out.append(p)
        p *= 2
    return out


def build_edges(N):
    P = set(powers_of_two_upto(2 * N))
    edges = []
    for i in range(1, N + 1):
        for q in P:
            j = q - i
            if j > i and j <= N:  # distinct, j>i to avoid dup
                edges.append((i, j))
    return edges


def max_independent_set(N):
    edges = build_edges(N)
    m = cp_model.CpModel()
    x = {i: m.NewBoolVar(f"x{i}") for i in range(1, N + 1)}
    for (i, j) in edges:
        m.Add(x[i] + x[j] <= 1)
    m.Maximize(sum(x.values()))
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = 8
    s.parameters.max_time_in_seconds = 30
    st = s.Solve(m)
    chosen = [i for i in range(1, N + 1) if s.Value(x[i]) > 0.5]
    return len(chosen), chosen, cp_model.OPTIMAL == st


if __name__ == "__main__":
    print(f"{'N':>5} {'alpha':>6} {'alpha/N':>8} {'optimal':>8}")
    for N in [8, 16, 32, 64, 128, 256, 512]:
        a, chosen, opt = max_independent_set(N)
        print(f"{N:>5} {a:>6} {a/N:>8.3f} {str(opt):>8}")
        if N == 64:
            # show a concrete large sum-free set for inspection
            print("   example S (N=64):", chosen)
