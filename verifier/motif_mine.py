#!/usr/bin/env python3
"""
Exhaustive witness enumeration + canonical motif clustering across all six
Type-B candidate databases (B20, B20D2, gap2_e29, gap1_e29, gap2_e30, gap1_e30).

For every candidate:
  - enumerate ALL simple 16-cycles (internal C16 witnesses)
  - enumerate ALL simple a-y paths of length 6
  - enumerate ALL simple a-y paths of length 14
  - record the exact chord (non-path) edges each witness uses
  - compute inclusion-minimal witness chord-sets (per witness type, per candidate)
  - canonicalize each minimal chord-set under path reversal (+ z1<->z2 swap
    where applicable), expressing endpoints symbolically (a, y, z, z1, z2, or
    a path-position offset from the nearer distinguished endpoint)
  - cluster canonical motifs across the whole population

Output: JSON summary written to motif_summary.json, printed tables to stdout.
"""
import json, time, itertools
import networkx as nx
from collections import Counter, defaultdict

DATA = "/home/user/erdos64/data"

FAMILIES = {}

def register(name, nv, path_last, a, y, z_list, path_edges, reversal, zswap=None):
    FAMILIES[name] = dict(nv=nv, path_last=path_last, a=a, y=y, z_list=z_list,
                           path_edges=path_edges, reversal=reversal, zswap=zswap)

# B20 (family_ii): 19 vertices, path 0..17 (a=0,y=17), z=18
register("B20", 19, 17, 0, 17, [18],
          [(i, i+1) for i in range(17)],
          reversal=lambda v: 18 if v == 18 else 17 - v)

# B20D2 (delta2): 19 vertices, full path 0..18 (a=0,y=18), no z
register("B20D2", 19, 18, 0, 18, [],
          [(i, i+1) for i in range(18)],
          reversal=lambda v: 18 - v)

# gap2_e29 / gap2_e30: 20 vertices, path 0..18 (a=0,y=18), z=19
def gap2_reversal(v):
    return 19 if v == 19 else 18 - v
register("gap2_e29", 20, 18, 0, 18, [19],
          [(i, i+1) for i in range(18)], reversal=gap2_reversal)
register("gap2_e30", 20, 18, 0, 18, [19],
          [(i, i+1) for i in range(18)], reversal=gap2_reversal)

# gap1_e29 / gap1_e30: 20 vertices, path 0..17 (a=0,y=17), z1=18,z2=19
def gap1_reversal(v):
    if v in (18, 19):
        return v
    return 17 - v
def gap1_zswap(v):
    if v == 18: return 19
    if v == 19: return 18
    return v
register("gap1_e29", 20, 17, 0, 17, [18, 19],
          [(i, i+1) for i in range(17)], reversal=gap1_reversal, zswap=gap1_zswap)
register("gap1_e30", 20, 17, 0, 17, [18, 19],
          [(i, i+1) for i in range(17)], reversal=gap1_reversal, zswap=gap1_zswap)

FILES = {
    "B20":       ("type_b_slack_family_ii_graphs.json", "graphs"),
    "B20D2":     ("type_b_delta2_candidates.json", "graphs"),
    "gap2_e29":  ("type_b_order40_gap2_e29_graphs.json", "graphs"),
    "gap1_e29":  ("type_b_order40_gap1_e29_graphs.json", "graphs"),
    "gap2_e30":  ("type_b_order40_gap2_e30_graphs.json", "graphs"),
    "gap1_e30":  ("type_b_order40_gap1_e30_graphs.json", "graphs"),
}

def load_candidates(fam):
    fname, key = FILES[fam]
    d = json.load(open(f"{DATA}/{fname}"))
    return d[key]

def symbol(fam, v):
    """Map a vertex index to a symbolic label (a, y, z, z1, z2, or p+k)."""
    F = FAMILIES[fam]
    if v == F["a"]:
        return "a"
    if v == F["y"]:
        return "y"
    if v in F["z_list"]:
        if len(F["z_list"]) == 1:
            return "z"
        else:
            return "z1" if v == F["z_list"][0] else "z2"
    return f"p{v}"

def edge_set_of_walk(vlist, cyclic=False):
    n = len(vlist)
    edges = []
    rng = n if cyclic else n - 1
    for i in range(rng):
        u, v = vlist[i], vlist[(i + 1) % n]
        edges.append(tuple(sorted((u, v))))
    return edges

def chords_used(fam, edges):
    F = FAMILIES[fam]
    path_set = set(F["path_edges"]) | set((b, a) for a, b in F["path_edges"])
    return sorted(set(e for e in edges if e not in path_set and (e[1], e[0]) not in path_set))

def canonical_chordset(fam, chordset):
    F = FAMILIES[fam]
    maps = [lambda v: v]
    maps.append(F["reversal"])
    if F["zswap"] is not None:
        maps.append(F["zswap"])
        maps.append(lambda v, r=F["reversal"], z=F["zswap"]: z(r(v)))
    variants = []
    for m in maps:
        variant = tuple(sorted(tuple(sorted((m(u), m(v)))) for u, v in chordset))
        variants.append(variant)
    return min(variants)

def symbolic_chordset(fam, chordset):
    """Represent a canonical chordset using symbolic endpoints + path-offsets
    relative to nearest distinguished point, for cross-candidate comparability."""
    out = []
    for u, v in chordset:
        su, sv = symbol(fam, u), symbol(fam, v)
        out.append(tuple(sorted((su, sv))))
    return tuple(sorted(out))

def minimal_chordsets(list_of_chordsets):
    """Given a list of chord-sets (each a sorted tuple of edges), return the
    inclusion-minimal ones (no other set in the list is a proper subset)."""
    uniq = list(set(list_of_chordsets))
    minimal = []
    for cs in uniq:
        cs_set = set(cs)
        if any(set(other) < cs_set for other in uniq if other != cs):
            continue
        minimal.append(cs)
    return minimal

def analyze_candidate(fam, cand):
    F = FAMILIES[fam]
    nv, a, y = F["nv"], F["a"], F["y"]
    g = nx.Graph()
    g.add_nodes_from(range(nv))
    g.add_edges_from(F["path_edges"])
    g.add_edges_from(tuple(e) for e in cand["edges"])

    c16_cycles = [c for c in nx.simple_cycles(g, length_bound=16) if len(c) == 16]
    p6 = [p for p in nx.all_simple_paths(g, a, y, cutoff=6) if len(p) - 1 == 6]
    p14 = [p for p in nx.all_simple_paths(g, a, y, cutoff=14) if len(p) - 1 == 14]
    # sanity: also confirm no C4/C8 and no length-2 a-y path (should already hold)
    c4 = [c for c in nx.simple_cycles(g, length_bound=4) if len(c) == 4]
    c8 = [c for c in nx.simple_cycles(g, length_bound=8) if len(c) == 8]
    p2 = [p for p in nx.all_simple_paths(g, a, y, cutoff=2) if len(p) - 1 == 2]

    c16_chordsets = [tuple(chords_used(fam, edge_set_of_walk(c, cyclic=True))) for c in c16_cycles]
    p6_chordsets = [tuple(chords_used(fam, edge_set_of_walk(p, cyclic=False))) for p in p6]
    p14_chordsets = [tuple(chords_used(fam, edge_set_of_walk(p, cyclic=False))) for p in p14]

    c16_min = minimal_chordsets(c16_chordsets)
    p6_min = minimal_chordsets(p6_chordsets)
    p14_min = minimal_chordsets(p14_chordsets)

    return dict(
        n_c16=len(c16_cycles), n_p6=len(p6), n_p14=len(p14),
        n_c4=len(c4), n_c8=len(c8), n_p2=len(p2),
        c16_min=c16_min, p6_min=p6_min, p14_min=p14_min,
    )

def main():
    t0 = time.time()
    summary = {}
    all_canonical = defaultdict(lambda: defaultdict(Counter))  # witness_type -> canonical_symbolic -> family -> count
    chord_count_hist = defaultdict(lambda: defaultdict(Counter))  # witness_type -> family -> chord_count -> n_candidates(with that as a minimal count)
    anomalies = []

    for fam in FAMILIES:
        cands = load_candidates(fam)
        n = len(cands)
        fam_stats = dict(n=n, n_c4=0, n_c8=0, n_p2=0, n_no_c16=0, n_no_p6=0, n_no_p14=0)
        per_cand_records = []
        tfam0 = time.time()
        for cand in cands:
            r = analyze_candidate(fam, cand)
            if r["n_c4"] > 0: fam_stats["n_c4"] += 1
            if r["n_c8"] > 0: fam_stats["n_c8"] += 1
            if r["n_p2"] > 0: fam_stats["n_p2"] += 1
            if r["n_c16"] == 0: fam_stats["n_no_c16"] += 1
            if r["n_p6"] == 0: fam_stats["n_no_p6"] += 1
            if r["n_p14"] == 0: fam_stats["n_no_p14"] += 1

            for wtype, minset in (("c16", r["c16_min"]), ("p6", r["p6_min"]), ("p14", r["p14_min"])):
                # record chord-count of EACH minimal witness (a candidate may have several minimal witnesses)
                counts_this_cand = set()
                for cs in minset:
                    canon = canonical_chordset(fam, cs)
                    sym = symbolic_chordset(fam, canon)
                    all_canonical[wtype][sym][fam] += 1
                    counts_this_cand.add(len(cs))
                for cnt in counts_this_cand:
                    chord_count_hist[wtype][fam][cnt] += 1

            per_cand_records.append(dict(id=cand.get("id"), **{k: r[k] for k in ("n_c16","n_p6","n_p14")}))

        fam_stats["time"] = time.time() - tfam0
        summary[fam] = fam_stats
        print(f"[{fam}] n={n} time={fam_stats['time']:.2f}s "
              f"c4={fam_stats['n_c4']} c8={fam_stats['n_c8']} p2={fam_stats['n_p2']} "
              f"no_c16={fam_stats['n_no_c16']} no_p6={fam_stats['n_no_p6']} no_p14={fam_stats['n_no_p14']}",
              flush=True)

    print("\ntotal time:", time.time() - t0)

    # Dump for later inspection
    out = dict(
        family_stats=summary,
        chord_count_hist={wt: {f: dict(c) for f, c in fd.items()} for wt, fd in chord_count_hist.items()},
        canonical_motif_counts={
            wt: {str(sym): dict(fc) for sym, fc in motifs.items()}
            for wt, motifs in all_canonical.items()
        },
    )
    with open("/tmp/claude-0/-home-user-erdos64/5988522f-a4cb-541e-9a6f-b2047176cc0e/scratchpad/motif_summary.json", "w") as f:
        json.dump(out, f, indent=1)
    print("wrote motif_summary.json")

if __name__ == "__main__":
    main()
