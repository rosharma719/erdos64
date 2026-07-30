#!/usr/bin/env python3
"""Prerequisites for any future q=4 / q=5 attack -- and NOTHING MORE.

SCOPE WARNING, READ FIRST. This script does **not** eliminate q=4, does
not eliminate q=5, and does not establish q(G)>=5 or q(G)>=6. The
established frontier remains `q(G)>=4` (defect_three.md Part VIII). All
this script does is compute, and cross-check, three *inputs* that a
future q=4/q=5 case analysis would need before it could even begin:

  (A) the exact (h,c1,c3) case tables at q=4 and q=5, derived from the
      already-PROVED leaf-count identity and strong inequality;
  (B) the colored degree-2 path bound t(h) extended to h=4 and h=5
      (defect_three.md Part IV proves t=2,5,8 for h=1,2,3);
  (C) the per-kernel-edge branching factor (count of valid colored
      words) at each h, which is what makes the reconstruction searches
      of Parts VI/VII grow.

Every computation is validated by first REPRODUCING the corresponding
already-PROVED q<=3 value; if any baseline fails to reproduce, the
script exits nonzero and the new numbers must not be trusted.

Rigor labels, per project discipline:
  - (A) DERIVED from PROVED inputs (pure algebra) + COMPUTATIONALLY
        VERIFIED (reproduces the documented q=1,2,3 tables exactly).
  - (B) COMPUTATIONALLY VERIFIED by two implementations that are
        independent by construction (direct graph construction with a
        sound color-symmetry reduction; and the finite-state automaton
        of colored_path_automaton.py). The underlying mechanism
        classification (defect_three.md IV.2) is a hand PROOF and is
        h-independent, so it applies verbatim at h=4,5.
  - (C) COMPUTATIONALLY VERIFIED (the h=3 total reproduces the PROVED
        unreduced search's own level sums exactly).
  - NOT FORMALLY VERIFIED. No proof-assistant artifact exists anywhere
    in this project.
"""
from __future__ import annotations

import hashlib
import math
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.colored_path_search import has_forbidden_cycle  # noqa: E402
from verifier.colored_path_automaton import explore  # noqa: E402

# ---------------------------------------------------------------------------
# (A) the exact (h,c1,c3) case table at a given q
# ---------------------------------------------------------------------------

# Documented tables to reproduce as baselines:
#   q=1 -> defect.md Part II (h=0 and h=1 only)
#   q=2 -> defect.md Part III (h=0,1,2; h=2 has c1=c3<=1, two rows)
#   q=3 -> defect_three.md II.1 (the boxed six-row table)
KNOWN_TABLES = {
    1: [(0, 0, 6), (1, 0, 2)],
    2: [(0, 0, 8), (1, 0, 4), (2, 0, 0), (2, 1, 1)],
    3: [(0, 0, 10), (1, 0, 6), (2, 0, 2), (2, 1, 3), (3, 2, 0), (3, 3, 1)],
}


def case_table(q: int) -> list[tuple[int, int, int]]:
    """Every (h,c1,c3) consistent with the PROVED relations at this q.

    Inputs used, all already proved (defect.md leaf-compression I.1/I.3,
    restated at defect_three.md Part I):
      h <= q                                    (all h)
      h=0: G cubic, n = 2q+4, c1 = 0, c3 = n
      h=1: c1 = 0 forced (a C1-vertex needs 2 DISTINCT H-neighbours),
           so the leaf identity gives c3 = 2q
      h>=2: leaf identity c1 = c3 + 4h - 2q - 4, with c1 >= 0,
            and the strong inequality c3 + 2h <= 2q + 1
    """
    rows: list[tuple[int, int, int]] = [(0, 0, 2 * q + 4)]
    if q >= 1:
        rows.append((1, 0, 2 * q))
    for h in range(2, q + 1):
        hi = 2 * q + 1 - 2 * h          # strong inequality
        lo = max(0, 2 * q + 4 - 4 * h)  # c1 >= 0 in the leaf identity
        for c3 in range(lo, hi + 1):
            c1 = c3 + 4 * h - 2 * q - 4
            assert c1 >= 0
            rows.append((h, c1, c3))
    return rows


def h1_order_bound(q: int) -> int:
    """n <= 4q+1 at h=1.

    defect_three.md III.2 proves, using ONLY h=1 and C4-freeness (never
    the value of q): every C3-vertex has <=1 neighbour in C2
    (branch-incidence), every kernel chain has <=2 internal C2 vertices
    (chain-length), and no kernel self-loop exists. With c3=2q kernel
    vertices the C2-incidence budget is 2q, each subdivided kernel edge
    consumes 2 units, so at most q subdivided edges, each contributing
    at most 2 internal C2 vertices: c2 <= 2q. Hence n = 1 + c3 + c2
    <= 1 + 2q + 2q = 4q+1.  (At q=3 this is the documented n<=13.)
    """
    return 4 * q + 1


# ---------------------------------------------------------------------------
# (B) colored degree-2 path bound, extended to h=4,5
# ---------------------------------------------------------------------------

def canonical_next_colors(word: tuple[int, ...], h: int) -> list[int]:
    """Colors keeping the word canonical: any already-used color, plus the
    single smallest unused one."""
    used = set(word)
    out = [c for c in range(h) if c in used]
    for c in range(h):
        if c not in used:
            out.append(c)
            break
    return out


def max_length_canonical(h: int) -> dict[str, Any]:
    """Prefix-closed BFS over CANONICAL words only.

    Soundness of the color-symmetry reduction: permuting the H-colors is
    a graph isomorphism of the realized graph (H is independent and its
    vertices carry no other structure), so validity is permutation-
    invariant; every word has a canonical representative of the same
    length; and every prefix of a canonical word is canonical. Hence the
    canonical set is prefix-closed and the emptiness argument of
    colored_path_search.py applies verbatim: the last nonempty level is
    the TRUE maximum, not a search cutoff.
    """
    level: list[tuple[int, ...]] = [()]
    levels: dict[int, int] = {0: 1}
    witness: dict[int, tuple[int, ...]] = {0: ()}
    mx = 0
    canonical_words = 0
    unreduced_words = 0
    while level:
        nxt = []
        for w in level:
            for c in canonical_next_colors(w, h):
                cand = w + (c,)
                bad, _ = has_forbidden_cycle(cand, h)
                if not bad:
                    nxt.append(cand)
        if not nxt:
            break
        for w in nxt:
            k = len(set(w))
            canonical_words += 1
            # orbit size: inject the k used roles into h actual colors
            unreduced_words += math.factorial(h) // math.factorial(h - k)
        t = len(nxt[0])
        levels[t] = len(nxt)
        witness[t] = nxt[0]
        mx = t
        level = nxt
    return {
        "h": h,
        "max_valid_length": mx,
        "canonical_levels": levels,
        "witness_at_max": list(witness[mx]),
        "canonical_valid_words": canonical_words,
        "unreduced_valid_words": unreduced_words,
    }


PROVED_PATH_BOUNDS = {1: 2, 2: 5, 3: 8}       # defect_three.md Part IV
# Sum of the PROVED unreduced level sizes (excluding the empty word),
# from defect_three.md IV.1 / manifests/colored_path_search_manifest.json:
#   h=1: 1+1                          = 2
#   h=2: 2+4+4+4+4                    = 18
#   h=3: 3+9+18+36+72+78+36+6         = 258
PROVED_WORD_TOTALS = {1: 2, 2: 18, 3: 258}


def main() -> int:
    from verifier.z3_certificate import compact_json

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    ok = True
    report: dict[str, Any] = {
        "scope": (
            "PREREQUISITES ONLY. Does not eliminate q=4 or q=5. The "
            "established frontier is q(G)>=4 (defect_three.md VIII). "
            "q(G)>=5 and q(G)>=6 are NOT established anywhere."
        ),
    }

    # --- (A) case tables -----------------------------------------------
    print("(A) exact (h,c1,c3) case tables")
    tables: dict[str, Any] = {}
    for q in range(1, 6):
        rows = case_table(q)
        tables[str(q)] = {
            "rows": [list(r) for r in rows],
            "row_count": len(rows),
            "max_kernel_vertices_h_ge_2": max(
                [c1 + c3 for (h, c1, c3) in rows if h >= 2], default=0
            ),
            "h0_order": 2 * q + 4,
            "h1_order_bound": h1_order_bound(q),
        }
        if q in KNOWN_TABLES:
            match = rows == KNOWN_TABLES[q]
            ok &= match
            print(f"    q={q}: {len(rows):2d} rows  "
                  f"[baseline documented table reproduced: {match}]")
        else:
            print(f"    q={q}: {len(rows):2d} rows  [NEW, derived from PROVED relations]")
    report["case_tables"] = tables

    # --- (B) colored-path bounds ---------------------------------------
    print("(B) colored degree-2 path bound t(h), two independent implementations")
    paths: dict[str, Any] = {}
    for h in range(1, 6):
        direct = max_length_canonical(h)
        auto = explore(h)["max_valid_length"]
        agree = direct["max_valid_length"] == auto
        ok &= agree
        entry = {
            "direct_construction_max": direct["max_valid_length"],
            "automaton_max": auto,
            "implementations_agree": agree,
            "canonical_levels": direct["canonical_levels"],
            "witness_at_max": direct["witness_at_max"],
            "canonical_valid_words": direct["canonical_valid_words"],
            "unreduced_valid_words": direct["unreduced_valid_words"],
        }
        if h in PROVED_PATH_BOUNDS:
            base = direct["max_valid_length"] == PROVED_PATH_BOUNDS[h]
            wbase = direct["unreduced_valid_words"] == PROVED_WORD_TOTALS[h]
            ok &= base and wbase
            entry["reproduces_proved_bound"] = base
            entry["reproduces_proved_word_total"] = wbase
            tag = f"[PROVED baseline reproduced: {base and wbase}]"
        else:
            tag = "[NEW, computational only]"
        paths[str(h)] = entry
        print(f"    h={h}: t={direct['max_valid_length']:2d} "
              f"(direct={direct['max_valid_length']}, automaton={auto}, "
              f"agree={agree}); valid words={direct['unreduced_valid_words']} {tag}")
    report["colored_path"] = paths

    encoded = compact_json(report)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(compact_json(report) + "\n")

    print("ALL BASELINES REPRODUCED" if ok else "BASELINE MISMATCH -- DO NOT TRUST NEW VALUES")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
