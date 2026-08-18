#!/usr/bin/env python3
"""Large-neighborhood ruin-and-recreate search for Type-T minimum cubic
multipole completions.

This generalizes ``type_t_port_multipole_sat.local_exchange_search`` (which
swaps 2-4 triple hubs at a time via randomized Algorithm-X) to genuinely
large moves: on every round we "ruin" a random subset of K triple hubs
(K much larger than 2-4, biased toward hubs implicated in the current worst
short cycle), and "recreate" the freed sub-partition with an OR-Tools CP-SAT
exact-cover solve over the *catalog* restricted to the freed deficient
vertices.  Rejected recreations (ones that regress an already-zero C4/C8
count) are excluded from the CP-SAT model with a local no-good clause and the
solver is asked again, so a single ruin can try several structurally
different repairs before giving up.  Acceptance beyond the C4/C8 hard floor
uses simulated annealing on the C16 count (matching the scalarization already
used by ``local_exchange_search`` and ``type_t_port_multiswitch.search``).

For even ``j`` the unique linked double-hub gadget can also be included in a
ruin (with some probability), in which case the CP-SAT sub-model additionally
selects exactly one gadget among the candidates whose four attachments lie in
the freed vertex set.

Every time the running-best lexicographic tuple (C4, C8, C16) improves, the
completion is materialized, independently checked with
``type_t_port_multipole_check.validate_partition`` and
``edge_path_cycle`` (an algorithmically distinct cycle detector), and saved
to ``data/type_t_port_c16/``.
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
import random
import time
from pathlib import Path

import networkx as nx
from ortools.sat.python import cp_model

from type_t_port_core_export import build_core
from type_t_port_multipole_check import edge_path_cycle, validate_partition
from type_t_port_multipole_sat import (
    build_catalog,
    enumerate_cycles_exact,
    first_cycle_profile,
    graph_encodings,
    materialize,
)
from type_t_port_multiswitch import cycle_edges, full_cycles, update_cycles
from type_t_port_triples import powers_up_to

Triple = tuple[int, int, int]
Pair = tuple[int, int]
Gadget = tuple[Pair, Pair]

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "data" / "type_t_port_c16"


def hub_edges(hub: int, attachments) -> set[tuple[int, int]]:
    return {(min(hub, v), max(hub, v)) for v in attachments}


def build_catalog_index(items, attachments_fn):
    by_vertex: dict[int, list] = {}
    for item in items:
        for vertex in attachments_fn(item):
            by_vertex.setdefault(vertex, []).append(item)
    return by_vertex


def candidates_within(freed: frozenset[int], by_vertex: dict[int, list],
                       attachments_fn) -> list:
    seen = set()
    result = []
    for vertex in freed:
        for item in by_vertex.get(vertex, ()):
            if item in seen:
                continue
            seen.add(item)
            if freed.issuperset(attachments_fn(item)):
                result.append(item)
    return result


def score_state(cycles: dict[int, set]) -> tuple[int, int, int]:
    return (
        len(cycles.get(4, ())), len(cycles.get(8, ())),
        len(cycles[16]) if 16 in cycles else 10 ** 9,
    )


class LNSInstance:
    """Mutable ruin-and-recreate search state for one (j, a, c) instance."""

    def __init__(self, core, seed: int):
        self.core = core
        self.rng = random.Random(seed)
        (self.normal, self.pairs, self.triples_catalog, self.gadgets_catalog,
         self.same_bad, self.cross_bad) = build_catalog(core)
        self.triple_by_vertex = build_catalog_index(
            self.triples_catalog, lambda t: t,
        )
        self.gadget_by_vertex = build_catalog_index(
            self.gadgets_catalog, lambda g: g[0] + g[1],
        )
        self.T = self.normal["triple_hubs"]
        self.has_gadget = core.j % 2 == 0
        self.hub_of_slot = list(range(core.order, core.order + self.T))
        self.left_hub = core.order + self.T if self.has_gadget else None
        self.right_hub = core.order + self.T + 1 if self.has_gadget else None
        self.order = core.order + self.T + (2 if self.has_gadget else 0)

    def initial_state(self, triples: list[Triple], gadget: Gadget | None):
        assert len(triples) == self.T
        assert (gadget is not None) == self.has_gadget
        self.triples = list(sorted(triples))
        self.gadget = gadget
        adjacency = [set() for _ in range(self.order)]
        for u, v in self.core.edges:
            adjacency[u].add(v)
            adjacency[v].add(u)
        for slot, triple in enumerate(self.triples):
            hub = self.hub_of_slot[slot]
            for v in triple:
                adjacency[hub].add(v)
                adjacency[v].add(hub)
        if self.has_gadget:
            adjacency[self.left_hub].add(self.right_hub)
            adjacency[self.right_hub].add(self.left_hub)
            for v in gadget[0]:
                adjacency[self.left_hub].add(v)
                adjacency[v].add(self.left_hub)
            for v in gadget[1]:
                adjacency[self.right_hub].add(v)
                adjacency[v].add(self.right_hub)
        self.adjacency = adjacency
        self.cycles = {4: full_cycles(adjacency, 4), 8: full_cycles(adjacency, 8)}
        self.cycles16_on = not self.cycles[4] and not self.cycles[8]
        if self.cycles16_on:
            self.cycles[16] = full_cycles(adjacency, 16)

    # -- ruin selection --------------------------------------------------
    def choose_ruin(self, k_min: int, k_max: int, gadget_prob: float):
        active_length = 4 if self.cycles[4] else 8 if self.cycles[8] else 16
        pool = self.cycles.get(active_length)
        implicated_slots: list[int] = []
        implicated_gadget = False
        if pool:
            target = self.rng.choice(tuple(pool))
            for vertex in target:
                if vertex in self.hub_of_slot:
                    implicated_slots.append(self.hub_of_slot.index(vertex))
                elif self.has_gadget and vertex in (self.left_hub, self.right_hub):
                    implicated_gadget = True
        k = self.rng.randint(k_min, min(k_max, self.T))
        selected = set(implicated_slots[: max(1, k // 3)])
        while len(selected) < k:
            selected.add(self.rng.randrange(self.T))
        selected = sorted(selected)
        include_gadget = self.has_gadget and (
            implicated_gadget or self.rng.random() < gadget_prob
        )
        return selected, include_gadget

    # -- recreate ----------------------------------------------------------
    def build_cp_model(self, freed: frozenset[int], include_gadget: bool,
                        forbidden_triple_combo, forbidden_gadget_combo,
                        rng_seed: int):
        model = cp_model.CpModel()
        cand_triples = candidates_within(
            freed, self.triple_by_vertex, lambda t: t,
        )
        t_var = {t: model.new_bool_var(f"t{i}") for i, t in enumerate(cand_triples)}
        incident: dict[int, list] = {v: [] for v in freed}
        for triple, var in t_var.items():
            for v in triple:
                incident[v].append(var)
        g_var = {}
        if include_gadget:
            cand_gadgets = candidates_within(
                freed, self.gadget_by_vertex, lambda g: g[0] + g[1],
            )
            g_var = {g: model.new_bool_var(f"g{i}") for i, g in enumerate(cand_gadgets)}
            for gadget, var in g_var.items():
                for v in gadget[0] + gadget[1]:
                    incident[v].append(var)
            if g_var:
                model.add_exactly_one(list(g_var.values()))
        for vertex in freed:
            if not incident[vertex]:
                return None, None, None
            model.add_exactly_one(incident[vertex])
        for combo in forbidden_triple_combo:
            variables = [t_var[t] for t in combo if t in t_var]
            if len(variables) == len(combo):
                model.add(sum(variables) <= len(combo) - 1)
        for combo in forbidden_gadget_combo:
            variables = [g_var[g] for g in combo if g in g_var]
            if len(variables) == len(combo):
                model.add(sum(variables) <= len(combo) - 1)
        return model, t_var, g_var

    def try_ruin_recreate(self, k_min: int, k_max: int, gadget_prob: float,
                          max_attempts: int, cp_time_limit: float,
                          temperature: float) -> dict | None:
        selected_slots, include_gadget = self.choose_ruin(
            k_min, k_max, gadget_prob,
        )
        old_triples = {slot: self.triples[slot] for slot in selected_slots}
        freed = set(v for triple in old_triples.values() for v in triple)
        old_gadget = None
        if include_gadget:
            old_gadget = self.gadget
            freed.update(old_gadget[0] + old_gadget[1])
        freed = frozenset(freed)

        forbidden_triples: list[frozenset] = [frozenset(old_triples.values())]
        forbidden_gadgets: list[frozenset] = (
            [frozenset({old_gadget})] if include_gadget else []
        )

        for attempt in range(max_attempts):
            model, t_var, g_var = self.build_cp_model(
                freed, include_gadget, forbidden_triples, forbidden_gadgets,
                rng_seed=self.rng.randrange(2 ** 31),
            )
            if model is None:
                return None
            solver = cp_model.CpSolver()
            solver.parameters.num_search_workers = 1
            solver.parameters.random_seed = self.rng.randrange(2 ** 31)
            solver.parameters.max_time_in_seconds = cp_time_limit
            status = solver.solve(model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                return None
            new_triples = [t for t, var in t_var.items() if solver.value(var)]
            new_gadget = None
            if include_gadget:
                chosen = [g for g, var in g_var.items() if solver.value(var)]
                assert len(chosen) == 1
                new_gadget = chosen[0]
            assert len(new_triples) == len(old_triples)

            removed_edges: set[tuple[int, int]] = set()
            added_edges: set[tuple[int, int]] = set()
            for slot, new_triple in zip(sorted(old_triples), sorted(new_triples)):
                hub = self.hub_of_slot[slot]
                removed_edges |= hub_edges(hub, old_triples[slot])
                added_edges |= hub_edges(hub, new_triple)
            if include_gadget:
                removed_edges |= hub_edges(self.left_hub, old_gadget[0])
                removed_edges |= hub_edges(self.right_hub, old_gadget[1])
                added_edges |= hub_edges(self.left_hub, new_gadget[0])
                added_edges |= hub_edges(self.right_hub, new_gadget[1])
            # Edges present both before and after (e.g. a triple reassigned
            # to a different slot but otherwise unchanged) are no-ops.
            common = removed_edges & added_edges
            removed_edges -= common
            added_edges -= common

            for u, v in removed_edges:
                self.adjacency[u].discard(v)
                self.adjacency[v].discard(u)
            for u, v in added_edges:
                self.adjacency[u].add(v)
                self.adjacency[v].add(u)

            proposed = {}
            proposed[4] = update_cycles(
                self.cycles[4], self.adjacency, removed_edges, added_edges, 4,
            )
            reject = bool(self.cycles[4] == set() and proposed[4])
            if not reject:
                proposed[8] = update_cycles(
                    self.cycles[8], self.adjacency, removed_edges, added_edges, 8,
                )
                reject = bool(self.cycles[8] == set() and proposed[8])
            if not reject and self.cycles16_on:
                proposed[16] = update_cycles(
                    self.cycles[16], self.adjacency, removed_edges, added_edges, 16,
                )
            elif not reject and not proposed[4] and not proposed[8]:
                proposed[16] = full_cycles(self.adjacency, 16)

            accept = False
            if not reject:
                current_score = score_state(self.cycles)
                new_score = score_state(proposed)
                if current_score[0] or current_score[1]:
                    old_value = current_score[0] * 10 ** 8 + current_score[1] * 10 ** 5
                    new_value = new_score[0] * 10 ** 8 + new_score[1] * 10 ** 5
                else:
                    old_value, new_value = current_score[2], new_score[2]
                accept = (
                    new_value <= old_value or
                    self.rng.random() < math.exp(
                        max(-700, (old_value - new_value) / max(temperature, 1e-6)),
                    )
                )

            if accept:
                for slot, new_triple in zip(sorted(old_triples), sorted(new_triples)):
                    self.triples[slot] = new_triple
                if include_gadget:
                    self.gadget = new_gadget
                self.cycles.update(proposed)
                if 16 in proposed:
                    self.cycles16_on = True
                return {
                    "attempts": attempt + 1,
                    "ruin_size": len(old_triples) + (4 if include_gadget else 0),
                    "gadget_ruined": include_gadget,
                }
            # revert and try another recreation of the same freed set
            for u, v in added_edges:
                self.adjacency[u].discard(v)
                self.adjacency[v].discard(u)
            for u, v in removed_edges:
                self.adjacency[u].add(v)
                self.adjacency[v].add(u)
            forbidden_triples.append(frozenset(new_triples))
            if include_gadget:
                forbidden_gadgets.append(frozenset({new_gadget}))
        return None

    def audit(self) -> None:
        for length in (4, 8) + ((16,) if self.cycles16_on else ()):
            assert self.cycles[length] == full_cycles(self.adjacency, length), length

    def materialize_current(self):
        return materialize(self.core, list(self.triples), self.gadget)


def deep_verify(core, triples, gadget) -> dict:
    """Exhaustive short-cycle check plus a NetworkX-based cross-check."""
    graph, adjacency, _, hubs = materialize(core, triples, gadget)
    order = graph.number_of_nodes()
    lengths = powers_up_to(order)
    report = {}
    for length in lengths:
        cycles, truncated = enumerate_cycles_exact(adjacency, length, 1)
        report[str(length)] = {
            "exhaustive_zero": (not cycles) and not truncated,
            "witness": list(cycles[0]) if cycles else None,
        }
        if not cycles:
            independent = edge_path_cycle(adjacency, length)
            report[str(length)]["edge_path_independent_check_zero"] = independent is None
    return {"order": order, "forbidden_cycle_lengths": list(lengths), "report": report}


def networkx_cross_check(graph: nx.Graph, lengths) -> dict:
    """A third, structurally different cycle search using NetworkX."""
    result = {}
    for length in lengths:
        found = None
        for cycle in nx.simple_cycles(graph, length_bound=length):
            if len(cycle) == length:
                found = cycle
                break
        result[str(length)] = {"found": found is not None, "witness": found}
    return result


def save_completion(core, instance_name: str, triples, gadget,
                    cycles_summary: dict, tag: str, extra: dict) -> Path:
    graph, adjacency, _, hubs = materialize(core, triples, gadget)
    lengths = powers_up_to(graph.number_of_nodes())
    witnesses = first_cycle_profile(adjacency, lengths)
    payload = {
        "status": tag,
        "parameters": {"j": core.j, "Y": core.Y, "a": core.a, "c": core.c},
        "instance": instance_name,
        "method": "large_neighborhood_search",
        "best_short_cycle_counts": cycles_summary,
        "power_cycle_witnesses": witnesses,
        "completion": {
            "triples": [list(item) for item in sorted(triples)],
            "linked_pairs": [list(pair) for pair in gadget] if gadget else None,
            "edges": [list(edge) for edge in sorted(graph.edges())],
            **graph_encodings(graph),
        },
        **extra,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"lns_{instance_name}_{tag}.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return path


def run(instance_name: str, j: int, a: int, c: int, start_path: Path, seed: int,
       time_budget: float, k_min: int, k_max: int, gadget_prob: float,
       max_attempts: int, cp_time_limit: float, checkpoint_seconds: float,
       audit_every: int, log_path: Path | None) -> dict:
    core = build_core(j, a, c)
    lns = LNSInstance(core, seed)

    start_payload = json.loads(
        gzip.open(start_path, "rt").read() if start_path.suffix == ".gz"
        else start_path.read_text()
    )
    completion = start_payload.get("completion", start_payload)
    triples0 = [tuple(sorted(t)) for t in completion["triples"]]
    gadget0 = None
    if completion.get("linked_pairs"):
        pair_list = [tuple(sorted(p)) for p in completion["linked_pairs"]]
        gadget0 = tuple(sorted(pair_list))
    lns.initial_state(triples0, gadget0)

    best_score = score_state(lns.cycles)
    best_triples = list(lns.triples)
    best_gadget = lns.gadget
    log_lines = []

    def log(msg: str) -> None:
        line = f"[{time.strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        log_lines.append(line)
        if log_path is not None:
            log_path.write_text("\n".join(log_lines) + "\n")

    log(
        f"start {instance_name}: T={lns.T} order={lns.order} "
        f"initial_score={best_score}",
    )

    started = time.monotonic()
    rounds = 0
    accepted = 0
    last_checkpoint = started
    temperature_span = time_budget

    saved_paths = []
    while time.monotonic() - started < time_budget:
        rounds += 1
        elapsed = time.monotonic() - started
        # Temperature anneals over the whole run; a floor keeps some
        # exploration alive so the search does not freeze permanently.
        temperature = max(2.0, 400.0 * (1 - elapsed / max(temperature_span, 1)))
        outcome = lns.try_ruin_recreate(
            k_min, k_max, gadget_prob, max_attempts, cp_time_limit, temperature,
        )
        if outcome is not None:
            accepted += 1
            score = score_state(lns.cycles)
            if score < best_score:
                best_score = score
                best_triples = list(lns.triples)
                best_gadget = lns.gadget
                log(
                    f"round {rounds}: NEW BEST {best_score} "
                    f"(ruin_size={outcome['ruin_size']}, "
                    f"gadget_ruined={outcome['gadget_ruined']}, "
                    f"attempts={outcome['attempts']})",
                )
                triples_for_save = list(best_triples)
                gadget_for_save = best_gadget
                if best_score == (0, 0, 0):
                    tag = "COUNTEREXAMPLE_CANDIDATE"
                    log("!!! (C4,C8,C16) = (0,0,0) reached -- deep-verifying now")
                    deep = deep_verify(core, triples_for_save, gadget_for_save)
                    log(f"deep_verify: {json.dumps(deep, sort_keys=True)[:2000]}")
                    graph, _, _, _ = materialize(core, triples_for_save, gadget_for_save)
                    nx_check = networkx_cross_check(
                        graph, deep["forbidden_cycle_lengths"],
                    )
                    log(f"networkx_cross_check: {json.dumps(nx_check, sort_keys=True)}")
                    struct = validate_partition(core, {
                        "triples": [list(t) for t in triples_for_save],
                        "linked_pairs": (
                            [list(p) for p in gadget_for_save]
                            if gadget_for_save else None
                        ),
                    })
                    struct.pop("adjacency", None)
                    path = save_completion(
                        core, instance_name, triples_for_save, gadget_for_save,
                        {str(k): len(v) for k, v in lns.cycles.items() if k in (4, 8, 16)},
                        tag,
                        {
                            "deep_verification": deep,
                            "networkx_cross_check": nx_check,
                            "structural_check": struct,
                            "search_rounds": rounds,
                            "elapsed_seconds": round(elapsed, 3),
                        },
                    )
                    saved_paths.append(path)
                    log(f"SAVED CANDIDATE COUNTEREXAMPLE to {path}")
                else:
                    tag = f"c4_{best_score[0]}_c8_{best_score[1]}_c16_{best_score[2]}"
                    struct = validate_partition(core, {
                        "triples": [list(t) for t in triples_for_save],
                        "linked_pairs": (
                            [list(p) for p in gadget_for_save]
                            if gadget_for_save else None
                        ),
                    })
                    struct.pop("adjacency", None)
                    graph, adjacency, _, _ = materialize(
                        core, triples_for_save, gadget_for_save,
                    )
                    independent_zero_checks = {}
                    for length in (4, 8, 16):
                        if best_score[{4: 0, 8: 1, 16: 2}[length]] == 0:
                            independent_zero_checks[str(length)] = (
                                edge_path_cycle(adjacency, length) is None
                            )
                    path = save_completion(
                        core, instance_name, triples_for_save, gadget_for_save,
                        {"4": best_score[0], "8": best_score[1], "16": best_score[2]},
                        tag,
                        {
                            "structural_check": struct,
                            "independent_zero_checks": independent_zero_checks,
                            "search_rounds": rounds,
                            "elapsed_seconds": round(elapsed, 3),
                        },
                    )
                    saved_paths.append(path)
                    log(f"saved improved completion to {path}")
        if audit_every and rounds % audit_every == 0:
            lns.audit()
            log(f"round {rounds}: audit OK, accepted={accepted}, current={score_state(lns.cycles)}")
        if time.monotonic() - last_checkpoint > checkpoint_seconds:
            last_checkpoint = time.monotonic()
            log(
                f"round {rounds}: accepted={accepted} current={score_state(lns.cycles)} "
                f"best={best_score} elapsed={elapsed:.0f}s",
            )
        if best_score == (0, 0, 0):
            break

    lns.audit()
    elapsed_total = time.monotonic() - started
    summary = {
        "instance": instance_name,
        "parameters": {"j": j, "a": a, "c": c},
        "seed": seed,
        "rounds": rounds,
        "accepted": accepted,
        "elapsed_seconds": round(elapsed_total, 3),
        "best_score_c4_c8_c16": list(best_score),
        "saved_paths": [str(p) for p in saved_paths],
    }
    log(f"FINISHED {instance_name}: {json.dumps(summary, sort_keys=True)}")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instance", required=True)
    parser.add_argument("--j", type=int, required=True)
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--start", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--time-budget", type=float, default=1800.0)
    parser.add_argument("--k-min", type=int, default=6)
    parser.add_argument("--k-max", type=int, default=14)
    parser.add_argument("--gadget-prob", type=float, default=0.2)
    parser.add_argument("--max-attempts", type=int, default=12)
    parser.add_argument("--cp-time-limit", type=float, default=2.0)
    parser.add_argument("--checkpoint-seconds", type=float, default=60.0)
    parser.add_argument("--audit-every", type=int, default=200)
    parser.add_argument("--log", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(
        args.instance, args.j, args.a, args.c, args.start, args.seed,
        args.time_budget, args.k_min, args.k_max, args.gadget_prob,
        args.max_attempts, args.cp_time_limit, args.checkpoint_seconds,
        args.audit_every, args.log,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
