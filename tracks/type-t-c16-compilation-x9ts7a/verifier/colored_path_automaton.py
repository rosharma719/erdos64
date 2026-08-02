#!/usr/bin/env python3
"""Part IV.1 (defect-three phase): the minimal finite-state automaton for
the colored degree-2 path lemma -- "implementation 2," to be cross-checked
against the direct-construction search in colored_path_search.py
("implementation 1").

FORBIDDEN-CYCLE MECHANISMS (the only two ways a coloring chi:{1..t}->H of
a degree-2 path can create a C4 or C8, given no H-H edges and a single
path of C2 vertices -- derived by hand in defect_three.md Part IV.2):

  (a) single-H-vertex mechanism: chi(i)==chi(i+2) gives a C4 (H-v_i-v_{i+1}
      -v_{i+2}-H); chi(i)==chi(i+6) gives a C8 (H-v_i-...-v_{i+6}-H).
      Needs only the last 6 colors -- a sliding window suffices.

  (b) two-H-vertex mechanism (C8 only): two vertex-disjoint sub-intervals
      [i1,j1], [i2,j2] of the path (i1<j1<i2<j2), each with endpoint
      colors {u,v} for a FIXED pair of colors, whose edge-lengths
      (j1-i1)+(j2-i2) sum to exactly 4 (from the corrected weighted-
      incidence formula 2t+sum|P_i| at t=2 H-vertices, C8 <=> sum=4).
      Since both interval lengths must be >=1 and sum to 4, each length
      lies in {1,2,3}.

STATE DESIGN (proved finite below, not just "not observed to blow up"):
  - a sliding window of the last <=6 colors (bounds mechanism (a): 3^6
    values, dominated by a trivial pigeonhole since chi ranges over a
    fixed finite color set of size h<=3).
  - for each unordered color pair {u,v} and each closed arc-length
    L in {1,2,3} used by mechanism (b): an AGE counter, i.e. the number
    of path positions elapsed since the EARLIEST arc of that (pair,L)
    closed, SATURATED at a fixed cap once no future information can
    change the outcome.

WHY SATURATION KEEPS THE STATE SPACE FINITE (not an enumeration cutoff):
for a newly closing arc of length L2 at the current position to combine
with an earlier-closed arc of complementary length L1=4-L2 (L2<=3) into
two DISJOINT intervals, the earlier arc's closing position j1 must
satisfy (current position) - j1 > L2, i.e. age > L2. Since L2<=3 always
(both arc lengths lie in {1,2,3} by construction), an age of 4 or more
is ALREADY sufficient to guarantee disjointness against every possible
future L2 -- no additional distinction between age=4 and age=400 can
ever change a transition's outcome, so ages are capped at CAP=4 without
losing any information the transition function could use. This is a
structural argument (finite window x finite pair set x finite length
set x provably-safe saturation cap), not an empirical "we didn't see it
grow past N" claim.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.z3_certificate import compact_json  # noqa: E402
from verifier.colored_path_search import has_forbidden_cycle  # noqa: E402

CAP = 4
REJECT = "REJECT"


def initial_state(h: int):
    return ((), frozenset())


def step(state, c: int, h: int):
    """Returns REJECT or the successor state."""
    window, flags_fs = state
    t = len(window)
    if t >= 2 and window[-2] == c:
        return REJECT
    if t >= 6 and window[-6] == c:
        return REJECT

    flags = {(p, l): a for (p, l, a) in flags_fs}
    aged = {k: min(v + 1, CAP) for k, v in flags.items()}

    new_events = []
    for L in (1, 2, 3):
        if t >= L and window[-L] != c:
            pair = frozenset((c, window[-L]))
            new_events.append((pair, L))

    for pair, L in new_events:
        comp = (pair, 4 - L)
        if comp in aged and aged[comp] > L:
            return REJECT

    for pair, L in new_events:
        key = (pair, L)
        if key not in aged:
            aged[key] = 0

    new_window = (window + (c,))[-6:]
    new_flags = frozenset((p, l, a) for (p, l), a in aged.items())
    return (new_window, new_flags)


def explore(h: int) -> dict[str, Any]:
    """BFS over automaton STATES (not raw words) by length; collapses
    words reaching the same state, which is exactly the compression a
    finite automaton is supposed to provide over the raw word search."""
    level = {initial_state(h): ()}  # state -> a witness word reaching it
    max_valid_length = 0
    witness_per_length = {0: ()}
    levels_sizes = {0: 1}
    all_states: set[Any] = {initial_state(h)}
    edges: list[tuple[Any, int, Any]] = []
    reachable_by_length: dict[int, list[Any]] = {0: [initial_state(h)]}

    t = 0
    while level:
        next_level: dict[Any, tuple[int, ...]] = {}
        for state, word in level.items():
            for c in range(h):
                nxt = step(state, c, h)
                edges.append((state, c, nxt if nxt != REJECT else REJECT))
                if nxt == REJECT:
                    continue
                if nxt not in next_level:
                    next_level[nxt] = word + (c,)
        if not next_level:
            break
        t += 1
        levels_sizes[t] = len(next_level)
        witness_per_length[t] = next(iter(next_level.values()))
        max_valid_length = t
        reachable_by_length[t] = list(next_level.keys())
        all_states |= set(next_level.keys())
        level = next_level

    return {
        "h": h,
        "max_valid_length": max_valid_length,
        "levels_sizes": levels_sizes,
        "witness_per_length": {k: list(v) for k, v in witness_per_length.items()},
        "total_reachable_states": len(all_states),
        "total_transitions_explored": len(edges),
        "reachable_states_by_length": {
            str(k): len(v) for k, v in reachable_by_length.items()
        },
    }


def certificate_verify(coloring: tuple[int, ...], h: int) -> bool:
    """Standalone certificate verifier: replays a word purely through the
    automaton's transition table (no reference to graph construction at
    all), returns True iff it is accepted (never hits REJECT)."""
    state = initial_state(h)
    for c in coloring:
        state = step(state, c, h)
        if state == REJECT:
            return False
    return True


def cross_check(h: int, max_len_to_check: int = 9) -> dict[str, Any]:
    """Implementation-agreement cross-check: for every word up to length
    max_len_to_check (small, since true max is <=8), the automaton's
    accept/reject verdict must agree EXACTLY with the direct-construction
    detector in colored_path_search.py."""
    import itertools

    mismatches = []
    checked = 0
    for length in range(0, max_len_to_check + 1):
        for word in itertools.product(range(h), repeat=length):
            checked += 1
            automaton_ok = certificate_verify(word, h)
            bad, _ = has_forbidden_cycle(word, h) if word else (False, {})
            direct_ok = not bad
            if automaton_ok != direct_ok:
                mismatches.append({"word": list(word), "automaton_ok": automaton_ok, "direct_ok": direct_ok})
    return {"h": h, "words_checked": checked, "mismatches": mismatches}


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    expected = {1: 2, 2: 5, 3: 8}
    report: dict[str, Any] = {}
    all_ok = True
    for h in (1, 2, 3):
        r = explore(h)
        report[f"automaton_h{h}"] = r
        ok = r["max_valid_length"] == expected[h]
        all_ok &= ok
        print(f"h={h}: automaton max valid length = {r['max_valid_length']} "
              f"(expected {expected[h]}, match={ok}); "
              f"reachable states by length = {r['reachable_states_by_length']}")

    for h in (1, 2, 3):
        # cross-check up to expected[h]+1 (one past the true max, to also
        # confirm the automaton correctly rejects the first invalid length)
        cc = cross_check(h, max_len_to_check=expected[h] + 1)
        report[f"cross_check_h{h}"] = cc
        agree = not cc["mismatches"]
        all_ok &= agree
        print(f"h={h}: cross-check against direct construction over "
              f"{cc['words_checked']} words, mismatches={len(cc['mismatches'])}")

    encoded = compact_json(report)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(compact_json(report) + "\n")

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
