#!/usr/bin/env python3
"""
Coarser structural classification pass: instead of exact (canonicalized,
absolute-position) motifs, classify each chord in a minimal witness by
*endpoint type* (a, y, z/z1/z2, or interior path vertex), and each witness
by its multiset of chord-types + chord count. This is what actually
generalizes across candidates with different chord placements, since exact
path positions are not comparable across differently-sized role
configurations, but "does the witness use a chord touching z" is.

Reuses the per-candidate minimal-witness computation logic from
motif_mine.py (re-executed here, still fast: ~75s total).
"""
import json, time
import networkx as nx
from collections import Counter, defaultdict
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motif_mine import (FAMILIES, FILES, load_candidates, symbol, edge_set_of_walk,
                         chords_used, analyze_candidate)

def chord_type(fam, u, v):
    su, sv = symbol(fam, u), symbol(fam, v)
    kind = lambda s: ("a" if s == "a" else "y" if s == "y" else
                       "z" if s in ("z", "z1", "z2") else "p")
    ku, kv = sorted([kind(su), kind(sv)])
    return f"{ku}-{kv}"

def witness_type_signature(fam, chordset):
    types = sorted(chord_type(fam, u, v) for u, v in chordset)
    return (len(chordset), tuple(types))

def main():
    t0 = time.time()
    type_sig_counts = defaultdict(lambda: defaultdict(Counter))  # wtype -> family -> sig -> n_witnesses
    type_sig_cand_coverage = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))  # wtype -> family -> sig -> set(cand_id) [candidates where this sig occurs as a MINIMAL witness]
    per_family_all_min_have_z = defaultdict(lambda: defaultdict(list))  # wtype -> family -> list of bool (does EVERY minimal witness for this candidate use >=1 z-chord?)

    for fam in FAMILIES:
        cands = load_candidates(fam)
        for cand in cands:
            r = analyze_candidate(fam, cand)
            cid = cand.get("id")
            for wtype, minset in (("c16", r["c16_min"]), ("p6", r["p6_min"]), ("p14", r["p14_min"])):
                sigs_this_cand = []
                for cs in minset:
                    sig = witness_type_signature(fam, cs)
                    type_sig_counts[wtype][fam][sig] += 1
                    type_sig_cand_coverage[wtype][fam][sig].add(cid)
                    sigs_this_cand.append(sig)
                all_have_z = all(any(t.startswith("z") or t.endswith("z") for t in sig[1]) for sig in sigs_this_cand) if sigs_this_cand else False
                any_have_z = any(any(t.startswith("z") or t.endswith("z") for t in sig[1]) for sig in sigs_this_cand) if sigs_this_cand else False
                exists_pure_p_witness = any(all(t == "p-p" for t in sig[1]) for sig in sigs_this_cand)
                per_family_all_min_have_z[wtype][fam].append((all_have_z, any_have_z, exists_pure_p_witness))

    print("time:", time.time() - t0)
    print()
    for wtype in ("c16", "p6", "p14"):
        print(f"=== {wtype}: chord-type-signature frequency (n_witnesses observed, n_candidates_covering) ===")
        for fam in FAMILIES:
            n = len(load_candidates(fam))
            sigs = type_sig_counts[wtype][fam]
            top = sorted(sigs.items(), key=lambda kv: -kv[1])
            print(f"  [{fam}] n_cand={n}")
            for sig, cnt in top[:12]:
                ncov = len(type_sig_cand_coverage[wtype][fam][sig])
                print(f"      {sig}: n_witness_occurrences={cnt}  n_candidates_using_as_minimal={ncov}")
        print()

    print("=== does EVERY minimal witness for a candidate involve a z-chord? (all_have_z, any_have_z, exists_pure_p-p_witness) ===")
    for wtype in ("c16", "p6", "p14"):
        print(f" -- {wtype} --")
        for fam in FAMILIES:
            data = per_family_all_min_have_z[wtype][fam]
            n = len(data)
            n_all_z = sum(1 for a, b, c in data if a)
            n_any_z = sum(1 for a, b, c in data if b)
            n_pure_p_exists = sum(1 for a, b, c in data if c)
            print(f"   [{fam}] n={n}  all_minimal_witnesses_use_z={n_all_z}  some_minimal_witness_uses_z={n_any_z}  pure_p-p_witness_exists={n_pure_p_exists}")

if __name__ == "__main__":
    main()
