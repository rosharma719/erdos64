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


def check_T5_consistency(triple_lambdas, perm_ce_order):
    """Given an assumed lex order among the 3 bridges' (c,e) (a permutation
    0<1<2 meaning bridge perm[0] has smallest (c,e), perm[2] largest),
    check: every self-sum-clean bridge must be the (unique, or tied-max)
    lex-maximal one, i.e. index perm[2] (or tied with it) -- else T5's
    corollary is violated for this assumed ordering."""
    clean = [is_self_sum_clean(triple_lambdas[i]) for i in range(3)]
    max_idx = perm_ce_order[2]
    for i in range(3):
        if clean[i] and i != max_idx:
            # i is self-sum-clean but NOT the assumed lex-maximal bridge --
            # only consistent if i is tied with max_idx, which we can't
            # express in a strict order; treat strict orderings as requiring
            # i == max_idx exactly.
            return False
    return True


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
        # does SOME assumed (c,e) ordering make T5 consistent?
        consistent_orderings = 0
        for perm in itertools.permutations(range(3)):
            if check_T5_consistency(tri, perm):
                consistent_orderings += 1
        if consistent_orderings > 0:
            survivors.append((tri, clean, consistent_orderings))

    return survivors, lambdas


def main():
    survivors, lambdas = abstract_search()
    print(f"\nabstract signature triples (pairwise cross-compatible under the "
          f"global bridge-spectrum identity): {len(survivors)}")

    n_all_clean = sum(1 for tri, clean, _ in survivors if all(clean))
    n_some_dyadic_self = sum(1 for tri, clean, _ in survivors if not all(clean))
    print(f"  of which all 3 bridges self-sum-clean: {n_all_clean}")
    print(f"  of which >=1 bridge has a dyadic self-sum: {n_some_dyadic_self}")

    print("\nsample survivors (up to 8):")
    for tri, clean, n_orderings in survivors[:8]:
        print(f"  Lambda triple={[sorted(t) for t in tri]} "
              f"self_sum_clean={clean} "
              f"consistent (c,e)-orderings for T5={n_orderings}/6")

    # Realizable filter
    print("\n=== realizable filter (cross-reference bridge-signature library) ===")
    library, checked, qualifying = build_library(nmin=3, nmax=7)
    print(f"bridge-signature library: {qualifying} qualifying bridges, "
          f"{len(library)} distinct signatures (n<=7)")
    realizable_lambdas = {sig[4] for sig in library.keys()}  # the Lambda component
    print(f"distinct REALIZABLE Lambda spectra in the library: {len(realizable_lambdas)}")

    realizable_survivors = [
        (tri, clean, n) for tri, clean, n in survivors
        if all(t in realizable_lambdas for t in tri)
    ]
    print(f"of the {len(survivors)} abstract survivors, "
          f"{len(realizable_survivors)} have all 3 Lambda values REALIZABLE "
          f"(library empty at this order range, so this is expected to be 0 --"
          f" relabeled PIPELINE VALIDATION, not evidence of general "
          f"nonexistence, per instruction)")

    print("\n=== smallest obstruction to promoting the three-bridge exclusion "
          "to a theorem ===")
    print("The abstract search alone does NOT exclude Type A: "
          f"{len(survivors)} abstract signature triples satisfy every "
          "currently-proved condition (T2, pairwise cross-compatibility, "
          "T5's maximality corollary under some (c,e) ordering). The "
          "obstruction to a theorem is exactly REALIZABILITY: no concrete "
          "bridge graph is yet known (searched through n=7) whose actual "
          "path spectrum matches any of these abstract Lambda sets while "
          "also satisfying T1 (B+xy 2-connected) and internal min-degree-3 "
          "with internal F-cleanness. This is the honest smallest-obstruction "
          "report requested: the gap is realizability, not the combinatorics "
          "of T2/T4/T5 themselves, which are already satisfiable abstractly.")


if __name__ == "__main__":
    main()
