#!/usr/bin/env python3
"""Complete static unary/binary C4 and C8 conflicts for Type-T multipoles."""

from __future__ import annotations

import argparse
import gzip
import json
import time
from collections import Counter
from pathlib import Path

from type_t_port_c16_hypergraph import Gadget, Passage, gadget_catalog
from type_t_port_core_export import build_core


def core_paths(core, maximum: int):
    deficient = set(core.deficient_vertices())
    adjacency = core.adjacency()
    paths = []
    by_endpoints = {}
    for start in sorted(deficient):
        path = [start]
        used = {start}

        def visit(vertex: int, depth: int) -> None:
            if depth and vertex in deficient and start < vertex:
                record = tuple(path)
                paths.append(record)
                by_endpoints.setdefault((start, vertex), []).append(record)
            if depth == maximum:
                return
            for neighbor in adjacency[vertex]:
                if neighbor not in used:
                    used.add(neighbor)
                    path.append(neighbor)
                    visit(neighbor, depth + 1)
                    path.pop()
                    used.remove(neighbor)

        visit(start, 0)
    paths.sort(key=lambda item: (len(item), item))
    return paths, by_endpoints


def passage_index(passages: dict[int, list[Passage]]):
    unique = {}
    for items in passages.values():
        for passage in items:
            key = (
                passage.gadget, min(passage.left, passage.right),
                max(passage.left, passage.right), passage.length,
                passage.hub_tokens,
            )
            unique[key] = passage
    by_pair = {}
    for passage in unique.values():
        pair = tuple(sorted((passage.left, passage.right)))
        by_pair.setdefault(pair, []).append(passage)
    for pair in by_pair:
        by_pair[pair].sort(key=lambda item: (
            item.gadget, item.length, item.hub_tokens,
        ))
    return by_pair


def co_selectable(first: Passage, second: Passage,
                  gadgets: dict[int, Gadget]) -> bool:
    if first.gadget == second.gadget:
        return (
            first.linked and second.linked and
            set(first.hub_tokens).isdisjoint(second.hub_tokens)
        )
    left = gadgets[first.gadget]
    right = gadgets[second.gadget]
    if left.kind == right.kind == "linked_pairs":
        return False
    return set(left.attachments).isdisjoint(right.attachments)


def oriented(passage: Passage, left: int, right: int) -> dict:
    assert {passage.left, passage.right} == {left, right}
    return {
        "gadget": passage.gadget,
        "left": left,
        "right": right,
        "length": passage.length,
        "hub_tokens": list(passage.hub_tokens),
        "passage_kind": passage.passage_kind,
    }


def compile_short(core) -> dict:
    started = time.monotonic()
    gadgets, passages, _, _ = gadget_catalog(core)
    by_pair = passage_index(passages)
    paths, by_endpoints = core_paths(core, 6)
    records = {4: {}, 8: {}}
    literal_cycles = Counter()

    # One passage plus one core path.  The allowed-gadget construction should
    # make this empty, but compiling it independently checks that premise.
    for pair, candidates in by_pair.items():
        for passage in candidates:
            for target in (4, 8):
                needed = target - passage.length
                for path in by_endpoints.get(pair, ()):
                    if len(path) - 1 != needed:
                        continue
                    support = (passage.gadget,)
                    records[target].setdefault(support, {
                        "support": list(support),
                        "support_size": 1,
                        "core_paths": [list(path)],
                        "passages": [oriented(
                            passage, path[-1], path[0],
                        )],
                        "gadgets": [gadgets[passage.gadget].to_json()],
                    })
                    literal_cycles[target] += 1

    # Two passages plus two vertex-disjoint core paths.  For C8 their total
    # core length is at most four; C4 is included as a completeness check.
    short_paths = [path for path in paths if len(path) - 1 <= 4]
    for first_index, first_path in enumerate(short_paths):
        first_vertices = set(first_path)
        for second_path in short_paths[first_index + 1:]:
            if first_vertices.intersection(second_path):
                continue
            for reverse in (False, True):
                other = second_path[::-1] if reverse else second_path
                pair_one = tuple(sorted((first_path[-1], other[0])))
                pair_two = tuple(sorted((other[-1], first_path[0])))
                for first_passage in by_pair.get(pair_one, ()):
                    for second_passage in by_pair.get(pair_two, ()):
                        if not co_selectable(first_passage, second_passage, gadgets):
                            continue
                        length = (
                            len(first_path) - 1 + len(other) - 1 +
                            first_passage.length + second_passage.length
                        )
                        if length not in records:
                            continue
                        support = tuple(sorted({
                            first_passage.gadget, second_passage.gadget,
                        }))
                        record = {
                            "support": list(support),
                            "support_size": len(support),
                            "core_paths": [list(first_path), list(other)],
                            "passages": [
                                oriented(
                                    first_passage, first_path[-1], other[0],
                                ),
                                oriented(
                                    second_passage, other[-1], first_path[0],
                                ),
                            ],
                            "gadgets": [
                                gadgets[variable].to_json() for variable in support
                            ],
                        }
                        records[length].setdefault(support, record)
                        literal_cycles[length] += 1

    combined = {}
    for length in (4, 8):
        for support, record in records[length].items():
            combined.setdefault(support, {**record, "cycle_lengths": []})[
                "cycle_lengths"
            ].append(length)
    ordered = sorted(combined.values(), key=lambda item: (
        item["support_size"], item["support"],
    ))
    unary = {
        record["support"][0] for record in ordered
        if record["support_size"] == 1
    }
    minimal = [
        record for record in ordered
        if record["support_size"] == 1 or
        unary.isdisjoint(record["support"])
    ]
    return {
        "status": "PASS",
        "complete": True,
        "method": "one/two weighted passages joined by exhaustive simple core paths",
        "completeness": (
            "a C4 or C8 has at most floor(L/3) selected hub passages; "
            "allowed unary passages are compiled directly and three passages "
            "already require at least nine edges"
        ),
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "core_paths_enumerated": len(paths),
        "literal_cycles_by_length": {
            str(key): value for key, value in sorted(literal_cycles.items())
        },
        "raw_supports_by_length": {
            str(length): len(records[length]) for length in (4, 8)
        },
        "minimal_supports": len(minimal),
        "support_size_distribution": {
            str(key): value for key, value in sorted(Counter(
                item["support_size"] for item in minimal
            ).items())
        },
        "supports": minimal,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--j", type=int, required=True)
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compile_short(build_core(args.j, args.a, args.c))
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.suffix == ".gz":
            args.output.write_bytes(gzip.compress(rendered.encode(), mtime=0))
        else:
            args.output.write_text(rendered)


if __name__ == "__main__":
    main()
