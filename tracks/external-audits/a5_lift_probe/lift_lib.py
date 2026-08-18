"""
Independent Python reimplementation of the base-graph tree/cotree bookkeeping,
word computation, and lift construction from a5_breakout_solver_v2.cpp --
built from scratch by reading the C++ source, not copy-pasted from it, so it
serves as a genuine cross-check as well as a tool for deriving new cuts.
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


def load_base(path=EDGES_FILE):
    with open(path) as f:
        header = f.readline().split()
        n, m = int(header[0]), int(header[1])
        edges = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            u, v = map(int, line.split())
            edges.append((u, v) if u < v else (v, u))
    assert len(edges) == m
    return n, edges


class BaseGraph:
    def __init__(self, path=EDGES_FILE):
        self.n, self.E = load_base(path)
        # replicate rd()'s adjacency list construction: for i<j in increasing
        # (i,j) order, append j to a[i] and i to a[j] -- this fixes the exact
        # traversal order the C++ BFS uses.
        self.a = [[] for _ in range(self.n)]
        self.eid = {}
        for idx, (i, j) in enumerate(self.E):
            self.eid[(i, j)] = idx
            self.a[i].append(j)
            self.a[j].append(i)
        # BFS from vertex 0 using a[u] traversal order (matches C++ main()).
        pa = [-1] * self.n
        pe = [-1] * self.n
        pa[0] = 0
        order = [0]
        qi = 0
        while qi < len(order):
            u = order[qi]
            qi += 1
            for v in self.a[u]:
                if pa[v] < 0:
                    pa[v] = u
                    pe[v] = self.eid[(u, v) if u < v else (v, u)]
                    order.append(v)
        tree_edge_ids = set(pe[v] for v in range(self.n) if v != 0)
        self.vo = {}  # edge_id -> cotree var index, or absent if tree edge
        self.cot = []  # cotree edge list, in b.E order
        for idx, e in enumerate(self.E):
            if idx not in tree_edge_ids:
                self.vo[idx] = len(self.cot)
                self.cot.append(e)
        self.r = len(self.cot)

    def word(self, walk):
        """walk: list of vertices v0,v1,...,v_{L-1} (closed, so edge v_{L-1}-v0 included).
        Returns list of signed ints (var_index+1, sign = direction) exactly as
        the C++ word() lambda computes, skipping tree edges."""
        w = []
        L = len(walk)
        for i in range(L):
            u, v = walk[i], walk[(i + 1) % L]
            e = self.eid[(u, v) if u < v else (v, u)]
            if e in self.vo:
                z = self.vo[e]
                w.append((1 if u < v else -1) * (z + 1))
        return w


IDENT = (0, 1, 2, 3, 4)


def inv_perm(p):
    q = [0] * 5
    for i, x in enumerate(p):
        q[x] = i
    return tuple(q)


def compose_word(word, assignment):
    """assignment: dict cotree_var_index -> tuple perm (image of 0..4).
    Returns the product permutation (as in C++ prod(): cur, then apply each
    step's permutation, tracking where each of 0..4 ends up)."""
    cur = list(IDENT)
    for zz in word:
        z = abs(zz) - 1
        p = assignment[z] if zz > 0 else inv_perm(assignment[z])
        cur = [p[c] for c in cur]
    return tuple(cur)


def is_5cycle(p):
    x = 0
    for k in range(1, 6):
        x = p[x]
        if x == 0:
            return k == 5
    return False


def all_closed_walks(bg, length, start):
    """All closed walks of exactly `length` edges starting and ending at `start`
    (revisits allowed; only immediate backtrack over the same edge is skipped,
    since it always contributes identity and can't create a new violation)."""
    out = []

    def rec(cur, prev, remaining, path):
        if remaining == 0:
            if cur == start:
                out.append(list(path))
            return
        for w in bg.a[cur]:
            if w == prev:
                continue
            path.append(w)
            rec(w, cur, remaining - 1, path)
            path.pop()

    rec(start, -1, length, [start])
    return out


def build_lift(bg, assignment):
    n = bg.n
    g = {i: set() for i in range(5 * n)}

    def node(v, s):
        return v * 5 + s

    for idx, (u, v) in enumerate(bg.E):
        perm = assignment.get(bg.vo.get(idx, -1), IDENT)
        for s in range(5):
            a, b = node(u, s), node(v, perm[s])
            g[a].add(b)
            g[b].add(a)
    return g


def lift_witness_to_walk(witness):
    """witness: list of raw lift node ids (v*5+s) from cd.find_cycle_len_dfs.
    Returns (base_walk_vertices, start_sheet)."""
    decoded = [divmod(node, 5) for node in witness]
    walk = [bv for bv, s in decoded]
    start_sheet = decoded[0][1]
    return walk, start_sheet
