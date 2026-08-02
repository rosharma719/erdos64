#!/usr/bin/env python3
"""Passage-level projection of Type-T multipole gadget variables.

A selected triple hub or linked-pair gadget supplies one or more *passages*
-- two- or three-edge routes between pairs of deficient core vertices. A
dyadic cycle only cares whether a passage exists, not which specific
gadget/triple identity supplies it (in particular, not about a triple's
unused third attachment). But the gadget-level conflict catalog in
``type_t_port_short_conflicts.py`` names the specific triple/gadget, so the
same geometric passage gets re-derived once per candidate supplier -- on
``(4,55,7)`` a passage is supplied by 14.5 different triples/gadgets on
average (up to 127), which is exactly the source of the C4/C8 catalog's
scale (and, more severely, of the raw C16 enumerator's blowup).

This module defines the passage variables and the *proved* correspondence
with the gadget variables:

* ``p2[u,v]`` (unordered pair of deficient vertices): true iff the
  completion supplies a two-edge route ``u - hub - v``.
* ``p3[u,v]``: true iff the completion supplies a three-edge route
  ``u - hub_L - hub_R - v`` through some even-``j`` linked gadget's
  joining edge.

## Forward implications (a selected gadget supplies its passages)

* Triple ``T = {u,v,w}``: selecting it supplies all three route-2 passages
  ``p2[u,v]``, ``p2[u,w]``, ``p2[v,w]`` simultaneously (the hub has all
  three edges regardless of which pair a given cycle actually uses).
* Linked gadget ``g = (P,Q)``, ``P=(p1,p2)``, ``Q=(q1,q2)``: selecting it
  supplies the two route-2 passages ``p2[p1,p2]``, ``p2[q1,q2]`` **and**
  all four route-3 cross passages ``p3[p1,q1]``, ``p3[p1,q2]``,
  ``p3[p2,q1]``, ``p3[p2,q2]`` simultaneously -- both new hubs and the
  joining edge exist together once ``g`` is selected, so every combination
  of one left attachment and one right attachment is a physically present
  3-edge route.

## Reverse implications and the "at most one supplier" fact

The reverse implication ``p2[u,v] -> OR of every candidate supplying it``
is also encoded (for completeness / for uses of ``p`` variables beyond
pure forbidding, e.g. Phase 8's hitting-set analysis). It raises a natural
question: could two *different* selected triples/gadgets simultaneously
supply the same passage? No -- **proved**, not assumed: any two distinct
candidates supplying the same passage ``(u,v)`` both have ``u`` and ``v``
among their own attachment vertices (a triple containing the pair, or a
gadget whose ``P`` or ``Q`` side *is* the pair). The exact-cover
constraints already require every deficient vertex, in particular ``u``,
to be covered by *exactly one* selected triple/gadget-side. So selecting
two different candidates that both claim ``u`` already violates the
existing exact-cover clauses, independent of anything about ``v`` or the
passage machinery. ``verify_at_most_one_supplier`` checks this
structurally against the actual catalogs (every pair of distinct
suppliers of the same passage key shares a vertex), rather than trusting
the argument abstractly.
"""

from __future__ import annotations

from collections import defaultdict

from type_t_port_triples import LinkedGadget, Triple


PassageKey = tuple[int, int]
VariableTag = tuple


def build_passage_catalog(triples: list[Triple], gadgets: list[LinkedGadget]):
    """Returns (p2_suppliers, p3_suppliers): dict[(u,v)] -> list of tags."""
    p2: dict[PassageKey, list[VariableTag]] = defaultdict(list)
    p3: dict[PassageKey, list[VariableTag]] = defaultdict(list)
    for triple in triples:
        u, v, w = triple
        tag = ("triple", triple)
        for a, b in ((u, v), (u, w), (v, w)):
            p2[(min(a, b), max(a, b))].append(tag)
    for gadget in gadgets:
        (p1, p2_side), (q1, q2_side) = gadget
        tag = ("gadget", gadget)
        for a, b in ((p1, p2_side), (q1, q2_side)):
            p2[(min(a, b), max(a, b))].append(tag)
        for pi in (p1, p2_side):
            for qj in (q1, q2_side):
                p3[(min(pi, qj), max(pi, qj))].append(tag)
    return dict(p2), dict(p3)


def channeling_clauses(pool, x_var, p2_var, p3_var, p2_suppliers, p3_suppliers):
    """CNF clauses implementing both directions of the gadget<->passage
    correspondence. ``x_var``/``p2_var``/``p3_var`` map tags/keys to SAT
    literals (already allocated by the caller, e.g. via ``pysat.formula.IDPool``).

    Forward (a selected gadget supplies its passages) is what soundness of
    a *passage-level conflict clause* actually needs. Reverse is included
    for completeness/documentation and for any downstream use of ``p``
    variables outside pure forbidding (Phase 8).
    """
    clauses: list[list[int]] = []
    # Forward: x_T -> p2[u,v] for each of T's three sub-pairs; likewise for gadgets.
    forward_targets: dict[VariableTag, list[PassageKey]] = defaultdict(list)
    for key, tags in p2_suppliers.items():
        for tag in tags:
            forward_targets[tag].append(("p2", key))
    for key, tags in p3_suppliers.items():
        for tag in tags:
            forward_targets[tag].append(("p3", key))
    for tag, targets in forward_targets.items():
        xv = x_var[tag]
        for kind, key in targets:
            pv = p2_var[key] if kind == "p2" else p3_var[key]
            clauses.append([-xv, pv])
    # Reverse: p2[u,v] -> OR of its suppliers (and symmetrically for p3).
    for key, tags in p2_suppliers.items():
        clauses.append([-p2_var[key]] + [x_var[tag] for tag in tags])
    for key, tags in p3_suppliers.items():
        clauses.append([-p3_var[key]] + [x_var[tag] for tag in tags])
    return clauses


def _attachment_vertices(tag: VariableTag) -> frozenset[int]:
    kind, item = tag
    if kind == "triple":
        return frozenset(item)
    (p1, p2_side), (q1, q2_side) = item
    return frozenset((p1, p2_side, q1, q2_side))


def drop_multi_p3_supports(results: dict) -> tuple[dict, int]:
    """Drop every support naming two different ``p3`` passages. This is
    NOT merely a compression -- for one important sub-case it is a real
    soundness fix, corrected after an external review caught the imprecise
    original justification.

    A single gadget's forward channeling makes ALL FOUR of its cross
    passages true simultaneously the moment it is selected (see
    ``channeling_clauses``): if the gadget's sides are ``{a,b}`` and
    ``{c,d}``, selecting it forces ``p3[a,c] AND p3[a,d] AND p3[b,c] AND
    p3[b,d]`` together, as *availability* predicates -- regardless of
    whether any one simple cycle could ever use more than one of those
    routes. A clause ``not p3[a,c] or not p3[b,d]`` would therefore be
    directly falsified by the channeling axiom the moment this gadget is
    selected: not vacuous (already excluded by other constraints) but
    actively UNSOUND, capable of forcing the whole SAT instance UNSAT by
    rejecting a perfectly legal completion for no real graph-theoretic
    reason. Checked directly against the catalogs: of the 1,457 raw p3-p3
    candidates found pre-fix for (4,55,7)'s C8 search, 331 were exactly
    this same-gadget "complementary pair" case.

    The remaining candidates -- two p3 passages that could only both be
    supplied by two *different* gadgets -- are the case the original
    docstring described: vacuous, not unsound, since exact-cover already
    forbids selecting two different gadgets at once. Checking literal
    vertex-disjointness (as the original verification did) distinguishes
    "shares a vertex" from "doesn't" but does NOT distinguish "same
    gadget, complementary pair" (unsound) from "two different gadgets"
    (merely vacuous) -- both cases have four fully distinct endpoint
    vertices, since a gadget's own two sides never overlap.

    Either way the correct action is identical -- exclude the support
    entirely -- and this function (plus the equivalent inline exclusion in
    ``enumerate_m2_passage_conflicts`` and ``enumerate_passage_conflicts``)
    already did that unconditionally, for every p3-p3 pair regardless of
    which case it falls into, so no committed catalog was ever affected by
    this imprecision -- only the written justification needed correcting.
    """
    kept = {}
    dropped = 0
    for key, value in results.items():
        if sum(1 for kind, _ in key if kind == "p3") >= 2:
            dropped += 1
            continue
        kept[key] = value
    return kept, dropped


def materialize_passages(core, support):
    """Materialize a MINIMAL ordinary graph containing exactly the named
    passages and nothing else -- one fresh 2-edge hub per ``p2[u,v]``
    (edges ``h-u``, ``h-v`` only, NOT a third attachment from whatever
    triple happens to supply it), and one fresh pair of hubs joined by an
    edge per ``p3[u,v]``.

    This is deliberately NOT the same as materializing a real supplying
    triple/gadget (``type_t_port_short_conflicts.materialize_variables``),
    which also adds that object's *other*, unused edges. Verifying a
    passage-level conflict against a fully materialized supplier is
    unsound as a check: ``edge_path_cycle`` may find a cycle that
    incidentally exists through the supplier's other attachments, "verifying"
    the claimed passage pair without ever actually using the claimed
    passage edges. Only this minimal construction tests the claim that was
    actually made.
    """
    import networkx as nx

    graph = nx.Graph()
    graph.add_nodes_from(range(core.order))
    graph.add_edges_from(core.edges)
    next_vertex = core.order
    for kind, (u, v) in support:
        if kind == "p2":
            hub = next_vertex
            next_vertex += 1
            graph.add_edges_from(((hub, u), (hub, v)))
        elif kind == "p3":
            left, right = next_vertex, next_vertex + 1
            next_vertex += 2
            graph.add_edges_from(((left, u), (left, right), (right, v)))
        else:
            raise AssertionError(f"unknown passage kind {kind}")
    adjacency = tuple(frozenset(graph.neighbors(v)) for v in range(next_vertex))
    return graph, adjacency


def verify_at_most_one_supplier(p2_suppliers, p3_suppliers) -> dict:
    """Structural proof-check: every pair of distinct suppliers of the same
    passage key shares an attachment vertex, hence can never be
    simultaneously selected under the existing exact-cover constraints."""
    checked_pairs = 0
    for suppliers in (p2_suppliers, p3_suppliers):
        for key, tags in suppliers.items():
            unique_tags = sorted(set(tags))
            for i in range(len(unique_tags)):
                for j in range(i + 1, len(unique_tags)):
                    a, b = unique_tags[i], unique_tags[j]
                    shared = _attachment_vertices(a) & _attachment_vertices(b)
                    if not shared:
                        raise AssertionError(
                            f"suppliers {a} and {b} of passage {key} share no vertex; "
                            "at-most-one-supplier claim is false"
                        )
                    checked_pairs += 1
    return {"status": "PROVED", "distinct_supplier_pairs_checked": checked_pairs}
