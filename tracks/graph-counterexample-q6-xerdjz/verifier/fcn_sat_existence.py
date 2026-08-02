#!/usr/bin/env python3
"""FC-N / F-N by direct SAT *graph existence* search (not generate-and-filter).

Question decided by this module, for parameters (n, d_x):

    Does there exist a simple graph B on n vertices with a designated terminal
    x with d_B(x) = d_x exactly, a designated terminal y != x with
    d_B(y) >= d_x, d_B(v) >= 3 for every v not in {x,y}, xy not in E(B),
    B + xy 2-connected, and B containing no C4 and no C8?

"UNSAT" is exactly the statement F-n (d_x=1) / FC-n (d_x=2) at order n.
This is the same predicate that `verifier/type_a_order12_f12.py` (d_x=1,
n=12) and `verifier/type_c_fcn_series.py` (d_x=2, n<=15) settle by
`nauty-geng` enumeration; those two results are the ground truth this solver
is validated against before being used prospectively (`--validate`).

ARCHITECTURE (why this is different from the geng pipelines)
-----------------------------------------------------------
Raw enumeration blows up: n=15 alone already has 2,625,442 raw candidates.
Here the *graph itself* is the decision variable: one Boolean e_{ij} per
unordered pair, and the solver either constructs a satisfying graph or proves
none exists.

  * degree conditions        -> cardinality constraints on the incidence rows
  * C4-freeness              -> EAGER: every pair of vertices has at most one
                                common neighbour (exactly equivalent to
                                C4-freeness in a simple graph)
  * C8-freeness              -> LAZY (CEGAR): solve, read off the candidate
                                graph, enumerate its 8-cycles, and add one
                                8-literal blocking clause per 8-cycle found.
                                Eager C8 encoding is hopeless -- it needs
                                2520*C(n,8) clauses (5.1e8 at n=21).
  * 2-connectivity of B+xy   -> LAZY: on a C4/C8-free candidate that has a cut
                                vertex c splitting V\{c} into S | T, add the
                                globally valid clause "some edge of B+xy
                                crosses S|T".  (Also the analogous clause for
                                a disconnected candidate.)
  * symmetry breaking        -> the vertices {2,...,n-1} are fully
                                interchangeable (identical constraints), so we
                                require the edge-variable serialisation to be
                                lex-maximal over every transposition of that
                                block.  Optional (`--no-symbreak`) so that the
                                validation can be run both ways.

SOUNDNESS OF "UNSAT"
--------------------
Every clause ever added -- eager or lazy -- is satisfied by *every* genuine
solution of the stated problem:

  * an 8-cycle blocking clause is satisfied because a genuine solution is
    C8-free, so it cannot contain that particular 8-cycle;
  * a lazy cut clause "some edge crosses S|T after deleting c" is satisfied
    because a genuine solution has B+xy 2-connected, so (B+xy)-c is connected
    for every c, so every bipartition of V\{c} is crossed;
  * the symmetry-breaking constraints are satisfied by at least one member of
    each relabelling orbit, and the true solution set is closed under
    relabelling of {2,...,n-1} (identical constraints), and the lazy clauses
    above are satisfied by *all* labellings, so orbit-closure is preserved.

Hence UNSAT of the accumulated formula implies no such graph B exists.
SAT is only ever reported after the witness graph has been re-verified from
scratch (independent C4/C8 detection via `cycle_detect.py`'s DFS routine plus
networkx, degree conditions, and `networkx.is_biconnected`).  A candidate that
fails re-verification is a bug and is reported as such, never as a survivor.

Usage
-----
    # decide one instance
    python verifier/fcn_sat_existence.py solve --n 15 --dx 2 --time-limit 600

    # replay the already-proven ground truth (F12 and FC-15)
    python verifier/fcn_sat_existence.py validate

    # push the (2,*) series forward
    python verifier/fcn_sat_existence.py sweep --dx 2 --from 13 --to 21 \
        --time-limit 600
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import threading
import time
from pathlib import Path

import networkx as nx
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_detect import from_edges, has_cycle_len_dfs  # noqa: E402

# glucose42 is the default because it is the strongest backend in this PySAT
# build that supports `solve_limited(expect_interrupt=True)` -- i.e. that lets
# the per-instance wall-clock budget actually be enforced *inside* a single
# solve call.  CaDiCaL and Lingeling raise NotImplementedError there, so with
# those backends the time limit can only be checked between CEGAR iterations
# (see `_solve_with_budget`), which is honest but coarser.
DEFAULT_SOLVER = "glucose42"


# ---------------------------------------------------------------------------
# 8-cycle enumeration on a concrete candidate graph
# ---------------------------------------------------------------------------

def enumerate_cycles_of_length(adj: dict[int, set[int]], length: int) -> list[list[int]]:
    """Every simple cycle with exactly `length` vertices, each reported once.

    Rooted at the cycle's unique minimum vertex, with orientation fixed by
    requiring the second vertex to be smaller than the last -- so each cycle is
    emitted exactly once, not 2*length times.
    """
    out: list[list[int]] = []
    verts = sorted(adj)
    for s in verts:
        allowed = {v for v in adj if v > s}
        path = [s]
        used = {s}

        def rec(cur: int, depth: int) -> None:
            if depth == length:
                if s in adj[cur] and path[1] < path[-1]:
                    out.append(list(path))
                return
            for nxt in adj[cur]:
                if nxt in allowed and nxt not in used:
                    used.add(nxt)
                    path.append(nxt)
                    rec(nxt, depth + 1)
                    path.pop()
                    used.discard(nxt)

        rec(s, 1)
    return out


def enumerate_open_paths(adj: dict[int, set[int]], length: int,
                         cap: int | None = None) -> list[list[int]]:
    """Every simple path on `length` vertices whose two endpoints are NOT
    adjacent, each reported once (up to reversal).

    Such a path is a "near-miss" forbidden cycle: adding the single missing
    chord would create a cycle of exactly `length`.  Blocking it is a valid
    constraint of the original problem (a genuine solution has no cycle of that
    length at all, so it cannot contain all `length` of those edges).

    Unlike `enumerate_cycles_of_length`, a path canNOT be rooted at its minimum
    vertex, because that vertex may be internal.  So paths are grown from every
    start vertex and de-duplicated by orientation (`path[0] < path[-1]`).

    NOTE: this is disabled by default (`--nearmiss 0`).  Benchmarking at n=17
    showed it is a net loss -- it cut iterations only 4124 -> 3538 while adding
    ~1e6 clauses, and wall time went 64s -> 103s.  Kept because the option is
    cheap and the trade-off may flip at other orders, not because any reported
    result uses it.
    """
    out: list[list[int]] = []
    for s in sorted(adj):
        path = [s]
        used = {s}

        def rec(cur: int) -> bool:
            if len(path) == length:
                if s not in adj[cur] and path[0] < path[-1]:
                    out.append(list(path))
                    if cap is not None and len(out) >= cap:
                        return True
                return False
            for nxt in adj[cur]:
                if nxt not in used:
                    used.add(nxt)
                    path.append(nxt)
                    stop = rec(nxt)
                    path.pop()
                    used.discard(nxt)
                    if stop:
                        return True
            return False

        if rec(s):
            break
    return out



def adjacency_from_edges(n: int, edges: list[tuple[int, int]]) -> dict[int, set[int]]:
    adj: dict[int, set[int]] = {v: set() for v in range(n)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


# ---------------------------------------------------------------------------
# The SAT model
# ---------------------------------------------------------------------------

class FCNExistenceModel:
    """Edge-variable SAT encoding of the FC-n / F-n existence question."""

    def __init__(self, n: int, dx: int, symbreak: bool = True,
                 require_2conn: bool = True, solver_name: str = DEFAULT_SOLVER,
                 forbidden: tuple[int, ...] = (4, 8),
                 min_internal_degree: int = 3):
        if n < 4:
            raise ValueError("n must be at least 4")
        if dx not in (1, 2):
            raise ValueError("dx must be 1 or 2")
        self.n = n
        self.dx = dx
        self.symbreak = symbreak
        self.require_2conn = require_2conn
        self.forbidden = tuple(sorted(forbidden))
        self.min_internal_degree = min_internal_degree
        self.x = 0
        self.y = 1

        self.pool = IDPool()
        # e(i,j), i<j -- allocate first so ids 1..C(n,2) are the edge vars
        self.evar: dict[tuple[int, int], int] = {}
        for i, j in itertools.combinations(range(n), 2):
            self.evar[(i, j)] = self.pool.id(("e", i, j))

        self.clauses: list[list[int]] = []
        self._build_base()

        self.solver = Solver(name=solver_name, bootstrap_with=self.clauses)
        self.solver_name = solver_name
        self.interruptible = solver_name.lower() not in (
            "cadical103", "cadical153", "cadical195", "lingeling")
        self.n_base_clauses = len(self.clauses)
        self.n_lazy_cycle = 0
        self.n_lazy_cut = 0
        self.n_lazy_nearmiss = 0
        self.n_lazy_block = 0
        self.iterations = 0

    # -- helpers ------------------------------------------------------------

    def e(self, i: int, j: int) -> int:
        return self.evar[(i, j)] if i < j else self.evar[(j, i)]

    def _add(self, clause: list[int]) -> None:
        self.clauses.append(clause)

    def _card(self, lits: list[int], bound: int, kind: str) -> None:
        if kind == "equals":
            cnf = CardEnc.equals(lits=lits, bound=bound, vpool=self.pool,
                                 encoding=EncType.seqcounter)
        elif kind == "atleast":
            cnf = CardEnc.atleast(lits=lits, bound=bound, vpool=self.pool,
                                  encoding=EncType.seqcounter)
        else:
            raise ValueError(kind)
        for cl in cnf.clauses:
            self._add(list(cl))

    # -- base encoding ------------------------------------------------------

    def _build_base(self) -> None:
        n, dx = self.n, self.dx

        # (1) xy not in E(B)
        self._add([-self.e(self.x, self.y)])

        # (2) degrees
        for v in range(n):
            lits = [self.e(v, w) for w in range(n) if w != v]
            if v == self.x:
                self._card(lits, dx, "equals")
            elif v == self.y:
                self._card(lits, dx, "atleast")
            else:
                self._card(lits, self.min_internal_degree, "atleast")

        # (3) C4-freeness  <=>  every vertex pair has at most one common
        #     neighbour.  Encoded directly as: for every {a,b} and every
        #     {c,d} disjoint from it, not all four of ac,bc,ad,bd present.
        if 4 in self.forbidden:
            for a, b in itertools.combinations(range(n), 2):
                others = [w for w in range(n) if w != a and w != b]
                for c, d in itertools.combinations(others, 2):
                    self._add([-self.e(a, c), -self.e(b, c),
                               -self.e(a, d), -self.e(b, d)])

        # (4) symmetry breaking over Sym({2,...,n-1})
        if self.symbreak and n >= 4:
            block = list(range(2, n))
            for u, v in itertools.combinations(block, 2):
                self._lex_ge_under_transposition(u, v)

    def _lex_ge_under_transposition(self, u: int, v: int) -> None:
        """Require serialise(A) >=_lex serialise(A^tau) for tau = (u v).

        The lex-maximum member of each relabelling orbit satisfies this for
        every transposition, so imposing it for all of them keeps at least one
        representative of every orbit -- a sound partial symmetry break.
        """
        def tau(w: int) -> int:
            return v if w == u else (u if w == v else w)

        lhs: list[int] = []
        rhs: list[int] = []
        for i, j in itertools.combinations(range(self.n), 2):
            p = self.evar[(i, j)]
            ti, tj = tau(i), tau(j)
            q = self.e(ti, tj)
            if p == q:
                continue  # always equal: never decides the comparison
            lhs.append(p)
            rhs.append(q)
        self._lex_ge(lhs, rhs)

    def _lex_ge(self, a: list[int], b: list[int]) -> None:
        """Clauses asserting the bit vector a is lexicographically >= b."""
        assert len(a) == len(b)
        if not a:
            return
        eq_prev: int | None = None  # None encodes the constant TRUE
        for idx in range(len(a)):
            ai, bi = a[idx], b[idx]
            # forbid: equal-so-far AND a_i=0 AND b_i=1
            base = [ai, -bi]
            self._add(base if eq_prev is None else [-eq_prev] + base)
            if idx == len(a) - 1:
                break
            eq_cur = self.pool.id(("lexeq", tuple(a), idx))
            # (eq_prev AND a_i == b_i) -> eq_cur
            pre: list[int] = [] if eq_prev is None else [-eq_prev]
            self._add(pre + [-ai, -bi, eq_cur])
            self._add(pre + [ai, bi, eq_cur])
            eq_prev = eq_cur

    # -- reading a model ----------------------------------------------------

    def edges_from_model(self, model: list[int]) -> list[tuple[int, int]]:
        pos = set(l for l in model if l > 0)
        return [(i, j) for (i, j), var in sorted(self.evar.items()) if var in pos]

    # -- lazy clause addition ----------------------------------------------

    def block_cycle(self, cycle: list[int]) -> None:
        lits = []
        k = len(cycle)
        for idx in range(k):
            lits.append(-self.e(cycle[idx], cycle[(idx + 1) % k]))
        self.solver.add_clause(lits)
        self.n_lazy_cycle += 1

    def add_cut_clause(self, side_s: set[int], side_t: set[int]) -> None:
        """B+xy 2-connected => after deleting any vertex the rest is connected,
        so every bipartition S|T of the remaining vertices is crossed by an
        edge of B+xy.  Valid for every genuine solution; xy itself counts, so
        the pair (x,y) is skipped as an available crossing edge only when it is
        genuinely absent -- it is always present in B+xy, so if x and y lie on
        opposite sides the bipartition is automatically crossed and no clause
        is emitted."""
        if (self.x in side_s and self.y in side_t) or (self.x in side_t and self.y in side_s):
            return
        lits = [self.e(a, b) for a in side_s for b in side_t]
        if not lits:
            return
        self.solver.add_clause(lits)
        self.n_lazy_cut += 1

    def block_path_closure(self, path: list[int]) -> None:
        """Forbid the cycle obtained by closing `path` with its missing chord."""
        k = len(path)
        lits = [-self.e(path[i], path[i + 1]) for i in range(k - 1)]
        lits.append(-self.e(path[-1], path[0]))
        self.solver.add_clause(lits)
        self.n_lazy_nearmiss += 1

    def block_exact_graph(self, edges: list[tuple[int, int]]) -> None:
        """Last-resort blocking clause forbidding one exact edge set."""
        present = set(edges)
        lits = []
        for (i, j), var in self.evar.items():
            lits.append(-var if (i, j) in present else var)
        self.solver.add_clause(lits)
        self.n_lazy_block += 1


# ---------------------------------------------------------------------------
# Independent re-verification of a claimed witness
# ---------------------------------------------------------------------------

def verify_witness(n: int, dx: int, edges: list[tuple[int, int]],
                   forbidden: tuple[int, ...] = (4, 8),
                   min_internal_degree: int = 3,
                   require_2conn: bool = True) -> dict:
    """Check a claimed survivor from scratch, using routines that share no code
    with the SAT encoding: networkx for the structural conditions, and BOTH
    `cycle_detect.has_cycle_len_dfs` and `networkx.simple_cycles` for the
    forbidden-cycle conditions (the same dual-detector discipline the geng
    pipelines use)."""
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)
    x, y = 0, 1
    report: dict = {"n": n, "dx": dx, "forbidden": list(forbidden),
                    "edges": sorted(tuple(sorted(e)) for e in edges),
                    "degrees": [G.degree(v) for v in range(n)]}

    report["deg_x_exact"] = (G.degree(x) == dx)
    report["deg_y_ok"] = (G.degree(y) >= dx)
    report["internal_deg_ok"] = all(G.degree(v) >= min_internal_degree
                                    for v in range(n) if v not in (x, y))
    report["xy_absent"] = not G.has_edge(x, y)

    closure = G.copy()
    closure.add_edge(x, y)
    report["closure_2connected"] = bool(nx.is_biconnected(closure)) if n >= 3 else False

    # Forbidden cycles, by two independent detectors.
    d = from_edges(n, [tuple(e) for e in G.edges()])
    bound = max(forbidden)
    nx_lengths = {len(c) for c in nx.simple_cycles(G, length_bound=bound)}
    detectors_agree = True
    cycle_free = True
    per_length = {}
    for L in forbidden:
        dfs_hit = has_cycle_len_dfs(d, L)
        nx_hit = (L in nx_lengths)
        per_length[L] = {"dfs": bool(dfs_hit), "networkx": bool(nx_hit)}
        detectors_agree = detectors_agree and (bool(dfs_hit) == bool(nx_hit))
        cycle_free = cycle_free and not dfs_hit
    report["cycle_detectors"] = per_length
    report["detectors_agree"] = detectors_agree
    report["cycle_free"] = cycle_free

    checks = [report["deg_x_exact"], report["deg_y_ok"], report["internal_deg_ok"],
              report["xy_absent"], report["detectors_agree"], report["cycle_free"]]
    if require_2conn:
        checks.append(report["closure_2connected"])
    report["is_genuine_survivor"] = all(checks)
    return report


def predicate_holds(G: nx.Graph, x: int, y: int, dx: int,
                    forbidden: tuple[int, ...] = (4, 8),
                    min_internal_degree: int = 3,
                    require_2conn: bool = True) -> bool:
    """The FC-n predicate, evaluated directly on a concrete graph with a
    concrete choice of terminals.  Used only by the brute-force cross-check;
    shares no code with the SAT encoding."""
    n = G.number_of_nodes()
    if G.degree(x) != dx or G.degree(y) < dx:
        return False
    if any(G.degree(v) < min_internal_degree for v in G if v not in (x, y)):
        return False
    if G.has_edge(x, y):
        return False
    if require_2conn:
        closure = G.copy()
        closure.add_edge(x, y)
        if not nx.is_biconnected(closure):
            return False
    lengths = {len(c) for c in nx.simple_cycles(G, length_bound=max(forbidden))}
    return not any(L in lengths for L in forbidden)


# ---------------------------------------------------------------------------
# The CEGAR search loop
# ---------------------------------------------------------------------------

def _solve_with_budget(model: "FCNExistenceModel", seconds: float) -> bool | None:
    """One SAT call with a wall-clock budget.  Returns True/False/None(=timeout).

    Uses the interruptible path when the backend supports it; otherwise falls
    back to an uninterruptible solve (the budget is then only enforced between
    CEGAR iterations, which is reported honestly by the caller)."""
    if not model.interruptible:
        return model.solver.solve()
    timer = threading.Timer(seconds, model.solver.interrupt)
    timer.start()
    try:
        return model.solver.solve_limited(expect_interrupt=True)
    finally:
        timer.cancel()
        try:
            model.solver.clear_interrupt()
        except NotImplementedError:
            pass


def search(n: int, dx: int, time_limit: float = 600.0, symbreak: bool = True,
           require_2conn: bool = True, solver_name: str = DEFAULT_SOLVER,
           forbidden: tuple[int, ...] = (4, 8), min_internal_degree: int = 3,
           nearmiss: int = 0, verbose: bool = False) -> dict:
    """Decide the FC-n/F-n existence question.

    Returns a dict with `status` in {"UNSAT", "SAT", "TIMEOUT", "BUG"}.
    """
    t0 = time.time()
    forbidden = tuple(sorted(forbidden))
    model = FCNExistenceModel(n, dx, symbreak=symbreak,
                              require_2conn=require_2conn, solver_name=solver_name,
                              forbidden=forbidden,
                              min_internal_degree=min_internal_degree)
    build_seconds = time.time() - t0

    status = "TIMEOUT"
    witness = None
    witness_report = None

    while True:
        remaining = time_limit - (time.time() - t0)
        if remaining <= 0:
            status = "TIMEOUT"
            break

        res = _solve_with_budget(model, remaining)
        model.iterations += 1

        if res is None:
            status = "TIMEOUT"
            break
        if res is False:
            status = "UNSAT"
            break

        edges = model.edges_from_model(model.solver.get_model())
        adj = adjacency_from_edges(n, edges)

        # C4 is encoded eagerly, so a C4 in a candidate means the eager
        # encoding is wrong -- report it as a bug, never silently repair it.
        if 4 in forbidden:
            c4s = enumerate_cycles_of_length(adj, 4)
            if c4s:
                model.solver.delete()
                return {"status": "BUG", "n": n, "dx": dx,
                        "detail": f"eager C4 encoding violated: {c4s[0]}",
                        "edges": edges, "elapsed_seconds": time.time() - t0}

        # Lazily block every forbidden cycle actually present in the candidate.
        found = 0
        for L in forbidden:
            if L == 4:
                continue  # already eager
            for cyc in enumerate_cycles_of_length(adj, L):
                model.block_cycle(cyc)
                found += 1
        # Optionally also block "near misses": simple paths on L vertices whose
        # endpoints are non-adjacent.  Valid for the same reason (a genuine
        # solution has no C_L at all), and far more informative -- it stops the
        # solver from converging one edge-flip at a time.
        if nearmiss:
            for L in forbidden:
                if L == 4:
                    continue
                for pth in enumerate_open_paths(adj, L, cap=nearmiss):
                    model.block_path_closure(pth)
        if found:
            if verbose and model.iterations % 200 == 0:
                print(f"    iter {model.iterations}: +{found} cycle clauses "
                      f"(total {model.n_lazy_cycle}), {time.time() - t0:.1f}s",
                      flush=True)
            continue

        # Candidate avoids every forbidden cycle.  Check the side conditions.
        rep = verify_witness(n, dx, edges, forbidden=forbidden,
                             min_internal_degree=min_internal_degree,
                             require_2conn=require_2conn)
        if rep["is_genuine_survivor"]:
            status = "SAT"
            witness = edges
            witness_report = rep
            break

        if not (rep["deg_x_exact"] and rep["deg_y_ok"] and rep["internal_deg_ok"]
                and rep["xy_absent"] and rep["cycle_free"]
                and rep["detectors_agree"]):
            model.solver.delete()
            return {"status": "BUG", "n": n, "dx": dx,
                    "detail": "candidate violates an eagerly-encoded condition",
                    "report": rep, "elapsed_seconds": time.time() - t0}

        # Only 2-connectivity of B+xy failed: add lazy cut clause(s).
        added = _add_2conn_clauses(model, n, edges)
        if added == 0:
            model.block_exact_graph(edges)
        if verbose:
            print(f"    iter {model.iterations}: candidate not 2-connected, "
                  f"+{added} cut clauses", flush=True)

    out = {
        "status": status, "n": n, "dx": dx, "symbreak": symbreak,
        "require_2conn": require_2conn, "forbidden": list(forbidden),
        "min_internal_degree": min_internal_degree, "solver": solver_name,
        "edge_vars": len(model.evar), "base_clauses": model.n_base_clauses,
        "lazy_cycle_clauses": model.n_lazy_cycle, "lazy_cut_clauses": model.n_lazy_cut,
        "lazy_nearmiss_clauses": model.n_lazy_nearmiss, "nearmiss_cap": nearmiss,
        "lazy_block_clauses": model.n_lazy_block,
        "iterations": model.iterations,
        "build_seconds": round(build_seconds, 2),
        "elapsed_seconds": round(time.time() - t0, 2),
    }
    if witness is not None:
        out["witness_edges"] = witness
        out["witness_report"] = witness_report
        out["witness_graph6"] = _graph6(n, witness)
    model.solver.delete()
    return out


def _add_2conn_clauses(model: FCNExistenceModel, n: int,
                       edges: list[tuple[int, int]]) -> int:
    """Emit lazy cut clauses witnessing that B+xy must stay connected after
    deleting any single vertex."""
    closure = nx.Graph()
    closure.add_nodes_from(range(n))
    closure.add_edges_from(edges)
    closure.add_edge(model.x, model.y)

    added = 0
    if not nx.is_connected(closure):
        comps = list(nx.connected_components(closure))
        s = set(comps[0])
        t = set(range(n)) - s
        before = model.n_lazy_cut
        model.add_cut_clause(s, t)
        added += model.n_lazy_cut - before
        return added

    for c in range(n):
        h = closure.copy()
        h.remove_node(c)
        if h.number_of_nodes() and not nx.is_connected(h):
            comps = list(nx.connected_components(h))
            s = set(comps[0])
            t = set(h.nodes()) - s
            before = model.n_lazy_cut
            model.add_cut_clause(s, t)
            added += model.n_lazy_cut - before
    return added


def _graph6(n: int, edges: list[tuple[int, int]]) -> str:
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)
    return nx.to_graph6_bytes(G, header=False).decode().strip()


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

GROUND_TRUTH = [
    # (dx, n, expected)  -- from f12_order12_result.md (F9/F11/F12 series) and
    # fcn_order15_result.md (FC-15).  All are "no such graph exists".
    *[(1, n, "UNSAT") for n in range(5, 13)],
    *[(2, n, "UNSAT") for n in range(5, 16)],
]


def cmd_solve(args: argparse.Namespace) -> None:
    r = search(args.n, args.dx, time_limit=args.time_limit,
               symbreak=not args.no_symbreak, require_2conn=not args.no_2conn,
               solver_name=args.solver, nearmiss=args.nearmiss,
               forbidden=tuple(int(t) for t in args.forbid.split(",")),
               verbose=args.verbose)
    print(json.dumps(r, indent=2, default=str))


def cmd_validate(args: argparse.Namespace) -> None:
    print("Validating the SAT existence solver against already-proven ground truth")
    print("  d_x=1, n=5..12  -> F9/F11/F12   (expect UNSAT everywhere)")
    print("  d_x=2, n=5..15  -> FC-15        (expect UNSAT everywhere)")
    print()
    header = (f"{'d_x':>4} {'n':>4} {'symbrk':>7} {'expect':>8} {'got':>8} "
              f"{'iters':>7} {'cyccl':>8} {'cutcl':>7} {'secs':>9}  verdict")
    print(header)
    ok = True
    rows = []
    for symbreak in ([True, False] if args.both_modes else [True]):
        for dx, n, expected in GROUND_TRUTH:
            if args.max_n and n > args.max_n:
                continue
            r = search(n, dx, time_limit=args.time_limit, symbreak=symbreak,
                       verbose=args.verbose)
            good = (r["status"] == expected)
            ok = ok and good
            rows.append({**r, "expected": expected, "match": good})
            print(f"{dx:>4} {n:>4} {str(symbreak):>7} {expected:>8} {r['status']:>8} "
                  f"{r['iterations']:>7} {r['lazy_cycle_clauses']:>8} "
                  f"{r['lazy_cut_clauses']:>7} {r['elapsed_seconds']:>9.2f}  "
                  f"{'MATCH' if good else '*** MISMATCH ***'}", flush=True)
    print()
    print("VALIDATION PASSED -- solver reproduces F12 and FC-15 exactly"
          if ok else "VALIDATION FAILED -- do not trust prospective runs")
    if args.out:
        Path(args.out).write_text(json.dumps(rows, indent=2, default=str))


def cmd_sweep(args: argparse.Namespace) -> None:
    print(f"Prospective sweep: d_x={args.dx}, n={args.start}..{args.end}, "
          f"time limit {args.time_limit}s/instance, symbreak={not args.no_symbreak}")
    print(f"{'n':>4} {'status':>8} {'iters':>8} {'cyccl':>9} {'cutcl':>7} "
          f"{'basecl':>9} {'secs':>9}")
    rows = []
    for n in range(args.start, args.end + 1):
        r = search(n, args.dx, time_limit=args.time_limit,
                   symbreak=not args.no_symbreak, solver_name=args.solver,
                   nearmiss=args.nearmiss,
                   forbidden=tuple(int(t) for t in args.forbid.split(",")),
                   verbose=args.verbose)
        rows.append(r)
        print(f"{n:>4} {r['status']:>8} {r['iterations']:>8} "
              f"{r['lazy_cycle_clauses']:>9} {r['lazy_cut_clauses']:>7} "
              f"{r['base_clauses']:>9} {r['elapsed_seconds']:>9.2f}", flush=True)
        if r["status"] == "SAT":
            print("  *** SURVIVOR FOUND -- re-verification report ***")
            print(json.dumps(r["witness_report"], indent=4, default=str))
            print(f"  graph6: {r['witness_graph6']}")
        if r["status"] == "BUG":
            print("  *** ENCODING BUG ***")
            print(json.dumps(r, indent=4, default=str))
            break
        if args.out:
            Path(args.out).write_text(json.dumps(rows, indent=2, default=str))
    if args.out:
        Path(args.out).write_text(json.dumps(rows, indent=2, default=str))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("solve")
    ps.add_argument("--n", type=int, required=True)
    ps.add_argument("--dx", type=int, required=True, choices=(1, 2))
    ps.add_argument("--time-limit", type=float, default=600.0)
    ps.add_argument("--no-symbreak", action="store_true")
    ps.add_argument("--no-2conn", action="store_true")
    ps.add_argument("--forbid", default="4,8",
                    help="comma-separated forbidden cycle lengths "
                         "(default 4,8 = the FC-N/F-N proposition; use "
                         "4,8,16 for the full power-of-two set at n<32)")
    ps.add_argument("--nearmiss", type=int, default=0,
                    help="also block up to N near-miss cycles (open L-vertex "
                         "paths) per iteration; 0 disables")
    ps.add_argument("--solver", default=DEFAULT_SOLVER)
    ps.add_argument("--verbose", action="store_true")
    ps.set_defaults(func=cmd_solve)

    pv = sub.add_parser("validate")
    pv.add_argument("--time-limit", type=float, default=600.0)
    pv.add_argument("--max-n", type=int, default=0)
    pv.add_argument("--both-modes", action="store_true",
                    help="also re-run every instance with symmetry breaking off")
    pv.add_argument("--out", default="")
    pv.add_argument("--verbose", action="store_true")
    pv.set_defaults(func=cmd_validate)

    pw = sub.add_parser("sweep")
    pw.add_argument("--dx", type=int, default=2, choices=(1, 2))
    pw.add_argument("--from", dest="start", type=int, required=True)
    pw.add_argument("--to", dest="end", type=int, required=True)
    pw.add_argument("--time-limit", type=float, default=600.0)
    pw.add_argument("--no-symbreak", action="store_true")
    pw.add_argument("--nearmiss", type=int, default=0)
    pw.add_argument("--forbid", default="4,8")
    pw.add_argument("--solver", default=DEFAULT_SOLVER)
    pw.add_argument("--out", default="")
    pw.add_argument("--verbose", action="store_true")
    pw.set_defaults(func=cmd_sweep)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
