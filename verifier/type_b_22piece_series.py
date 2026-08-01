"""FB22-N: the Type-B closed-piece ("(2,*)-with-terminal-edge") C4/C8 series.

THE OBJECT.  Let {x,y} be a Type-B 2-cut of a minimal Erdos-Gyarfas
counterexample G (two_cut.md 2c: t=2, xy in E(G), a_1=a_2=1, deg_G(x)=3).
Let C_1,C_2 be the components of G-{x,y} and put

    J_i := G[C_i u {x,y}] = B_i + xy          (the "closed piece").

Then, purely by citation:
  * d_{J_i}(x) = a_i + 1 = 2                     (two_cut.md 2c)
  * d_{J_i}(y) = b_i + 1 >= 2                    (two_cut.md 1: b_i >= 1)
  * d_{J_i}(v) = deg_G(v) >= 3 for internal v    (two_cut.md T2 proof)
  * J_i is 2-connected                           (two_cut.md T1)
  * J_i is an induced subgraph of G, so it is {C4,C8,C16,...}-free
  * xy IS an edge of J_i                         (Type B)
  * n(G) = |V(J_1)| + |V(J_2)| - 2               (two_cut.md 26)

So a lower bound N0 on |V(J_i)| immediately gives n(G) >= 2*N0 - 2.

WHY THIS IS NOT FC-N.  verifier/type_c_fcn_series.py (FC-15) asks the same
degree question but with `xy NOT in E(B)`.  Here the terminal edge is
PRESENT.  The two families are disjoint, so FC-15 does not cover this case;
but they live in the same nauty-geng box, and this script confirms the
zero-survivor verdict is driven by the degree shape alone, not by the
xy-adjacency filter.

SEARCH BOX.  2|E(J)| >= 2 + 2 + 3(n-2) = 3n-2, so m >= m_min =
ceil((3n-2)/2); and J is {C4,C8}-free so m <= ex(n;{C4,C8}) (literature.md
L15).  For every n <= 17 except n=18.. this pins m exactly (m_min == ex(n))
or rules n out by counting.  With m pinned, the degree sequence is pinned
too:
    slack := 2*m_min - (3n-2)
    slack 0  (n even)  ->  degrees exactly 2,2,3^(n-2), so -D3
    slack 1  (n odd)   ->  one extra unit; -D4

ORDER 17 IS SPLIT.  At n=17, m=25=ex(17), slack 1, and d(y) in {2,3}:
  sub-case A: d(y)=3 -> degree sequence 2,3^16, max degree 3.  Searched
              directly here (-D3, 6,314 raw graphs).
  sub-case B: d(y)=2 -> degree sequence 2,2,4,3^14, max degree 4.  The -D4
              box at n=17 is far too large to enumerate, so this script
              instead settles it by DELETING the two terminals: H := J-{x,y}
              then has 15 vertices, 22 = ex(15;{C4,C8}) edges, is connected
              and {C4,C8}-free, and has degree sequence 2,3^14 or
              2,2,4,3^12.  Every extremal {C4,C8}-free 15-vertex graph is
              already enumerated by the n=15 layer of this same script, and
              none has either sequence.  `check_order_17_subcase_B` verifies
              exactly that.

Usage:  python verifier/type_b_22piece_series.py            # through n=17
        python verifier/type_b_22piece_series.py 14         # cheap subset
"""
from __future__ import annotations

import json
import random
import subprocess
import sys
from pathlib import Path

import networkx as nx

# ex(n;{C4,C8}), McKay extremal data, literature.md L15 / L15b table.
EX_C4C8 = {3: 3, 4: 4, 5: 6, 6: 7, 7: 9, 8: 11, 9: 12, 10: 14, 11: 15,
           12: 17, 13: 19, 14: 20, 15: 22, 16: 23, 17: 25, 18: 27, 19: 29,
           20: 31, 21: 33}

C_BINARY = Path("/tmp/check_power_masks_fb22")
RAW_CACHE = Path("/tmp/fb22_raw")


def compile_c_detector() -> None:
    src = Path(__file__).with_name("check_power_masks.c")
    proc = subprocess.run(["cc", "-O3", "-std=c11", str(src), "-o", str(C_BINARY)],
                          capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr)


def c_masks(records: list[str]) -> list[int]:
    payload = "".join(r + "\n" for r in records).encode()
    proc = subprocess.run([str(C_BINARY)], input=payload, capture_output=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode(errors="replace"))
    masks = [int(t) for t in proc.stdout.split() if t.lstrip(b"-" if isinstance(t, bytes) else "-").isdigit()]
    if len(masks) != len(records):
        raise RuntimeError(f"detector cardinality mismatch {len(masks)} vs {len(records)}")
    return masks


def has_len(G: nx.Graph, L: int) -> bool:
    """Independent Python DFS for an exact-length simple cycle."""
    for s in G:
        stack = [(s, {s}, 1)]
        while stack:
            v, seen, d = stack.pop()
            if d == L:
                if G.has_edge(v, s):
                    return True
                continue
            for w in G[v]:
                if w == s or w in seen or w < s:
                    continue
                stack.append((w, seen | {w}, d + 1))
    return False


def box(n: int) -> tuple[int, int, int]:
    t = 3 * n - 2
    m_min = -(-t // 2)
    return m_min, 2 * m_min - t, EX_C4C8[n]


def generate(n: int, m: int, cap: int) -> list[str]:
    RAW_CACHE.mkdir(exist_ok=True)
    path = RAW_CACHE / f"n{n}_m{m}_D{cap}.g6"
    if not path.exists():
        out = subprocess.run(
            ["nauty-geng", "-c", "-q", "-f", "-d2", f"-D{cap}", str(n), f"{m}:{m}"],
            capture_output=True, text=True).stdout
        path.write_text(out)
    return path.read_text().split()


def fb22_pairs(G: nx.Graph) -> list[tuple[int, int]]:
    """(x,y) with d(x)=2, d(y)>=2, xy IN E, every other vertex degree >=3,
    and the piece 2-connected -- the exact closed-piece profile."""
    out = []
    for x in [v for v in G if G.degree(v) == 2]:
        for y in G[x]:
            if G.degree(y) < 2:
                continue
            if any(G.degree(v) < 3 for v in G if v not in (x, y)):
                continue
            if nx.is_biconnected(G):
                out.append((x, y))
    return out


def shape_admissible(G: nx.Graph) -> bool:
    """xy-AGNOSTIC weakening: is there any (x,y), d(x)=2, d(y)>=2, all others
    >=3?  If False, both the FC-N (xy absent) and FB22 (xy present) variants
    are vacuous on G -- this is what shows FC-15's verdict is not an artefact
    of its `xy not in E` filter."""
    for x in [v for v in G if G.degree(v) == 2]:
        for y in G:
            if y != x and G.degree(y) >= 2 and all(
                    G.degree(v) >= 3 for v in G if v not in (x, y)):
                return True
    return False


def check_order(n: int, cap_override: int | None = None,
                reject_sample: int = 500, seed: int = 0) -> dict:
    m_min, slack, exn = box(n)
    if m_min > exn:
        return {"n": n, "status": "INFEASIBLE_BY_COUNTING",
                "m_min": m_min, "ex": exn, "slack": slack}
    if m_min != exn:
        return {"n": n, "status": "NOT_PINNED_OUT_OF_SCOPE",
                "m_min": m_min, "ex": exn, "slack": slack}
    cap = cap_override if cap_override is not None else (3 if slack == 0 else 4)
    raw = generate(n, m_min, cap)
    masks = c_masks(raw)
    free = [raw[i] for i, m in enumerate(masks) if not (m & 3)]

    # cross-check 1: every C-detector-clean graph, independently, in Python
    mism = sum(1 for r in free
               if has_len(nx.from_graph6_bytes(r.encode()), 4)
               or has_len(nx.from_graph6_bytes(r.encode()), 8))
    # cross-check 2: a random sample of the C-detector's rejects
    rej = [raw[i] for i, m in enumerate(masks) if (m & 3)]
    random.seed(seed)
    for r in random.sample(rej, min(reject_sample, len(rej))):
        G = nx.from_graph6_bytes(r.encode())
        if not (has_len(G, 4) or has_len(G, 8)):
            mism += 1

    shape_ok, survivors, seqs = 0, [], {}
    for r in free:
        G = nx.from_graph6_bytes(r.encode())
        seqs.setdefault(tuple(sorted(d for _, d in G.degree())), 0)
        seqs[tuple(sorted(d for _, d in G.degree()))] += 1
        if shape_admissible(G):
            shape_ok += 1
        survivors.extend((r, x, y) for x, y in fb22_pairs(G))
    return {"n": n, "status": "SEARCHED", "m": m_min, "ex": exn, "slack": slack,
            "cap": cap, "raw": len(raw), "c4c8_free": len(free),
            "reject_sample": min(reject_sample, len(rej)),
            "detector_disagreements": mism, "shape_admissible": shape_ok,
            "survivors": survivors,
            "free_degree_sequences": {str(list(k)): v for k, v in seqs.items()}}


def check_order_17_subcase_B() -> dict:
    """d(y)=2 at n=17 -> J-{x,y} is an extremal {C4,C8}-free 15-vertex graph
    with degree sequence 2,3^14 or 2,2,4,3^12.  Enumerate the n=15 extremal
    layer and confirm neither sequence occurs."""
    raw = generate(15, 22, 4)
    masks = c_masks(raw)
    free = [raw[i] for i, m in enumerate(masks) if not (m & 3)]
    wanted = {tuple(sorted([2] + [3] * 14)),
              tuple(sorted([2, 2, 4] + [3] * 12))}
    found, seqs = [], {}
    for r in free:
        G = nx.from_graph6_bytes(r.encode())
        s = tuple(sorted(d for _, d in G.degree()))
        seqs[str(list(s))] = seqs.get(str(list(s)), 0) + 1
        if s in wanted:
            found.append(r)
    return {"case": "n=17 sub-case B (d(y)=2) via terminal deletion",
            "n15_raw": len(raw), "n15_c4c8_free": len(free),
            "n15_free_degree_sequences": seqs,
            "target_sequences": [str(sorted([2] + [3] * 14)),
                                 str(sorted([2, 2, 4] + [3] * 12))],
            "matches": found, "eliminated": not found}


def main() -> None:
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 17
    compile_c_detector()
    report, clean = [], True
    hdr = (f"{'n':>3} {'status':>24} {'m':>4} {'ex':>4} {'slk':>4} {'cap':>4} "
           f"{'raw':>9} {'C4C8free':>9} {'shapeOK':>8} {'mismatch':>9} {'surv':>6}")
    print(hdr)
    for n in sorted(k for k in EX_C4C8 if k <= max_n):
        cap = 3 if n == 17 else None          # n=17 -D3 == sub-case A only
        r = check_order(n, cap_override=cap)
        report.append(r)
        if r["status"] != "SEARCHED":
            print(f"{n:>3} {r['status']:>24} {r['m_min']:>4} {r['ex']:>4} "
                  f"{r['slack']:>4} {'--':>4} {'--':>9} {'--':>9} {'--':>8} "
                  f"{'--':>9} {0:>6}")
            continue
        print(f"{n:>3} {r['status']:>24} {r['m']:>4} {r['ex']:>4} {r['slack']:>4} "
              f"{r['cap']:>4} {r['raw']:>9} {r['c4c8_free']:>9} "
              f"{r['shape_admissible']:>8} {r['detector_disagreements']:>9} "
              f"{len(r['survivors']):>6}")
        if r["survivors"] or r["detector_disagreements"]:
            clean = False
            print(f"  !!! n={n}: survivors={r['survivors'][:3]} "
                  f"mismatches={r['detector_disagreements']}")
    if max_n >= 17:
        b = check_order_17_subcase_B()
        report.append(b)
        print()
        print(f"n=17 sub-case B via terminal deletion: n=15 extremal layer has "
              f"{b['n15_c4c8_free']} {{C4,C8}}-free graphs, degree sequences "
              f"{b['n15_free_degree_sequences']}")
        print(f"  target sequences {b['target_sequences']} -> "
              f"{len(b['matches'])} matches; eliminated={b['eliminated']}")
        clean = clean and b["eliminated"]
    print()
    print("FB22-17 HOLDS: every Type-B closed piece has order >= 18, so a "
          "Type-B 2-cut forces n >= 34." if clean else
          "SURVIVOR OR MISMATCH -- do not trust the conclusion.")
    out = Path(__file__).resolve().parents[1] / "data" / "fb22_series_report.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=1))
    print(f"report -> {out}")


if __name__ == "__main__":
    main()
