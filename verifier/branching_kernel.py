#!/usr/bin/env python3
"""Part I (defect-three phase): bounded branching-kernel identities.

Proves, from the leaf-count identity c1=c3+4h-2q-4 and the h>=2 strong
inequality c3+2h<=2q+1 (both already proved in the leaf-compression
phase), three case-split bounds:

  h=0: n = 2q+4                      (cubic case, G3's q=n/2-2 inverted)
  h=1: c3 = 2q                       (c1=0 forced, substitute into I.1)
  h>=2: c1+c3 <= 2q-2                (combine I.1 with the h>=2 bound)

These are pure algebra given the same hypotheses as the leaf-compression
phase's I.1/I.3 (H independent, C-degree-3, M2's C-restriction; h>=2
additionally needs the leaf-graph 2-degeneracy bound, itself a
minimality argument -- same scope caveat as before, not re-litigated
here).

"Bounded branching-kernel lemma": after suppressing every maximal
degree-2 path of F into a single edge (a purely topological operation on
F, not touching G's realized cycle structure), the resulting kernel graph
has exactly c1+c3 vertices -- bounded as above solely in terms of q.
Components of F consisting ENTIRELY of degree-2 vertices contribute NO
kernel vertices at all (they collapse under suppression to an
unrepresented pure cycle) and must be handled separately (Part V).
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.cubic_core import check_identities, random_cubic_core_graph  # noqa: E402
from verifier.cycle_detect import from_edges, has_cycle_len_dfs  # noqa: E402
from verifier.z3_certificate import compact_json  # noqa: E402


def branching_kernel_bound(rec: dict[str, Any], c4_free: bool | None = None) -> dict[str, Any]:
    """Given an already-computed check_identities record (with c1,c2,c3,
    h,q,n applicable), evaluate the three case-split claims.

    IMPORTANT SCOPE NOTE (the exact same pitfall caught in the
    leaf-compression phase's Part III): h=0 and h=1 are PURE ALGEBRA
    (need only H-independence + C-degree-3 + M2), so they are checked
    UNCONDITIONALLY, on every applicable graph, and are expected to hold
    universally. The h>=2 bound (c1+c3<=2q-2) is derived from the strong
    inequality c3+2h<=2q+1, which needs the leaf-graph's L4 minimality
    argument -- i.e. GENUINE F-cleanness (no power-of-two cycle
    anywhere), not merely H-independence/C-degree-3. It is therefore
    NOT expected to hold on arbitrary synthetic/atlas constructions (most
    of which are not F-clean, some not even satisfying q>=1) and is
    checked ONLY when `c4_free` is explicitly passed True (a partial,
    checkable proxy for F-cleanness at small size -- exact F-cleanness
    would need "no cycle of ANY power-of-two length", untestable in
    general without full cycle enumeration, so C4-freeness alone is used
    as the cheapest necessary condition, consistent with this project's
    established practice)."""
    h = rec["h"]
    q = rec["q"]
    n = rec["n"]
    c1 = rec.get("c1")
    c3 = rec.get("c3")
    out: dict[str, Any] = {"h": h, "q": q, "n": n, "c1": c1, "c3": c3}
    if h == 0:
        out["case"] = "h=0"
        out["claim"] = "n == 2q+4"
        out["holds"] = (n == 2 * q + 4)
    elif h == 1:
        out["case"] = "h=1"
        out["claim"] = "c1==0 and c3==2q"
        out["holds"] = (c1 == 0 and c3 == 2 * q)
    else:
        out["case"] = "h>=2"
        out["claim"] = "c1+c3 <= 2q-2 (scope: C4-free graphs only)"
        if c4_free:
            out["holds"] = (c1 is not None and c3 is not None and c1 + c3 <= 2 * q - 2)
        else:
            out["holds"] = True  # not applicable outside the C4-free scope; not a failure
            out["scope_skipped"] = True
    return out


def is_c4_free(graph: nx.Graph) -> bool:
    """Despite the name (kept for call-site brevity), this checks
    C4-AND-C8-freeness -- C4-freeness alone is NOT a sufficient proxy for
    F-cleanness (caught directly: an earlier pass using C4-freeness alone
    found 5 "failures," every one of which turned out to have a C8,
    hence was never actually F-clean to begin with -- not a counterexample
    to the theorem, just too weak a scope filter). F-cleanness needs no
    power-of-two cycle of ANY length; C4-and-C8-free is the standard
    cheap necessary (not sufficient) proxy used throughout this project."""
    relabel = {v: i for i, v in enumerate(sorted(graph, key=str))}
    g = from_edges(graph.number_of_nodes(), [(relabel[u], relabel[v]) for u, v in graph.edges()])
    return not has_cycle_len_dfs(g, 4) and not has_cycle_len_dfs(g, 8)


def atlas_sweep() -> dict[str, Any]:
    checked = 0
    failures = []
    by_case = {"h=0": 0, "h=1": 0, "h>=2": 0}
    c4_free_h2plus = 0
    for graph in nx.graph_atlas_g():
        if graph.number_of_nodes() < 4 or not nx.is_connected(graph):
            continue
        if min(dict(graph.degree()).values()) < 3:
            continue
        rec = check_identities(graph)
        if not rec["applicable"] or not rec.get("every_c_has_f_neighbour"):
            continue
        checked += 1
        c4free = is_c4_free(graph)
        bk = branching_kernel_bound(rec, c4_free=c4free)
        by_case[bk["case"]] += 1
        if bk["case"] == "h>=2" and c4free:
            c4_free_h2plus += 1
        if not bk["holds"]:
            failures.append((nx.to_graph6_bytes(graph, header=False).decode().strip(), bk))
    return {
        "population": "atlas order<=7", "checked": checked, "by_case": by_case,
        "h>=2_c4_free_population": c4_free_h2plus, "failures": failures,
    }


def synthetic_sweep(trials: int, seed: int) -> dict[str, Any]:
    import random
    rng = random.Random(seed)
    checked = 0
    failures = []
    by_case = {"h=0": 0, "h=1": 0, "h>=2": 0}
    c4_free_h2plus = 0
    for _ in range(trials):
        h = rng.randint(0, 6)
        if h == 0:
            # cubic case: build directly (random_cubic_core_graph needs h>=1
            # for its H-attachment machinery, so h=0 is handled as a plain
            # random cubic graph via a spanning-tree-plus-matching approach)
            n = rng.choice([6, 8, 10, 12, 14, 16])
            G = _random_cubic(rng, n)
            if G is None:
                continue
        else:
            n_pieces = rng.randint(1, 4)
            forest_sizes = [rng.randint(2, 6) for _ in range(n_pieces)]
            G = random_cubic_core_graph(rng, h, forest_sizes)
        if G is None:
            continue
        rec = check_identities(G)
        if not rec["applicable"] or not rec.get("every_c_has_f_neighbour"):
            continue
        checked += 1
        c4free = is_c4_free(G)
        bk = branching_kernel_bound(rec, c4_free=c4free)
        by_case[bk["case"]] += 1
        if bk["case"] == "h>=2" and c4free:
            c4_free_h2plus += 1
        if not bk["holds"]:
            failures.append((sorted((str(u), str(v)) for u, v in G.edges()), bk))
    return {
        "population": f"synthetic, {trials} trials", "checked": checked, "by_case": by_case,
        "h>=2_c4_free_population": c4_free_h2plus, "failures": failures,
    }


def _random_cubic(rng, n):
    """A random connected cubic graph via the pairing/configuration model
    with rejection (simple, connected)."""
    import networkx as nx
    for _ in range(200):
        stubs = [v for v in range(n) for _ in range(3)]
        rng.shuffle(stubs)
        G = nx.Graph()
        G.add_nodes_from(range(n))
        ok = True
        for i in range(0, len(stubs), 2):
            u, v = stubs[i], stubs[i + 1]
            if u == v or G.has_edge(u, v):
                ok = False
                break
            G.add_edge(u, v)
        if ok and G.number_of_edges() == 3 * n // 2 and nx.is_connected(G):
            return G
    return None


def main() -> int:
    import argparse
    import json
    import hashlib

    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=300000)
    parser.add_argument("--seed", type=int, default=20260728)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    atlas = atlas_sweep()
    synth = synthetic_sweep(args.trials, args.seed)

    print(f"atlas: checked={atlas['checked']} by_case={atlas['by_case']} failures={len(atlas['failures'])}")
    print(f"synthetic: checked={synth['checked']} by_case={synth['by_case']} failures={len(synth['failures'])}")

    report = {"atlas": atlas, "synthetic": synth}
    encoded = compact_json(report)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(compact_json(report) + "\n")

    ok = not atlas["failures"] and not synth["failures"]
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
