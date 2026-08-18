#!/usr/bin/env python3
"""Part VI.1 (defect-three phase): (c1,c3)=(0,2) at h=2.

By Part II.2's parity argument the 2 C3 vertices share a component; by
Part V (no pure-C2 F-component exists at h=2) that component cannot be
supplemented by any pure-cycle component, and since c1=0 there are no
other kernel vertices anywhere in F either -- so F is that ONE
component: kappa(F)=1 is FORCED (sharper than Part II.2's "free,
beta=kappa+1" table entry), hence beta(F)=2.

A connected multigraph on 2 vertices u,w, each of F-degree 3 (the
kernel, after suppression), with cyclomatic number beta=2 (|E|=|V|+1=3
kernel edges), has exactly two shapes consistent with both vertices
having ODD degree 3, from the elementary degree-parity count (p self-
loops at u, r self-loops at w, c cross edges: 2p+c=3=2r+c forces p=r,
c=3-2p, p in {0,1}):

  - p=0: THETA -- 3 parallel cross edges between u and w (no loops).
  - p=1: DUMBBELL -- 1 cross (bridge) edge, plus 1 self-loop at EACH
    of u and w.

Each kernel edge is realized as either a direct edge (0 internal C2
vertices) or a colored path (Part IV's per-path lemma, bound t<=5 for
h=2) between the two kernel endpoints it joins; each self-loop is
realized via the separately-justified loop-word generator (also
bounded, empirically, to s<=4 survivors for h=2 -- see the loop-word
search below, extended past that bound here for redundancy).
"""
from __future__ import annotations

import hashlib
import itertools
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.kernel_reconstruction import (  # noqa: E402
    all_valid_loop_words, all_valid_path_words, build_kernel_graph, check_c4_c8,
)
from verifier.z3_certificate import compact_json  # noqa: E402

H = 2
PATH_MAX = 5   # Part IV's proved h=2 bound
LOOP_MAX = 6   # extends 2 past the empirically-found s<=4 cutoff, for redundancy


def flat_words(by_len: dict[int, list[tuple[int, ...]]]) -> list[tuple[int, ...]]:
    out = []
    for words in by_len.values():
        out.extend(words)
    return out


def theta_pigeonhole_certificate() -> dict[str, Any]:
    """Hand argument, checked directly: if all 3 theta branches are
    subdivided (t>=1, i.e. u has 3 distinct C2 neighbours, each with its
    own first colour in {0,1}), pigeonhole forces 2 of the 3 first
    colours to coincide, giving an immediate C4 through u -- independent
    of every other position in every branch. Verified on every relevant
    (first-colour) triple."""
    no_repeat = []
    for c1, c2, c3 in itertools.product(range(H), repeat=3):
        if len({c1, c2, c3}) == 3:  # would need 3 distinct colours; impossible when H=2
            no_repeat.append((c1, c2, c3))
    assert not no_repeat, "pigeonhole should hold vacuously for H=2 with 3 draws"
    return {"claim": "3 draws from 2 colours always repeat (pigeonhole)", "verified": True}


def search_theta() -> dict[str, Any]:
    words_by_len = all_valid_path_words(H, PATH_MAX)
    candidates = flat_words(words_by_len)
    survivors = []
    tested = 0
    all_subdivided_survivors = []
    one_direct_survivors = []
    for w1, w2, w3 in itertools.product(candidates, repeat=3):
        n_direct = sum(1 for w in (w1, w2, w3) if len(w) == 0)
        if n_direct >= 2:
            # G is SIMPLE: 2+ direct u-w edges would be a parallel edge,
            # not a valid realization -- excluded, not tested as if valid.
            continue
        tested += 1
        branches = [("u", "w", w1), ("u", "w", w2), ("u", "w", w3)]
        G = build_kernel_graph(branches, H)
        c4, c8 = check_c4_c8(G)
        if not (c4 or c8):
            n_direct = sum(1 for w in (w1, w2, w3) if len(w) == 0)
            rec = {"lengths": [len(w1), len(w2), len(w3)], "words": [list(w1), list(w2), list(w3)]}
            survivors.append(rec)
            if n_direct == 0:
                all_subdivided_survivors.append(rec)
            elif n_direct >= 1:
                one_direct_survivors.append(rec)
    return {
        "topology": "theta", "tested": tested, "survivors": survivors,
        "all_subdivided_survivors": all_subdivided_survivors,
        "one_or_more_direct_survivors": one_direct_survivors,
    }


def search_dumbbell() -> dict[str, Any]:
    loop_words = all_valid_loop_words(H, LOOP_MAX)
    loop_candidates = flat_words({s: ws for s, ws in loop_words.items() if ws})
    bridge_candidates = flat_words(all_valid_path_words(H, PATH_MAX))
    survivors = []
    tested = 0
    for lu, lw, bridge in itertools.product(loop_candidates, loop_candidates, bridge_candidates):
        tested += 1
        branches = [("u", "u", lu), ("w", "w", lw), ("u", "w", bridge)]
        G = build_kernel_graph(branches, H)
        c4, c8 = check_c4_c8(G)
        if not (c4 or c8):
            survivors.append({
                "loop_u": list(lu), "loop_w": list(lw), "bridge": list(bridge),
            })
    return {
        "topology": "dumbbell", "tested": tested, "survivors": survivors,
        "loop_word_counts_by_s": {str(s): len(ws) for s, ws in loop_words.items()},
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    pigeonhole = theta_pigeonhole_certificate()
    theta = search_theta()
    dumbbell = search_dumbbell()

    print(f"pigeonhole: {pigeonhole}")
    print(f"theta: tested={theta['tested']} survivors={len(theta['survivors'])} "
          f"(all_subdivided={len(theta['all_subdivided_survivors'])}, "
          f"one_direct+={len(theta['one_or_more_direct_survivors'])})")
    print(f"dumbbell: tested={dumbbell['tested']} survivors={len(dumbbell['survivors'])} "
          f"loop_counts={dumbbell['loop_word_counts_by_s']}")

    report: dict[str, Any] = {"pigeonhole": pigeonhole, "theta": theta, "dumbbell": dumbbell}
    encoded = compact_json(report)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(compact_json(report) + "\n")

    eliminated = not theta["survivors"] and not dumbbell["survivors"]
    return 0 if eliminated else 1


if __name__ == "__main__":
    raise SystemExit(main())
