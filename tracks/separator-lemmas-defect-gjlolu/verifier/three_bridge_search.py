"""
Three-bridge (Type A) abstract + realizable search (task Part 6, 2026-07-25,
sixth redirection pass).

Type A (two_cut.md Sec.2c): t=3, xy not an edge, a1=a2=a3=1 (all bridges
share a degree-1 terminal), deg_G(x)=3, q1=q2=q3=3 -- forced exactly by
T4. The only remaining freedom per bridge is its path spectrum Lambda_i
(subject to T2: contains 2 values differing by 1 or 2) and its own
(c_i, e_i) signature.

ABSTRACT search: enumerate small candidate Lambda sets (not required to
be realized by an actual graph yet), form triples, and check:
  - T2: each Lambda_i has 2 admissible (diff 1 or 2) values;
  - pairwise cross-compatibility: (Lambda_i+Lambda_j) & F == empty for
    every i!=j (the global bridge-spectrum identity, Sec.2);
  - self-sum status of each Lambda_i: is (Lambda_i+Lambda_i) & F empty
    (self-sum-clean) or not (dyadic self-sum)?
  - T5's corollary, checked directly (not assumed): if a bridge is
    self-sum-clean, is it consistent for it to be lexicographically
    maximal among the triple (using an ASSUMED (c_i,e_i) ordering swept
    over all 6 permutations, since Lambda alone doesn't fix c,e)?

REALIZABLE filter: cross-reference against the bridge-signature library
(verifier/bridge_signature.py) -- currently empty through n=7 (E19) --
so the realizable count is reported honestly as 0, not fabricated.
"""
from __future__ import annotations
import itertools
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from bridge_signature import build_library

F = set()
_p = 4
while _p <= 4096:
    F.add(_p)
    _p *= 2


def sumset(a, b):
    return {x + y for x in a for y in b}


def passes_T2(lam):
    lam = sorted(lam)
    return any(abs(a - b) in (1, 2) for a, b in itertools.combinations(lam, 2))


def is_self_sum_clean(lam):
    return not (sumset(lam, lam) & F)


def candidate_lambdas(max_len=6, universe=range(1, 9)):
    """Small candidate Lambda sets (subsets of 1..8, size 2-3, passing T2)."""
    out = []
    for size in (2, 3):
        for combo in itertools.combinations(universe, size):
            if passes_T2(combo):
                out.append(frozenset(combo))
    return out


def check_T5_consistency_with_ties(triple_lambdas):
    """CORRECTED per the seventh-pass instruction: the previous version of
    this check only tested STRICT (c,e) permutations, which cannot express
    a genuine 3-way tie -- and T5's corollary only requires each self-sum-
    clean bridge to be WEAKLY maximal (>= every other, ties allowed), not
    uniquely maximal. Any subset S of self-sum-clean bridges can ALWAYS be
    made consistent by simply setting (c,e) equal for every bridge in S at
    the maximum value, with the rest <= that value -- so this check is now
    (correctly) trivially satisfiable for ANY clean/non-clean pattern.
    This triviality is not a bug: it IS the seventh-pass finding (Sec.7 of
    two_cut.md) that T5, once ties are modeled correctly, imposes no
    additional exclusionary power beyond what T2 + pairwise compatibility
    already give -- kept here as an explicit, checkable confirmation of
    that finding rather than silently dropped."""
    return True  # always consistent once ties are properly allowed -- see docstring


def verify_infinite_equal_signature_family(max_m=2000):
    """two_cut.md Sec.7's Proposition: Lambda_1=Lambda_2=Lambda_3={m,m+1}
    survives every pairwise/self-sum check for infinitely many m (all m
    with neither 2m nor 2m+2 in F). Verified computationally here, not
    just asserted."""
    qualifying = []
    for m in range(1, max_m):
        lam = frozenset((m, m + 1))
        s = sumset(lam, lam)  # same as Lambda_i+Lambda_j for any i,j here
        if not (s & F):
            qualifying.append(m)
    return qualifying


def abstract_search():
    lambdas = candidate_lambdas()
    print(f"{len(lambdas)} candidate Lambda sets pass T2 (universe 1..8, size 2-3)")

    survivors = []
    for combo in itertools.combinations_with_replacement(range(len(lambdas)), 3):
        tri = [lambdas[i] for i in combo]
        # pairwise cross-compatibility (all 3 pairs, i<j)
        ok = True
        for i, j in itertools.combinations(range(3), 2):
            if sumset(tri[i], tri[j]) & F:
                ok = False
                break
        if not ok:
            continue
        clean = [is_self_sum_clean(tri[i]) for i in range(3)]
        # T5 with ties properly modeled: always consistent (see docstring
        # of check_T5_consistency_with_ties) -- kept as an explicit call,
        # not silently dropped, to make the triviality checkable in code.
        if check_T5_consistency_with_ties(tri):
            survivors.append((tri, clean))

    return survivors, lambdas


def main():
    print("=== SCOPE NOTE (seventh pass): this script is retained for the "
          "regression battery below, NOT as a route to excluding Type A. "
          "two_cut.md Sec.7 PROVES T2+T4+T5+pairwise-compatibility are "
          "jointly insufficient (an explicit infinite equal-signature "
          "family survives all of them). Abstract survivor counts are no "
          "longer reported as if they could establish the three-bridge "
          "exclusion -- see verifier/bridge_closure_search.py for the "
          "actual current program (direct construction/search over real "
          "two-terminal graphs, T6's copy-gadget criterion). ===\n")

    print("=== Verifying the infinite equal-signature family explicitly ===")
    qualifying_m = verify_infinite_equal_signature_family(max_m=2000)
    print(f"Lambda_1=Lambda_2=Lambda_3={{m,m+1}}: {len(qualifying_m)} of the "
          f"first 1999 integers m give a fully pairwise+self-sum-clean equal "
          f"triple (neither 2m nor 2m+2 in F) -- e.g. m={qualifying_m[:5]}. "
          f"This alone proves T2+T4+T5+pairwise-compatibility cannot exclude "
          f"Type A abstractly: infinitely many valid tied signatures survive.")

    survivors, lambdas = abstract_search()
    print(f"\n(regression only, small finite universe 1..8) abstract "
          f"signature triples pairwise-compatible + T5-with-ties-consistent: "
          f"{len(survivors)} -- NOT reported as progress toward exclusion; "
          f"kept solely to confirm the search code agrees with the proved "
          f"insufficiency result above (every one of these ties are trivially "
          f"realizable in the abstract sense per the tie-argument, consistent "
          f"with Sec.7, not a new finding).")

    n_all_clean = sum(1 for tri, clean in survivors if all(clean))
    print(f"  of which all 3 bridges self-sum-clean (matches the infinite "
          f"family's shape): {n_all_clean}")

    # Realizable filter -- the only count that actually matters now.
    print("\n=== realizable filter (the actual open question) ===")
    library, checked, qualifying = build_library(nmin=3, nmax=7)
    print(f"bridge-signature library: {qualifying} qualifying bridges, "
          f"{len(library)} distinct signatures (n<=7)")
    realizable_lambdas = {sig[4] for sig in library.keys()}  # the Lambda component
    print(f"distinct REALIZABLE Lambda spectra in the library: {len(realizable_lambdas)}")

    realizable_survivors = [
        (tri, clean) for tri, clean in survivors
        if all(t in realizable_lambdas for t in tri)
    ]
    print(f"of the {len(survivors)} regression-only abstract survivors, "
          f"{len(realizable_survivors)} have all 3 Lambda values REALIZABLE "
          f"(library empty at this order range, so this is expected to be 0 --"
          f" relabeled PIPELINE VALIDATION, not evidence of general "
          f"nonexistence, per instruction)")

    print("\n=== smallest obstruction to promoting the three-bridge exclusion "
          "to a theorem ===")
    print("As proved (not just observed) in two_cut.md Sec.7: the additive/"
          "combinatorial conditions (T2, T4, T5, pairwise compatibility) "
          "cannot exclude Type A abstractly on their own -- an infinite "
          "family of valid tied signatures survives them. The "
          "obstruction to a theorem is exactly REALIZABILITY: no concrete "
          "bridge graph is yet known (searched through n=7) whose actual "
          "path spectrum matches any surviving abstract Lambda shape while "
          "also satisfying T1 (B+xy 2-connected) and internal min-degree-3 "
          "with internal F-cleanness. This is the honest smallest-obstruction "
          "report requested: the gap is realizability, not the combinatorics "
          "of T2/T4/T5 themselves, which are already satisfiable abstractly.")


if __name__ == "__main__":
    main()
