"""
One-pole graph search (Erdos #64 redirection, 2026-07-25, task Part 5).

A "one-pole graph" H: exactly one root vertex of degree 2, every other
vertex has degree >= 3, simple, connected. A survivor that ALSO has no
cycle of length a power of two immediately yields a counterexample to
Erdos-Gyarfas: take two copies of H and identify their roots (S4's
"doubling" construction, proved in lemmas.md) -- the glued graph has
min degree >= 3 everywhere (root becomes degree 4) and, because the two
copies share only the root vertex, every simple cycle stays inside one
copy (same argument as S4/S5), so it inherits H's forbidden-cycle-freeness.

This script generates candidates via `geng -c -d2` (connected, min degree
>=2), filters to "exactly one vertex of degree 2, rest >=3", then checks
the dyadic cycle spectrum with the project's validated DFS detector
(cycle_detect.has_cycle_len_dfs). See one_pole_verify.py for the
independent cross-check (networkx-based detector + explicit doubling
re-verification) that must agree before any survivor is trusted.
"""
from __future__ import annotations
import subprocess
import sys
import json

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from cycle_detect import from_edges, powers_of_two_up_to, has_cycle_len_dfs, Graph


def read_graph6_line(line: str) -> Graph:
    import networkx as nx
    G = nx.from_graph6_bytes(line.strip().encode())
    n = G.number_of_nodes()
    return from_edges(n, list(G.edges()))


def is_one_pole(g: Graph) -> tuple[bool, int | None]:
    """Return (True, root) iff exactly one vertex has degree 2 and every
    other vertex has degree >=3 (degree <2 disqualifies entirely, and
    >=2 degree-2 vertices disqualifies -- 'one' pole means exactly one)."""
    deg2 = [v for v in g if len(g[v]) == 2]
    others_ok = all(len(g[v]) >= 3 for v in g if v not in deg2)
    if len(deg2) == 1 and others_ok and all(len(g[v]) >= 2 for v in g):
        return True, deg2[0]
    return False, None


def run_geng(n: int):
    """Stream geng output line by line instead of buffering the whole
    stream in memory (buffering was the bottleneck observed at n=10 --
    see experiments.md E9)."""
    cmd = ["geng", "-c", "-d2", str(n)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        line = line.strip()
        if line:
            yield line
    proc.wait()


def check_candidate(g: Graph, root: int) -> dict:
    n = len(g)
    spectrum = {L: has_cycle_len_dfs(g, L) for L in powers_of_two_up_to(n)}
    missing = [L for L, present in spectrum.items() if not present]
    is_survivor = len(missing) == len(spectrum)  # ALL dyadic lengths missing
    return dict(n=n, root=root, present=[L for L, p in spectrum.items() if p],
                missing=missing, is_survivor=is_survivor)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=5)
    ap.add_argument("--nmax", type=int, default=14)
    args = ap.parse_args()

    total_one_pole = 0
    survivors = []
    for n in range(args.nmin, args.nmax + 1):
        n_this = 0
        n_total = 0
        for g6 in run_geng(n):
            n_total += 1
            g = read_graph6_line(g6)
            ok, root = is_one_pole(g)
            if not ok:
                continue
            n_this += 1
            total_one_pole += 1
            st = check_candidate(g, root)
            if st["is_survivor"]:
                survivors.append((n, g6, root, st))
                print(f"!!! SURVIVOR at n={n}: g6={g6} root={root} -- "
                      f"NO power-of-two cycle found. Verify independently!")
            if n_total % 200000 == 0:
                print(f"  ...n={n} progress: {n_total} graphs read, "
                      f"{n_this} one-pole so far", flush=True)
        print(f"n={n}: {n_total} connected min-deg>=2 graphs, "
              f"{n_this} are one-pole (exactly one deg-2 vertex, rest>=3)")

    print(f"\n=== SUMMARY: n={args.nmin}..{args.nmax} ===")
    print(f"total one-pole candidates checked: {total_one_pole}")
    print(f"survivors (no power-of-two cycle): {len(survivors)}")
    if survivors:
        with open("verifier/one_pole_survivors.json", "w") as f:
            json.dump([{"n": n, "g6": g6, "root": root} for n, g6, root, st in survivors], f, indent=2)
        print("saved to verifier/one_pole_survivors.json -- run one_pole_verify.py next")
    else:
        print("no survivors -- this is COMPUTATIONALLY VERIFIED evidence only "
              "for n in this range, not a proof for larger n.")


if __name__ == "__main__":
    main()
