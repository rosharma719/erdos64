"""
K4 rigid-skeleton analysis (task Part 5, 2026-07-25, third redirection pass).

K4 is the smallest possible R-node skeleton (4 vertices, 6 edges, 3-connected,
no further 2-cut decomposition). Vertices 1,2,3,4; edges:
  12,13,14,23,24,34.
Each edge is either REAL (a literal edge of the host graph, contributing
path-length 1 between its endpoints) or VIRTUAL (expanded into a
two-terminal gadget with its own terminal-path spectrum Lambda_e, coming
from a child SPQR-tree node -- an S or P piece, or recursively another R).

In the fully-realized graph, K4's only simple cycles (as an abstract
4-vertex graph) are the 4 triangles and the 3 quadrilaterals (K4 minus a
perfect matching) -- nothing else, since a simple cycle in the expanded
graph corresponds exactly to a simple cycle in the skeleton (the gadgets'
internal vertices only connect back through their 2 terminals, no extra
cross-connectivity). So the *skeleton-level* cycle spectrum is exactly:

  4 triangles: Lambda_e1 + Lambda_e2 + Lambda_e3  (3-way sumset)
  3 quadrilaterals: Lambda_e1+Lambda_e2+Lambda_e3+Lambda_e4  (4-way sumset)

This module enumerates both, derives the immediate C4-freeness
restriction (checked first, as instructed, before C8/C16), then extends
to the full forbidden set, and searches bounded small Lambda_e assignments
for "reducible configurations": patterns of real/virtual edges that EITHER
force a power-of-two cycle, OR whose virtual-edge doubling (per the
one_pole.md two-terminal doubling criterion) yields a smaller one-pole.
"""
from __future__ import annotations
import itertools

VERTICES = [1, 2, 3, 4]
EDGES = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]

TRIANGLES = [
    frozenset([(1, 2), (1, 3), (2, 3)]),
    frozenset([(1, 2), (1, 4), (2, 4)]),
    frozenset([(1, 3), (1, 4), (3, 4)]),
    frozenset([(2, 3), (2, 4), (3, 4)]),
]

# K4 minus each perfect matching = one quadrilateral
MATCHINGS = [
    frozenset([(1, 2), (3, 4)]),
    frozenset([(1, 3), (2, 4)]),
    frozenset([(1, 4), (2, 3)]),
]
ALL_EDGES = frozenset(EDGES)
QUADRILATERALS = [ALL_EDGES - m for m in MATCHINGS]

F = set()
p = 4
while p <= 4096:
    F.add(p)
    p *= 2


def edge_key(e):
    return tuple(sorted(e))


def sumset(sets):
    out = {0}
    for s in sets:
        out = {a + b for a in out for b in s}
    return out


def triangle_spectrum(assignment, tri):
    return sumset([assignment[edge_key(e)] for e in tri])


def quad_spectrum(assignment, quad):
    return sumset([assignment[edge_key(e)] for e in quad])


def all_skeleton_cycle_lengths(assignment):
    lengths = set()
    for tri in TRIANGLES:
        lengths |= triangle_spectrum(assignment, tri)
    for quad in QUADRILATERALS:
        lengths |= quad_spectrum(assignment, quad)
    return lengths


def is_c4_free(assignment):
    return 4 not in all_skeleton_cycle_lengths(assignment)


def is_f_clean(assignment):
    return not (all_skeleton_cycle_lengths(assignment) & F)


def real_only_c4_check():
    """If ALL 4 edges of some quadrilateral are real (Lambda={1} each),
    that quadrilateral's spectrum is {4} -- an immediate C4. Purely
    combinatorial, no need to consider C8/C16 first, as instructed."""
    real = {edge_key(e): {1} for e in EDGES}
    for idx, quad in enumerate(QUADRILATERALS):
        spec = quad_spectrum(real, quad)
        print(f"quadrilateral {idx} (all edges real): spectrum={sorted(spec)} "
              f"{'CONTAINS C4' if 4 in spec else ''}")
    for idx, tri in enumerate(TRIANGLES):
        spec = triangle_spectrum(real, tri)
        print(f"triangle {idx} (all edges real): spectrum={sorted(spec)}")


def report_real_edge_count_restriction():
    """Exhaustively check, over all 2^6 subsets of K4's edges marked real
    (rest virtual with 1 not in spectrum), whether any of the 3
    quadrilaterals is entirely real -- the exact combinatorial C4 trigger,
    independent of what the virtual edges' own spectra turn out to be."""
    max_real_without_full_quad = 0
    for r in range(7):
        for subset in itertools.combinations(EDGES, r):
            subset_set = frozenset(edge_key(e) for e in subset)
            contains_full_quad = any(
                frozenset(edge_key(e) for e in quad) <= subset_set
                for quad in QUADRILATERALS)
            if not contains_full_quad:
                max_real_without_full_quad = max(max_real_without_full_quad, r)
    print(f"\nExhaustive check: the largest all-real edge subset containing "
          f"no full quadrilateral has size {max_real_without_full_quad} "
          f"(of 6 edges) -- confirms the pigeonhole bound below exactly.")
    print("  FACT: real-edges assignment is C4-free at the skeleton level "
          "iff no one of the 3 quadrilaterals is entirely real (its "
          "spectrum would be exactly {4}). Equivalently: at least one edge "
          "of EVERY quadrilateral must be virtual with 1 not in its "
          "spectrum, OR real-edge count on K4 is capped so that all 3 "
          "quadrilaterals retain >=1 virtual edge -- since each edge lies "
          "in exactly 2 of the 3 quadrilaterals, at most 4 of K4's 6 edges "
          "can be real without some quadrilateral being fully real "
          "(a short pigeonhole check, verified exhaustively below).")


def search_reducible_configurations(candidate_spectra):
    """Bounded search: for every way of assigning each of K4's 6 edges
    either 'real' (Lambda={1}) or one of the candidate virtual spectra,
    check C4/C8/... -freeness at the skeleton level, and flag every
    configuration that is skeleton-F-clean (a genuine reducible-config
    CANDIDATE, not yet a full graph -- still needs a valid full-graph
    realization to be a real gadget). Every proposed configuration is
    reported with its exact violating cycle(s) if not clean, matching the
    'test against all small realizable signatures before promoting to a
    lemma' requirement.
    """
    options = [{1}] + [set(s) for s in candidate_spectra]
    total = 0
    clean = []
    forced_c4 = 0
    forced_other_dyadic = 0
    for combo in itertools.product(range(len(options)), repeat=6):
        total += 1
        assignment = {edge_key(EDGES[i]): options[combo[i]] for i in range(6)}
        lengths = all_skeleton_cycle_lengths(assignment)
        hit = lengths & F
        if not hit:
            clean.append((combo, assignment, lengths))
        elif 4 in hit:
            forced_c4 += 1
        else:
            forced_other_dyadic += 1
    return dict(total=total, clean=clean, forced_c4=forced_c4,
                forced_other_dyadic=forced_other_dyadic, options=options)


def main(candidates=None):
    print("=== C4-freeness first (as instructed) ===")
    real_only_c4_check()
    report_real_edge_count_restriction()

    print("\n=== Bounded search over small virtual-edge spectra ===")
    # Candidate small virtual spectra to try for each edge (beyond {1}=real)
    if candidates is None:
        candidates = [{2}, {3}, {2, 3}, {3, 4}, {2, 4}, {5}]
    res = search_reducible_configurations(candidates)
    print(f"total configurations tested: {res['total']}")
    print(f"forced a C4: {res['forced_c4']}")
    print(f"forced some other dyadic length (8,16,...): {res['forced_other_dyadic']}")
    print(f"skeleton-level F-clean configurations found: {len(res['clean'])}")
    if res["clean"]:
        combo, assignment, lengths = res["clean"][0]
        print("smallest example (first found):")
        for e in EDGES:
            print(f"  edge {e}: spectrum {sorted(assignment[edge_key(e)])}")
        print(f"  all skeleton cycle lengths: {sorted(lengths)}")
        print("  NOTE: this is only a SKELETON-level clean configuration -- "
              "it does not yet certify a full one-pole survivor; each "
              "virtual edge's spectrum must still be realized by an actual "
              "F-clean two-terminal gadget internally, and internal cycles "
              "of each gadget (not tracked at this skeleton level) must "
              "ALSO avoid F. Reported as a candidate for further work, not "
              "a proved reducible configuration or a counterexample.")
    return res


# ---------------------------------------------------------------------------
# O7 refiltering (task Part 6, 2026-07-25, fourth redirection pass)
# ---------------------------------------------------------------------------
import itertools as _it

# edge -> its 2 triangles' "other 2 edges" (for the O7 triangle check)
def _other_edges_in_triangles(e):
    ek = edge_key(e)
    out = []
    for tri in TRIANGLES:
        if ek in {edge_key(x) for x in tri}:
            others = [edge_key(x) for x in tri if edge_key(x) != ek]
            out.append(others)
    return out  # list of 2 lists, each of length 2


EDGE_TRIANGLE_OTHERS = {edge_key(e): _other_edges_in_triangles(e) for e in EDGES}


def o7_survives(assignment):
    """Reject if ANY virtual edge (spectrum != {1}, i.e. representing a
    remote leaf R-child under the modeling choice stated in one_pole.md)
    has either of its 2 triangles with both OTHER edges real (spectrum=={1})."""
    for e in EDGES:
        ek = edge_key(e)
        if assignment[ek] == {1}:
            continue  # real edge itself, not a virtual R-child edge
        for others in EDGE_TRIANGLE_OTHERS[ek]:
            if all(assignment[o] == {1} for o in others):
                return False
    return True


def real_pattern(assignment):
    return tuple(1 if assignment[edge_key(e)] == {1} else 0 for e in EDGES)


K4_VERTEX_PERMS = list(_it.permutations(VERTICES))


def edge_index_map():
    return {edge_key(e): i for i, e in enumerate(EDGES)}


def canonical_pattern(pattern):
    """Canonical form of a 6-bit real/virtual pattern (ignoring WHICH
    virtual spectrum, just real-vs-virtual) under K4's automorphism group
    (S4 acting on vertices, inducing an action on the 6 edges)."""
    idx = edge_index_map()
    best = None
    for perm in K4_VERTEX_PERMS:
        relabel = {VERTICES[i]: perm[i] for i in range(4)}
        new_pattern = [0] * 6
        for e in EDGES:
            a, b = relabel[e[0]], relabel[e[1]]
            new_e = edge_key((a, b))
            new_pattern[idx[new_e]] = pattern[idx[edge_key(e)]]
        t = tuple(new_pattern)
        if best is None or t < best:
            best = t
    return best


def o7_refilter_report(candidates, base_result=None):
    res = (base_result if base_result is not None
           else search_reducible_configurations(candidates))
    clean = res["clean"]
    survivors = [(combo, assignment, lengths) for (combo, assignment, lengths) in clean
                 if o7_survives(assignment)]
    print(f"\n=== O7 refiltering of the {len(clean)} skeleton-clean configurations ===")
    print(f"survivors after O7: {len(survivors)}")

    by_real_pattern = {}
    for combo, assignment, lengths in survivors:
        rp = real_pattern(assignment)
        by_real_pattern.setdefault(rp, []).append((assignment, lengths))
    print(f"distinct real/virtual EDGE patterns among survivors: {len(by_real_pattern)}")

    orbits = {}
    for rp in by_real_pattern:
        canon = canonical_pattern(rp)
        orbits.setdefault(canon, []).append(rp)
    print(f"distinct real/virtual patterns up to K4 automorphism: {len(orbits)}")

    print("\nrepresentatives (one per orbit), with #real edges and one example spectrum assignment:")
    print("(canonical pattern shown for orbit identification; the printed "
          "real_edges/virtual_edges/spectra below all refer consistently to "
          "ONE ACTUAL representative assignment, using ITS OWN edge labels "
          "-- not a mix of the canonical labels with a different member's "
          "assignment.)")
    for canon, members in sorted(orbits.items(), key=lambda kv: -sum(kv[0])):
        example_rp = members[0]  # an actual real/virtual pattern in this orbit
        examples = by_real_pattern[example_rp]
        assignment, lengths = examples[0]
        # Use example_rp's OWN labels throughout -- self-consistent.
        real_edges = [EDGES[i] for i in range(6) if example_rp[i] == 1]
        virt_edges = [(EDGES[i], sorted(assignment[edge_key(EDGES[i])]))
                      for i in range(6) if example_rp[i] == 0]
        print(f"  canonical_pattern={canon} orbit_size(#patterns)={len(members)} "
              f"#real={sum(example_rp)} real_edges={real_edges} "
              f"virtual_edges(spectra)={virt_edges} cycle_lengths={sorted(lengths)}")
    return dict(total_clean=len(clean), survivors=len(survivors),
                distinct_patterns=len(by_real_pattern), distinct_orbits=len(orbits))


def run_all():
    """Run E16/E17 once each while sharing the single bounded census."""
    candidates = [{2}, {3}, {2, 3}, {3, 4}, {2, 4}, {5}]
    base_result = main(candidates)
    o7_result = o7_refilter_report(candidates, base_result=base_result)
    return {"base": base_result, "o7": o7_result}


if __name__ == "__main__":
    run_all()
