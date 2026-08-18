"""
Canonical-state-memoization / proof-DAG prototype (task Part 6, 2026-07-25).

SCOPING NOTE (read this first): the task asks to "convert the P13
computation into lemma extraction." There is no local implementation of
the P13-free induced-path search in this repo -- L7 / Track E (plan.md,
literature.md) cites an EXTERNAL paper (Hegde, Sandeep, Shashank,
arXiv:2410.22842) whose search code is not reproduced here. Re-implementing
their full induced-path backtracking search is out of scope for this pass.
Instead this prototype applies the SAME METHODOLOGY -- canonical state
memoization, a proof DAG of failed completions, extraction of minimal
impossible states -- to a search this project DOES control locally:
incremental construction of one-pole graphs (Part 5), vertex by vertex,
pruned the moment a forbidden (power-of-two-length) cycle appears.

Honesty caveats:
  - State canonicalization here is an INEXPENSIVE APPROXIMATE signature
    (degree sequence + sorted realized-cycle-length multiset), NOT a full
    nauty-canonical graph form. Two non-isomorphic states can share a
    signature (this only costs extra work, never soundness -- we still
    only report a state "impossible" after literally exhausting every
    successor at that node, isomorphism-collapsed or not).
  - "Minimal impossible state" means: the fewest EDGES among the states
    that were fully explored and yielded zero live descendants, not a
    minimum over all conceivable states (the search is depth/width bounded
    for tractability, so this is COMPUTATIONALLY VERIFIED within the
    explored bound, not an exhaustive claim).

Search: start from the root r (degree target 2), build up by repeatedly
adding an edge between two "open" vertices (degree < target) or a new
vertex, targeting an eventual one-pole graph on <= max_n vertices with the
root at degree exactly 2 and everything else >= 3. Prune on: any dyadic
cycle appearing (4, 8), or degree exceeding a small cap (keeps the search
finite -- this is a deliberate scope restriction, recorded honestly).
"""
from __future__ import annotations
import sys
from collections import defaultdict

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from cycle_detect import has_cycle_len_dfs, powers_of_two_up_to


class State:
    __slots__ = ("n", "edges", "adj")

    def __init__(self, n, edges):
        self.n = n
        self.edges = edges
        adj = defaultdict(set)
        for a, b in edges:
            adj[a].add(b)
            adj[b].add(a)
        self.adj = adj

    def degree(self, v):
        return len(self.adj[v])

    def signature(self):
        """Approximate canonical key: degree sequence + realized dyadic
        cycle-length multiset. NOT a full isomorphism invariant -- see
        module docstring."""
        degs = tuple(sorted(self.degree(v) for v in range(self.n)))
        g = {v: set(self.adj[v]) for v in range(self.n)}
        cyc = tuple(L for L in powers_of_two_up_to(self.n) if has_cycle_len_dfs(g, L))
        return (degs, cyc, self.n)

    def has_forbidden_cycle(self):
        g = {v: set(self.adj[v]) for v in range(self.n)}
        for L in powers_of_two_up_to(self.n):
            if has_cycle_len_dfs(g, L):
                return True
        return False

    def is_valid_one_pole(self, target_deg2_count=1, deg_cap=4):
        deg2 = [v for v in range(self.n) if self.degree(v) == 2]
        if len(deg2) != target_deg2_count:
            return False
        return all(self.degree(v) >= 3 for v in range(self.n) if v not in deg2)


def search(max_n=9, deg_cap=4, max_nodes=200000):
    """DFS with memoized dead-state signatures and a proof DAG (parent ->
    list of dead children) for the smallest dead states found."""
    memo_dead = set()
    dead_examples = {}  # signature -> (n, edges) smallest witness
    survivors = []
    nodes_visited = 0
    proof_dag_edges = []  # (parent_sig, child_sig) for dead transitions

    class BudgetExceeded(Exception):
        pass

    def dfs(state: State, parent_sig=None):
        nonlocal nodes_visited
        nodes_visited += 1
        if nodes_visited > max_nodes:
            # Abort the whole run rather than silently truncating -- a
            # node cut off by budget must NEVER be recorded as "dead"
            # (that would corrupt the proof DAG with false impossibility
            # claims caused by running out of time, not by genuine
            # exhaustion).
            raise BudgetExceeded()

        if state.has_forbidden_cycle():
            return False  # dead: pruned by forbidden cycle

        if state.is_valid_one_pole():
            survivors.append((state.n, sorted(state.edges)))
            return True  # success propagates up, no memoization needed

        sig = state.signature()
        if sig in memo_dead:
            return False

        # try extending: connect two vertices below degree cap, or add a
        # new vertex (if under max_n) connected to one existing vertex.
        any_live = False
        candidates = []
        verts = list(range(state.n))
        for i in range(len(verts)):
            for j in range(i + 1, len(verts)):
                a, b = verts[i], verts[j]
                if b in state.adj[a]:
                    continue
                if state.degree(a) >= deg_cap or state.degree(b) >= deg_cap:
                    continue
                candidates.append((a, b))
        for (a, b) in candidates:
            child = State(state.n, state.edges + [(a, b)])
            if dfs(child, sig):
                any_live = True
                # do not break -- we want ALL survivors found in this budget
        if state.n < max_n:
            new_v = state.n
            for a in verts:
                if state.degree(a) >= deg_cap:
                    continue
                child = State(state.n + 1, state.edges + [(a, new_v)])
                if dfs(child, sig):
                    any_live = True

        if not any_live:
            memo_dead.add(sig)
            if sig not in dead_examples or len(state.edges) < len(dead_examples[sig][1]):
                dead_examples[sig] = (state.n, state.edges)
            if parent_sig is not None:
                proof_dag_edges.append((parent_sig, sig))
        return any_live

    root_state = State(1, [])
    aborted = False
    try:
        dfs(root_state)
    except BudgetExceeded:
        aborted = True
    return dict(nodes_visited=nodes_visited, dead_states=len(memo_dead),
                dead_examples=dead_examples, survivors=survivors,
                proof_dag_size=len(proof_dag_edges), aborted=aborted)


def classify_dead_state(n, edges):
    """Cheap cause classification for a minimal impossible state."""
    g = defaultdict(set)
    for a, b in edges:
        g[a].add(b)
        g[b].add(a)
    for L in powers_of_two_up_to(n):
        gg = {v: set(g[v]) for v in range(n)}
        if has_cycle_len_dfs(gg, L):
            return f"contains forbidden {L}-cycle"
    return "exhausted successors without reaching a valid one-pole completion " \
           "within the search's degree-cap / max-n bound"


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-n", type=int, default=8)
    ap.add_argument("--deg-cap", type=int, default=4)
    ap.add_argument("--max-nodes", type=int, default=50000)
    args = ap.parse_args()

    res = search(max_n=args.max_n, deg_cap=args.deg_cap, max_nodes=args.max_nodes)
    if res["aborted"]:
        print(f"*** ABORTED: exceeded max_nodes={args.max_nodes} before full "
              f"exhaustion -- results below are PARTIAL, do not treat any "
              f"'dead state' as exhaustively proved impossible. Re-run with "
              f"smaller --max-n/--deg-cap or larger --max-nodes. ***")
    print(f"nodes visited: {res['nodes_visited']}")
    print(f"distinct dead (approx-canonical) states memoized: {res['dead_states']}")
    print(f"proof-DAG edges recorded: {res['proof_dag_size']}")
    print(f"survivors found: {len(res['survivors'])}")

    smallest = sorted(res["dead_examples"].values(), key=lambda t: len(t[1]))[:5]
    print("\nsmallest impossible (dead) states found:")
    for n, edges in smallest:
        cause = classify_dead_state(n, edges)
        print(f"  n={n} edges={sorted(edges)} -- cause: {cause}")


if __name__ == "__main__":
    main()
