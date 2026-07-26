"""Typed T4/T5 bridge-compatibility search (E20 integrity pass).

The search space is exactly the three cases proved in ``two_cut.md``:

* Type A: three bridges, no terminal edge, a common degree-1 terminal;
* Type B: two bridges plus the terminal edge, a common degree-1 terminal;
* Type C: two bridges without the terminal edge, satisfying T4's exact
  terminal-degree coverage and proper-subselection conditions.

T5 is evaluated before any pairwise cross-spectrum calculation.  Every
evaluation records its structural data and the ordered filter trace, so the
logic remains testable even while the real bridge library is empty.
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from dataclasses import asdict, dataclass, replace
from pathlib import Path

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from bridge_signature import build_library
from cycle_detect import (
    from_edges,
    has_cycle_len_dfs,
    has_cycle_len_nx,
    powers_of_two_up_to,
)

import networkx as nx


def sumset(a, b):
    return {x + y for x in a for y in b}


def is_forbidden_length(value):
    return value >= 4 and value & (value - 1) == 0


def hits_forbidden(values):
    return any(is_forbidden_length(value) for value in values)


def passes_T2(lam):
    values = sorted(lam)
    return any(abs(a - b) in (1, 2)
               for a, b in itertools.combinations(values, 2))


@dataclass(frozen=True)
class BridgeRecord:
    """One oriented abstract or graph-realizable bridge signature."""

    c: int
    e: int
    dx: int
    dy: int
    lam: frozenset[int]
    dyadic_internal_cycle_spectrum: frozenset[int] = frozenset()
    realizable: bool = False
    source_signature: tuple | None = None
    orientation: str = "xy"

    @classmethod
    def from_signature(cls, signature, *, realizable=True):
        c, e, dx, dy, lam, dyadic_cycles = signature
        return cls(c, e, dx, dy, frozenset(lam),
                   frozenset(dyadic_cycles), realizable, signature, "xy")

    @property
    def lex_signature(self):
        return (self.c, self.e)

    @property
    def self_sum_clean(self):
        return not hits_forbidden(sumset(self.lam, self.lam))

    @property
    def internal_cycle_clean(self):
        return not self.dyadic_internal_cycle_spectrum

    def swapped(self):
        return replace(self, dx=self.dy, dy=self.dx,
                       orientation="yx" if self.orientation == "xy" else "xy")


@dataclass
class CandidateEvaluation:
    bridge_type: str
    terminal_edge: bool
    bridges: tuple[BridgeRecord, ...]
    terminal_degree_profile: dict
    signatures: list[tuple[int, int]]
    self_sum_clean: list[bool]
    internal_cycle_clean: list[bool]
    realizability: list[str]
    structural_status: bool
    t2_status: bool | None = None
    terminal_edge_status: bool | None = None
    t5_maximality_status: bool | None = None
    pairwise_cross_compatible: bool | None = None
    filters_applied: list[str] | None = None
    rejection_stage: str | None = None
    accepted: bool = False

    def as_dict(self):
        data = asdict(self)
        for bridge in data["bridges"]:
            bridge["lam"] = sorted(bridge["lam"])
            bridge["dyadic_internal_cycle_spectrum"] = sorted(
                bridge["dyadic_internal_cycle_spectrum"])
            if bridge["source_signature"] is not None:
                bridge["source_signature"] = repr(bridge["source_signature"])
        data["signatures"] = [list(sig) for sig in self.signatures]
        return data


def _common_degree_one_terminal(bridges):
    if all(bridge.dx == 1 for bridge in bridges):
        return "x"
    if all(bridge.dy == 1 for bridge in bridges):
        return "y"
    return None


def _terminal_profile(bridges, terminal_edge):
    edge_degree = int(terminal_edge)
    return {
        "per_bridge": [
            {"dx": bridge.dx, "dy": bridge.dy} for bridge in bridges
        ],
        "terminal_edge": terminal_edge,
        "assembled_dx": sum(bridge.dx for bridge in bridges) + edge_degree,
        "assembled_dy": sum(bridge.dy for bridge in bridges) + edge_degree,
        "common_degree_one_terminal": _common_degree_one_terminal(bridges),
    }


def _structure_is_type(bridges, bridge_type):
    positive_terminal_degrees = all(
        bridge.dx >= 1 and bridge.dy >= 1 for bridge in bridges
    )
    if bridge_type == "A":
        terminal_edge = False
        valid = (len(bridges) == 3 and positive_terminal_degrees
                 and _common_degree_one_terminal(bridges) is not None)
    elif bridge_type == "B":
        terminal_edge = True
        valid = (len(bridges) == 2 and positive_terminal_degrees
                 and _common_degree_one_terminal(bridges) is not None)
    elif bridge_type == "C":
        terminal_edge = False
        valid = (
            len(bridges) == 2
            and positive_terminal_degrees
            and sum(bridge.dx for bridge in bridges) >= 3
            and sum(bridge.dy for bridge in bridges) >= 3
            and all(not (bridge.dx >= 3 and bridge.dy >= 3)
                    for bridge in bridges)
        )
    else:
        raise ValueError(f"unknown bridge type: {bridge_type}")
    return valid, terminal_edge


def t5_maximality_holds(bridges):
    """Every self-sum-clean bridge must be weakly lexicographically maximal."""
    maximum = max(bridge.lex_signature for bridge in bridges)
    return all(not bridge.self_sum_clean or bridge.lex_signature == maximum
               for bridge in bridges)


def pairwise_compatible(bridges):
    return all(not hits_forbidden(sumset(left.lam, right.lam))
               for left, right in itertools.combinations(bridges, 2))


def terminal_edge_compatible(bridges):
    """A Type-B terminal edge creates cycles of length ell+1."""
    return all(not hits_forbidden({length + 1 for length in bridge.lam})
               for bridge in bridges)


def evaluate_candidate(bridges, bridge_type):
    """Evaluate one candidate in the required order, with T5 before cross-sums."""
    bridges = tuple(bridges)
    structural_status, terminal_edge = _structure_is_type(bridges, bridge_type)
    evaluation = CandidateEvaluation(
        bridge_type=bridge_type,
        terminal_edge=terminal_edge,
        bridges=bridges,
        terminal_degree_profile=_terminal_profile(bridges, terminal_edge),
        signatures=[bridge.lex_signature for bridge in bridges],
        self_sum_clean=[bridge.self_sum_clean for bridge in bridges],
        internal_cycle_clean=[bridge.internal_cycle_clean for bridge in bridges],
        realizability=["GRAPH_REALIZABLE" if bridge.realizable else "ABSTRACT"
                       for bridge in bridges],
        structural_status=structural_status,
        filters_applied=[],
    )

    evaluation.filters_applied.append("type_structure")
    if not structural_status:
        evaluation.rejection_stage = "type_structure"
        return evaluation

    evaluation.filters_applied.append("internal_cycle_cleanliness")
    if not all(evaluation.internal_cycle_clean):
        evaluation.rejection_stage = "internal_cycle_cleanliness"
        return evaluation

    evaluation.t2_status = all(passes_T2(bridge.lam) for bridge in bridges)
    evaluation.filters_applied.append("T2")
    if not evaluation.t2_status:
        evaluation.rejection_stage = "T2"
        return evaluation

    if bridge_type == "B":
        evaluation.terminal_edge_status = terminal_edge_compatible(bridges)
        evaluation.filters_applied.append("terminal_edge_cycle_check")
        if not evaluation.terminal_edge_status:
            evaluation.rejection_stage = "terminal_edge_cycle_check"
            return evaluation

    if bridge_type in ("A", "B"):
        evaluation.t5_maximality_status = t5_maximality_holds(bridges)
        evaluation.filters_applied.append("T5_maximality")
        if not evaluation.t5_maximality_status:
            evaluation.rejection_stage = "T5_maximality"
            return evaluation

    evaluation.pairwise_cross_compatible = pairwise_compatible(bridges)
    evaluation.filters_applied.append("pairwise_cross_spectrum")
    if not evaluation.pairwise_cross_compatible:
        evaluation.rejection_stage = "pairwise_cross_spectrum"
        return evaluation

    evaluation.accepted = True
    return evaluation


def oriented_records(records):
    """Include both terminal orientations, without duplicating symmetric records."""
    out = []
    seen = set()
    for record in records:
        variants = [record] if record.dx == record.dy else [record, record.swapped()]
        for variant in variants:
            key = (variant.c, variant.e, variant.dx, variant.dy, variant.lam,
                   variant.dyadic_internal_cycle_spectrum,
                   variant.realizable, variant.source_signature)
            if key not in seen:
                seen.add(key)
                out.append(variant)
    return out


def search_typed_candidates(records):
    """Search only Types A/B/C; arbitrary family sizes are intentionally absent."""
    records = oriented_records(records)
    evaluations = []
    for bridge_type, size in (("A", 3), ("B", 2), ("C", 2)):
        for bridges in itertools.combinations_with_replacement(records, size):
            structural_status, _ = _structure_is_type(bridges, bridge_type)
            if structural_status:
                evaluations.append(evaluate_candidate(bridges, bridge_type))
    return evaluations


def assemble_and_verify(evaluation, library):
    """Assemble one graph-realizable accepted candidate and recheck it."""
    if not evaluation.accepted or not all(bridge.realizable
                                          for bridge in evaluation.bridges):
        raise ValueError("assembly requires an accepted graph-realizable candidate")
    graph = nx.Graph()
    xstar, ystar = "X*", "Y*"
    graph.add_nodes_from([xstar, ystar])
    for index, bridge in enumerate(evaluation.bridges):
        n, g6, x, y = library[bridge.source_signature][0]
        if bridge.orientation == "yx":
            x, y = y, x
        piece = nx.from_graph6_bytes(g6.encode())
        if piece.has_edge(x, y):
            raise AssertionError("bridge realization contains forbidden terminal edge xy")
        relabel = {
            vertex: (xstar if vertex == x else ystar if vertex == y
                     else f"b{index}_{vertex}")
            for vertex in piece.nodes()
        }
        graph = nx.compose(graph, nx.relabel_nodes(piece, relabel))
    if evaluation.terminal_edge:
        graph.add_edge(xstar, ystar)

    vertices = sorted(graph.nodes(), key=str)
    remap = {vertex: i for i, vertex in enumerate(vertices)}
    simple = from_edges(len(vertices), [(remap[u], remap[v])
                                        for u, v in graph.edges()])
    spectrum_dfs = {length: has_cycle_len_dfs(simple, length)
                    for length in powers_of_two_up_to(len(vertices))}
    spectrum_nx = {length: has_cycle_len_nx(simple, length)
                   for length in powers_of_two_up_to(len(vertices))}
    assert spectrum_dfs == spectrum_nx, "detector disagreement on assembled graph"
    return {
        "n": len(vertices),
        "m": graph.number_of_edges(),
        "min_degree": min(map(len, simple.values())),
        "is_f_clean": not any(spectrum_dfs.values()),
        "spectrum": spectrum_dfs,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nmin", type=int, default=3)
    parser.add_argument("--nmax", type=int, default=7)
    parser.add_argument("--output", type=Path,
                        help="optional JSON path for every typed candidate record")
    args = parser.parse_args()

    library, checked, qualifying = build_library(args.nmin, args.nmax)
    records = [BridgeRecord.from_signature(signature, realizable=True)
               for signature in library]
    evaluations = search_typed_candidates(records)
    print(f"bridge library: {checked} terminal pairs checked, {qualifying} "
          f"qualifying realizations, {len(library)} distinct signatures")
    print("typed candidates only: " + ", ".join(
        f"Type {bridge_type}={sum(e.bridge_type == bridge_type for e in evaluations)}"
        for bridge_type in ("A", "B", "C")))
    print(f"accepted after ordered filters: "
          f"{sum(evaluation.accepted for evaluation in evaluations)}")

    if not library:
        print("EMPTY REAL LIBRARY through the requested range: the real-data "
              "search is vacuous. Synthetic pytest fixtures exercise every "
              "Type A/B/C and T5 path nonvacuously.")

    if args.output:
        payload = {
            "range": {"nmin": args.nmin, "nmax": args.nmax},
            "library": {"checked": checked, "qualifying": qualifying,
                        "distinct_signatures": len(library)},
            "candidates": [evaluation.as_dict() for evaluation in evaluations],
        }
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print(f"wrote {len(evaluations)} candidate records to {args.output}")

    verified = []
    for evaluation in evaluations:
        if evaluation.accepted and all(bridge.realizable
                                       for bridge in evaluation.bridges):
            result = assemble_and_verify(evaluation, library)
            verified.append(result)
            if result["is_f_clean"] and result["min_degree"] >= 3:
                print("!!! ERDOS-GYARFAS COUNTEREXAMPLE FOUND -- escalate !!!")
    print(f"assembled and independently reverified: {len(verified)}")


if __name__ == "__main__":
    main()
