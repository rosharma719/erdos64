#!/usr/bin/env python3
"""Enumerate the finite first-edge states at the surviving Type-T pole.

This is a symbolic state audit, not a graph census or a SAT proof.  It checks
the set-partition/orbit count, degree compatibility, and the exact cycle
formulas in the prefix-only rooted core.  Arbitrary intersections after the
forced initial prefixes are deliberately not encoded.
"""

from __future__ import annotations

import json
from collections import defaultdict
from itertools import combinations, product


BRANCHES = ("A", "B", "C", "D")
SAME_THETA = ({"A", "B"}, {"C", "D"})
SWAP_XY = {"A": "C", "B": "D", "C": "A", "D": "B"}

LENGTH_LABELS = {
    "A": "2^rho_x-1",
    "B": "2^s_x",
    "C": "2^rho_y-1",
    "D": "2^s_y",
}

PREFERRED_REPRESENTATIVES = {
    "E2_parallel": (("A", "C"), ("B", "D")),
    "E2_cross": (("A", "D"), ("B", "C")),
    "E3_near": (("A", "C"), ("B",), ("D",)),
    "E3_power": (("A",), ("B", "D"), ("C",)),
    "E3_mixed": (("A", "D"), ("B",), ("C",)),
    "E4_discrete": (("A",), ("B",), ("C",), ("D",)),
}


def set_partitions(items: tuple[str, ...]):
    """Yield every set partition once, in a canonical tuple representation."""
    if not items:
        yield ()
        return
    first, *rest = items
    for partition in set_partitions(tuple(rest)):
        yield canonical_partition(((first,), *partition))
        for index in range(len(partition)):
            blocks = [tuple(block) for block in partition]
            blocks[index] = tuple((*blocks[index], first))
            yield canonical_partition(tuple(blocks))


def canonical_partition(partition):
    blocks = [tuple(sorted(block, key=BRANCHES.index)) for block in partition]
    return tuple(sorted(blocks, key=lambda block: tuple(BRANCHES.index(x) for x in block)))


def allowed(partition) -> bool:
    return all(not forbidden.issubset(block) for block in map(set, partition) for forbidden in SAME_THETA)


def xy_swap(partition):
    return canonical_partition(tuple(tuple(SWAP_XY[x] for x in block) for block in partition))


def orbit_key(partition):
    swapped = xy_swap(partition)
    return min(partition, swapped)


def equality_pairs(partition):
    return tuple("".join(block) for block in partition if len(block) == 2)


def state_name(partition):
    pairs = equality_pairs(partition)
    if len(partition) == 2:
        return "E2_parallel" if set(pairs) == {"AC", "BD"} else "E2_cross"
    if len(partition) == 3:
        pair = pairs[0]
        if pair == "AC":
            return "E3_near"
        if pair == "BD":
            return "E3_power"
        return "E3_mixed"
    if len(partition) == 4:
        return "E4_discrete"
    raise AssertionError(partition)


def branch_length(branch, rho_x, s_x, rho_y, s_y):
    values = {
        "A": 2**rho_x - 1,
        "B": 2**s_x,
        "C": 2**rho_y - 1,
        "D": 2**s_y,
    }
    return values[branch]


def outer_cycle_length(pair, rho_x, s_x, rho_y, s_y, prefix):
    """Prefix-only cycle closed by x'-x-y-y' (three edges)."""
    u, v = pair
    return (
        branch_length(u, rho_x, s_x, rho_y, s_y)
        + branch_length(v, rho_x, s_x, rho_y, s_y)
        - 2 * prefix
        + 3
    )


def is_dyadic_cycle(length):
    return length >= 4 and length & (length - 1) == 0


def add_expression(*expressions):
    total = defaultdict(int)
    for expression in expressions:
        for variable, coefficient in expression.items():
            total[variable] += coefficient
    return {variable: coefficient for variable, coefficient in total.items() if coefficient}


def core_edges(partition):
    """Build the suppressed prefix-only multigraph with symbolic weights."""
    terminal = {"A": "xprime", "B": "xprime", "C": "yprime", "D": "yprime"}
    edges = []
    for block in partition:
        if len(block) == 2:
            pair = "".join(block)
            split = f"w_{pair}"
            edges.append((f"prefix_{pair}", "z0", split, {f"h_{pair}": 1}))
            for branch in block:
                edges.append(
                    (
                        branch,
                        split,
                        terminal[branch],
                        {f"L_{branch}": 1, f"h_{pair}": -1},
                    )
                )
        else:
            branch = block[0]
            edges.append((branch, "z0", terminal[branch], {f"L_{branch}": 1}))
    edges.append(("K", "xprime", "yprime", {"K": 1}))
    return edges


def prefix_only_cycles(partition):
    """Enumerate every simple cycle of the suppressed weighted multigraph."""
    edges = core_edges(partition)
    cycles = []
    for size in range(2, len(edges) + 1):
        for subset in combinations(edges, size):
            degree = defaultdict(int)
            adjacency = defaultdict(set)
            for _, u, v, _ in subset:
                degree[u] += 1
                degree[v] += 1
                adjacency[u].add(v)
                adjacency[v].add(u)
            if any(value != 2 for value in degree.values()):
                continue
            stack = [next(iter(degree))]
            seen = set()
            while stack:
                vertex = stack.pop()
                if vertex in seen:
                    continue
                seen.add(vertex)
                stack.extend(adjacency[vertex] - seen)
            if len(seen) != len(degree):
                continue
            cycles.append(
                {
                    "edges": [edge[0] for edge in subset],
                    "expression": add_expression(*(edge[3] for edge in subset)),
                }
            )
    return cycles


def evaluate_expression(expression, exponents, prefixes):
    rho_x, s_x, rho_y, s_y = exponents
    values = {
        "L_A": 2**rho_x - 1,
        "L_B": 2**s_x,
        "L_C": 2**rho_y - 1,
        "L_D": 2**s_y,
        "K": 3,
        **{f"h_{pair}": value for pair, value in prefixes.items()},
    }
    return sum(coefficient * values[variable] for variable, coefficient in expression.items())


def core_arithmetic_audit(partition, max_exponent=6):
    pairs = equality_pairs(partition)
    cycles = prefix_only_cycles(partition)
    checked = 0
    failing = []
    safe = []
    for exponents in product(range(2, max_exponent + 1), repeat=4):
        prefix_ranges = []
        for pair in pairs:
            maximum = min(
                branch_length(pair[0], *exponents),
                branch_length(pair[1], *exponents),
            ) - 1
            prefix_ranges.append(range(1, maximum + 1))
        for prefix_values in product(*prefix_ranges):
            prefixes = dict(zip(pairs, prefix_values))
            lengths = [evaluate_expression(cycle["expression"], exponents, prefixes) for cycle in cycles]
            assert all(length >= 3 for length in lengths)
            checked += 1
            record = {
                "exponents": dict(zip(("rho_x", "s_x", "rho_y", "s_y"), exponents)),
                "prefixes": prefixes,
                "cycle_lengths": sorted(lengths),
            }
            bucket = failing if any(is_dyadic_cycle(length) for length in lengths) else safe
            if len(bucket) < 2:
                bucket.append(record)
    return {
        "cycles": cycles,
        "instances_checked": checked,
        "dyadic_examples": failing,
        "fully_non_dyadic_examples": safe,
    }


def arithmetic_audit(max_exponent=10):
    pair_results = {}
    for pair in ("AC", "AD", "BC", "BD"):
        prefix_hits = []
        prefix_safe = []
        zero_prefix_values = []
        checked = 0
        for exponents in product(range(2, max_exponent + 1), repeat=4):
            rho_x, s_x, rho_y, s_y = exponents
            zero = outer_cycle_length(pair, *exponents, 0)
            zero_prefix_values.append(zero)
            max_prefix = min(
                branch_length(pair[0], *exponents),
                branch_length(pair[1], *exponents),
            ) - 1
            for prefix in range(1, max_prefix + 1):
                checked += 1
                length = outer_cycle_length(pair, *exponents, prefix)
                record = {
                    "exponents": {
                        "rho_x": rho_x,
                        "s_x": s_x,
                        "rho_y": rho_y,
                        "s_y": s_y,
                    },
                    "prefix": prefix,
                    "cycle_length": length,
                }
                bucket = prefix_hits if is_dyadic_cycle(length) else prefix_safe
                if len(bucket) < 2:
                    bucket.append(record)

        if pair in ("AC", "BD"):
            assert all(value % 2 == 1 for value in zero_prefix_values)
            assert not prefix_hits
        else:
            assert all(value % 4 == 2 for value in zero_prefix_values)
            assert prefix_hits and prefix_safe

        pair_results[pair] = {
            "formula": {
                "AC": "2^rho_x+2^rho_y+1-2h",
                "AD": "2^rho_x+2^s_y+2-2h",
                "BC": "2^s_x+2^rho_y+2-2h",
                "BD": "2^s_x+2^s_y+3-2h",
            }[pair],
            "positive_prefix_instances_checked": checked,
            "dyadic_examples": prefix_hits,
            "non_dyadic_examples": prefix_safe,
        }
    return pair_results


def main():
    partitions = sorted(set(set_partitions(BRANCHES)))
    admissible = [partition for partition in partitions if allowed(partition)]
    relevant = [partition for partition in admissible if 2 <= len(partition) <= 4]
    orbits = {}
    for partition in relevant:
        orbits.setdefault(orbit_key(partition), []).append(partition)

    assert len(partitions) == 15
    assert len(relevant) == 7
    assert len(orbits) == 6
    assert sorted(len(partition) for partition in relevant) == [2, 2, 3, 3, 3, 3, 4]

    states = []
    names = set()
    for orbit_representative, members in sorted(orbits.items(), key=lambda item: (len(item[0]), item[0])):
        name = state_name(orbit_representative)
        representative = canonical_partition(PREFERRED_REPRESENTATIVES[name])
        assert representative in members
        assert name not in names
        names.add(name)
        first_edge_count = len(representative)
        min_degree = first_edge_count + 2  # the two triangle edges z_0x,z_0y
        states.append(
            {
                "state": name,
                "representative": [list(block) for block in representative],
                "xy_orbit_size": len(members),
                "first_edge_count": first_edge_count,
                "forced_shared_prefixes": list(equality_pairs(representative)),
                "minimum_degree_z0": min_degree,
                "degree_classes": {
                    "deg4": min_degree <= 4,
                    "deg5": min_degree <= 5,
                    "deg6_or_more": True,
                },
                "first_neighbor_core_degrees_if_prefixes_split_immediately": sorted(
                    len(block) + 1 for block in representative
                ),
                "prefix_only_core": core_arithmetic_audit(representative),
            }
        )

    assert names == {
        "E2_parallel",
        "E2_cross",
        "E3_near",
        "E3_power",
        "E3_mixed",
        "E4_discrete",
    }
    assert sum(state["degree_classes"]["deg4"] for state in states) == 2
    assert sum(state["degree_classes"]["deg5"] for state in states) == 5
    assert sum(state["degree_classes"]["deg6_or_more"] for state in states) == 6
    for state in states:
        core = state["prefix_only_core"]
        expected_cycles = 6 if state["state"] == "E4_discrete" else 7
        assert len(core["cycles"]) == expected_cycles
        assert core["fully_non_dyadic_examples"]
        if state["state"] == "E4_discrete":
            assert not core["dyadic_examples"]
        else:
            assert core["dyadic_examples"]

    arithmetic = arithmetic_audit()
    output = {
        "assertion_failures": 0,
        "scope": (
            "finite first-edge/orbit and prefix-only arithmetic audit; "
            "not a graph census and not a bound on later four-color intersections"
        ),
        "branch_lengths": LENGTH_LABELS,
        "raw_set_partitions": len(partitions),
        "admissible_labeled_partitions": len(relevant),
        "xy_symmetry_orbits": len(orbits),
        "states": states,
        "prefix_only_outer_cycles": arithmetic,
        "theorem": {
            "degree4": "exactly the two E2 states",
            "degree5": "the E2 and E3 states; an E2 state leaves one unused nontriangle edge",
            "degree6_or_more": "all six rooted orbit states are locally degree-compatible",
            "forced_dyadic_state": None,
            "universally_prefix_only_safe_state": "E4_discrete",
            "conditional_dyadic_pair_cycles": ["AD", "BC"],
            "conditional_four_color_cycle_states": [
                "E2_parallel",
                "E2_cross",
                "E3_near",
                "E3_power",
                "E3_mixed",
            ],
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
