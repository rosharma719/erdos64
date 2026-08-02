#!/usr/bin/env python3
"""Brute-force cross-validation of the SAT graph-existence encoding.

Two kinds of check, both required before the SAT solver may be used
prospectively:

  A. EXACT AGREEMENT ON SMALL ORDERS.  For every n where `nauty-geng` can
     enumerate all graphs outright, decide the FC-n predicate by brute force
     (every graph, every ordered terminal pair (x,y)) and compare with the SAT
     solver's SAT/UNSAT verdict.  Run over several parameter settings, not just
     the two of real interest, so that the comparison actually exercises both
     answers.

  B. POSITIVE CONTROLS.  A solver with a bug that over-constrains would report
     UNSAT everywhere and would sail through any all-UNSAT validation suite.
     So the suite deliberately includes parameter settings where survivors DO
     exist (weaker forbidden-cycle sets, weaker degree floors); the SAT solver
     must find one, and the witness must pass independent re-verification AND
     be confirmed against the brute-force answer.

Usage: python verifier/test_fcn_sat_existence.py [--quick]
"""

from __future__ import annotations

import argparse
import itertools
import subprocess
import sys
import time
from pathlib import Path

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_detect import from_edges, has_cycle_len_dfs  # noqa: E402
from fcn_sat_existence import (  # noqa: E402
    FCNExistenceModel,
    adjacency_from_edges,
    enumerate_cycles_of_length,
    predicate_holds,
    search,
    verify_witness,
)


# ---------------------------------------------------------------------------
# Brute force reference
# ---------------------------------------------------------------------------

def all_graphs(n: int):
    """Every graph on n vertices up to isomorphism, via nauty-geng (streamed)."""
    proc = subprocess.Popen(["nauty-geng", "-q", str(n)],
                            stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        line = line.strip()
        if line:
            yield nx.from_graph6_bytes(line.encode())
    proc.wait()


def brute_force_exists(n: int, dx: int, forbidden: tuple[int, ...],
                       min_internal_degree: int, require_2conn: bool
                       ) -> tuple[bool, object]:
    """True iff some graph on n vertices admits terminals (x,y) satisfying the
    predicate.  Tries every graph and every ordered pair of distinct vertices --
    no assumption whatsoever about the degree sequence's shape (in particular no
    assumption that both terminals have degree exactly d_x, which is the exact
    parity trap documented in fcn_order15_result.md).

    Two graph-level prefilters are applied first.  Both are exact, not
    heuristic: the forbidden-cycle condition does not mention (x,y) at all, and
    the degree condition forces at least n-2 vertices to have degree >=
    min_internal_degree whichever pair is chosen (only x and y are exempt).
    Skipping a graph that fails either can therefore never skip a survivor."""
    for G in all_graphs(n):
        # Degree prefilter first (O(n), rejects most graphs instantly).
        if sum(1 for v in G if G.degree(v) >= min_internal_degree) < n - 2:
            continue
        # Then the forbidden-cycle prefilter, using the SHORT-CIRCUITING
        # detector rather than enumerating every cycle -- enumerating all
        # cycles up to length 8 on a dense 9-vertex graph is hopeless, while
        # "does a C4 exist" is answered almost immediately.
        d = from_edges(n, [tuple(e) for e in G.edges()])
        if any(has_cycle_len_dfs(d, L) for L in forbidden):
            continue
        for x, y in itertools.permutations(range(n), 2):
            if predicate_holds(G, x, y, dx, forbidden=forbidden,
                               min_internal_degree=min_internal_degree,
                               require_2conn=require_2conn):
                return True, (nx.to_graph6_bytes(G, header=False).decode().strip(), x, y)
    return False, None


# ---------------------------------------------------------------------------
# Unit checks on the encoding pieces
# ---------------------------------------------------------------------------

def check_cycle_enumerator() -> list[str]:
    """`enumerate_cycles_of_length` must agree exactly with networkx, counting
    each cycle once."""
    failures = []
    import random
    random.seed(12345)
    for trial in range(300):
        n = random.randint(5, 11)
        p = random.uniform(0.2, 0.55)
        G = nx.gnp_random_graph(n, p, seed=random.randint(0, 10 ** 9))
        adj = {v: set(G[v]) for v in G}
        for L in (3, 4, 5, 6, 8):
            mine = enumerate_cycles_of_length(adj, L)
            theirs = [c for c in nx.simple_cycles(G, length_bound=L) if len(c) == L]
            if len(mine) != len(theirs):
                failures.append(f"cycle count mismatch n={n} L={L}: "
                                f"{len(mine)} vs {len(theirs)}")
            # every reported cycle must really be a cycle of that length
            for c in mine:
                if len(set(c)) != L:
                    failures.append(f"reported non-simple cycle {c}")
                    break
                if any(c[(i + 1) % L] not in adj[c[i]] for i in range(L)):
                    failures.append(f"reported non-adjacent cycle {c}")
                    break
    return failures


def check_symmetry_breaking_is_sound(n: int, dx: int, forbidden: tuple[int, ...],
                                     min_internal_degree: int) -> list[str]:
    """Symmetry breaking must not change the SAT/UNSAT verdict.  Run every
    small instance both with and without it."""
    failures = []
    with_sb = search(n, dx, time_limit=120, symbreak=True, forbidden=forbidden,
                     min_internal_degree=min_internal_degree)
    without_sb = search(n, dx, time_limit=120, symbreak=False, forbidden=forbidden,
                        min_internal_degree=min_internal_degree)
    if with_sb["status"] != without_sb["status"]:
        failures.append(f"symmetry breaking changed the verdict at n={n} dx={dx} "
                        f"forbidden={forbidden} mind={min_internal_degree}: "
                        f"{with_sb['status']} vs {without_sb['status']}")
    return failures


# ---------------------------------------------------------------------------
# Main suite
# ---------------------------------------------------------------------------

# (n, dx, forbidden, min_internal_degree, require_2conn)
# geng enumerates all graphs on <=9 vertices quickly (274,668 at n=9).
def build_cases(quick: bool) -> list[tuple]:
    max_n = 8 if quick else 9
    cases = []
    for n in range(5, max_n + 1):
        for dx in (1, 2):
            # the real predicate
            cases.append((n, dx, (4, 8), 3, True))
            # positive-control variants where survivors are expected to exist
            cases.append((n, dx, (4,), 3, True))
            cases.append((n, dx, (4, 8), 2, True))
            cases.append((n, dx, (8,), 3, True))
            cases.append((n, dx, (4, 8), 3, False))
    return cases


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()

    all_failures: list[str] = []

    print("=" * 78)
    print("1. cycle enumerator vs networkx (300 random graphs, L in {3,4,5,6,8})")
    print("=" * 78)
    f = check_cycle_enumerator()
    all_failures += f
    print("  FAIL:" if f else "  OK -- exact agreement on every graph and length")
    for line in f[:10]:
        print("   ", line)

    print()
    print("=" * 78)
    print("2. SAT verdict vs exhaustive brute force (geng over ALL graphs, ALL")
    print("   ordered terminal pairs).  Includes positive controls -- settings")
    print("   where survivors must exist -- so an over-constrained encoding")
    print("   cannot pass by answering UNSAT everywhere.")
    print("=" * 78)
    hdr = (f"{'n':>3} {'dx':>3} {'forbid':>10} {'mind':>5} {'2conn':>6} "
           f"{'brute':>7} {'sat':>8} {'secs':>7}  verdict")
    print(hdr)

    n_sat_cases = 0
    for (n, dx, forbidden, mind, req2c) in build_cases(args.quick):
        t0 = time.time()
        bf, bf_witness = brute_force_exists(n, dx, forbidden, mind, req2c)
        r = search(n, dx, time_limit=300, symbreak=True, require_2conn=req2c,
                   forbidden=forbidden, min_internal_degree=mind)
        got = r["status"]
        expected = "SAT" if bf else "UNSAT"
        good = (got == expected)
        if got == "SAT":
            n_sat_cases += 1
            rep = r["witness_report"]
            if not rep["is_genuine_survivor"]:
                good = False
                all_failures.append(f"n={n} dx={dx}: SAT witness failed re-verification")
        if not good:
            all_failures.append(
                f"MISMATCH n={n} dx={dx} forbidden={forbidden} mind={mind} "
                f"2conn={req2c}: brute={expected} sat={got} "
                f"(brute witness {bf_witness})")
        print(f"{n:>3} {dx:>3} {str(forbidden):>10} {mind:>5} {str(req2c):>6} "
              f"{expected:>7} {got:>8} {time.time() - t0:>7.1f}  "
              f"{'ok' if good else '*** MISMATCH ***'}", flush=True)

    print()
    print(f"  positive controls that actually returned SAT: {n_sat_cases}")
    if n_sat_cases == 0:
        all_failures.append("no case returned SAT -- the suite has no positive "
                            "control power, do not trust an all-UNSAT result")

    print()
    print("=" * 78)
    print("3. symmetry breaking must not change any verdict")
    print("=" * 78)
    for (n, dx, forbidden, mind, req2c) in build_cases(args.quick):
        if not req2c:
            continue
        f = check_symmetry_breaking_is_sound(n, dx, forbidden, mind)
        all_failures += f
        for line in f:
            print("   ", line)
    print("  OK" if not all_failures else "  see failures above")

    print()
    print("=" * 78)
    if all_failures:
        print(f"FAILED: {len(all_failures)} problem(s)")
        for line in all_failures:
            print("  -", line)
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
