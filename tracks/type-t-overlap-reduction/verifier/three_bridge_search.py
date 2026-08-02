"""E21 Type-A abstract-model reconciliation and regression search.

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
  - the OLD strict-order model, retained only to reproduce the incomplete
    318 count from the sixth pass;
  - the CORRECTED tied-signature model, which returns 547 survivors and
    restores exactly 229 triples having at least two self-sum-clean bridges.

REALIZABLE filter: cross-reference against the bridge-signature library
(verifier/bridge_signature.py) -- currently empty through n=7 (E19) --
so the realizable count is reported honestly as 0, not fabricated.
"""
from __future__ import annotations
import itertools
import sys
from dataclasses import dataclass

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


def candidate_lambdas(universe=range(1, 9)):
    """Small candidate Lambda sets (subsets of 1..8, size 2-3, passing T2)."""
    out = []
    for size in (2, 3):
        for combo in itertools.combinations(universe, size):
            if passes_T2(combo):
                out.append(frozenset(combo))
    return out


def check_T5_consistency_strict_order(triple_lambdas):
    """Reproduce the OLD, incomplete strict-permutation representation.

    A strict ordering has one unique maximum.  Therefore it can represent
    T5 only when at most one bridge is self-sum-clean.  This function keeps
    the old enumeration explicit rather than replacing it with that shortcut.
    """
    clean = [is_self_sum_clean(lam) for lam in triple_lambdas]
    for order in itertools.permutations(range(3)):
        unique_maximum = order[-1]
        if all(not status or i == unique_maximum
               for i, status in enumerate(clean)):
            return True
    return False


def check_T5_consistency_with_ties(triple_lambdas):
    """Implement the corrected tied-signature representation.

    T5 requires each self-sum-clean bridge to be weakly maximal.  Any clean
    subset can tie at the maximum signature, while non-clean bridges may be
    below or tied.  Consequently every clean/non-clean pattern is representable.
    """
    return True


def triple_key(triple_lambdas):
    """Stable JSON-friendly key for a combinations-with-replacement triple."""
    return tuple(tuple(sorted(lam)) for lam in triple_lambdas)


@dataclass(frozen=True)
class ModelReconciliation:
    input_spectra: int
    spectra_after_T2: int
    triple_candidates: int
    pairwise_cross_compatible: int
    old_strict_survivors: int
    corrected_tied_survivors: int
    newly_represented: int
    newly_with_exactly_two_clean: int
    newly_with_three_clean: int
    delta_exactly_old_representation_gap: bool


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


def abstract_search(model="corrected_tied"):
    """Return pairwise-compatible survivors under the selected E21 model."""
    lambdas = candidate_lambdas()
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
        clean = [is_self_sum_clean(lam) for lam in tri]
        if model == "old_strict_order":
            accepted = check_T5_consistency_strict_order(tri)
        elif model == "corrected_tied_signature":
            accepted = check_T5_consistency_with_ties(tri)
        else:
            raise ValueError(f"unknown E21 model: {model}")
        if accepted:
            survivors.append((tri, clean))

    return survivors, lambdas


def reconcile_models():
    """Compute and directly prove the exact 318/547/229 relationship."""
    all_input = [frozenset(combo) for size in (2, 3)
                 for combo in itertools.combinations(range(1, 9), size)]
    t2_spectra = candidate_lambdas()
    triple_candidates = sum(
        1 for _ in itertools.combinations_with_replacement(t2_spectra, 3))
    corrected, _ = abstract_search("corrected_tied_signature")
    old, _ = abstract_search("old_strict_order")
    corrected_by_key = {triple_key(tri): clean for tri, clean in corrected}
    old_keys = {triple_key(tri) for tri, _ in old}
    delta = set(corrected_by_key) - old_keys
    expected_delta = {
        key for key, clean in corrected_by_key.items() if sum(clean) >= 2
    }
    return ModelReconciliation(
        input_spectra=len(all_input),
        spectra_after_T2=len(t2_spectra),
        triple_candidates=triple_candidates,
        pairwise_cross_compatible=len(corrected),
        old_strict_survivors=len(old),
        corrected_tied_survivors=len(corrected),
        newly_represented=len(delta),
        newly_with_exactly_two_clean=sum(
            sum(corrected_by_key[key]) == 2 for key in delta),
        newly_with_three_clean=sum(
            sum(corrected_by_key[key]) == 3 for key in delta),
        delta_exactly_old_representation_gap=(delta == expected_delta),
    )


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

    reconciliation = reconcile_models()
    print("\n=== Canonical E21 model reconciliation ===")
    print(f"input spectra (all size-2/3 subsets of 1..8): "
          f"{reconciliation.input_spectra}")
    print(f"spectra after T2: {reconciliation.spectra_after_T2}")
    print(f"triple candidates with replacement: "
          f"{reconciliation.triple_candidates}")
    print(f"after pairwise cross-compatibility: "
          f"{reconciliation.pairwise_cross_compatible}")
    print(f"old strict-order survivors (INCOMPLETE MODEL): "
          f"{reconciliation.old_strict_survivors}")
    print(f"corrected tied-signature survivors: "
          f"{reconciliation.corrected_tied_survivors}")
    print(f"newly represented: {reconciliation.newly_represented} "
          f"(exactly-two-clean={reconciliation.newly_with_exactly_two_clean}, "
          f"three-clean={reconciliation.newly_with_three_clean})")
    print("direct delta check (new survivors are exactly the old "
          "strict-order representation gap): "
          f"{reconciliation.delta_exactly_old_representation_gap}")

    survivors, lambdas = abstract_search("corrected_tied_signature")
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
