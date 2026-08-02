#!/usr/bin/env python3
"""Verify the pure-combinatorics claims behind the proposed adaptive local-repair
search over triple-hub partitions of the deficient set (chat proposal, not tied
to any specific (j,a,c) instance):

1. M_m = (3m)! / (6^m * m!)  -- number of ways to repartition 3m touched
   vertices (from m touched triple hubs) into m new triples.
2. Exactly m! of those M_m repartitions preserve every one of the m original
   hub-triples (a bijection of the m "leftover" vertices onto the m triples).
3. The space of all t-triple partitions of a fixed 3t-element set is connected
   under two-block repartition moves, with diameter <= 2(t-1) (verified here
   by exhaustive BFS for small t; the move graph is vertex-transitive under
   S_{3t} relabelling, so eccentricity from one canonical partition equals the
   true diameter).
4. R_M = {2^k mod M : k>=2} for a Mersenne-flavoured modular safe-pole
   certificate.

Usage: python verifier/type_t_port_repair_combinatorics.py
"""

from __future__ import annotations

import itertools
import math
import time
from collections import deque


def M(m: int) -> int:
    return math.factorial(3 * m) // (6**m * math.factorial(m))


def verify_repartition_counts() -> None:
    print("=== M_m and preservation count (m! preserves the original m triples) ===")
    for m in range(2, 6):
        Mm = M(m)
        preserve = math.factorial(m)
        print(f"  m={m}: M_m={Mm:,}  preserve={preserve}  destroy={Mm - preserve:,}")


def _all_two_triple_splits(six: frozenset[int]) -> list[frozenset[frozenset[int]]]:
    elems = list(six)
    a = elems[0]
    rest = elems[1:]
    out = []
    for combo in itertools.combinations(rest, 2):
        t1 = frozenset((a,) + combo)
        t2 = frozenset(e for e in elems if e not in t1)
        out.append(frozenset([t1, t2]))
    return out


def _neighbors(partition: frozenset[frozenset[int]]) -> list[frozenset[frozenset[int]]]:
    blocks = list(partition)
    out = []
    for i in range(len(blocks)):
        for j in range(i + 1, len(blocks)):
            b1, b2 = blocks[i], blocks[j]
            rest = frozenset(blocks) - {b1, b2}
            for repart in _all_two_triple_splits(b1 | b2):
                if repart != frozenset([b1, b2]):
                    out.append(rest | repart)
    return out


def verify_diameter(t: int) -> None:
    elems = list(range(3 * t))
    start = frozenset(frozenset(elems[3 * i:3 * i + 3]) for i in range(t))
    t0 = time.time()
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in _neighbors(u):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    diam = max(dist.values())
    bound = 2 * (t - 1)
    status = "OK" if diam <= bound else "VIOLATED"
    print(f"  t={t}: states={len(dist):,} (expect M_t={M(t):,})  "
          f"diameter={diam}  bound 2(t-1)={bound}  {status}  "
          f"time={time.time() - t0:.1f}s")


def verify_modular_residues(M_: int, kmax: int = 200) -> None:
    residues = sorted({pow(2, k, M_) for k in range(2, kmax)})
    shifted = sorted((x - 2) % M_ for x in residues)
    print(f"  M={M_}: R_M={residues}  R_M-2 (mod M)={shifted}")


def main() -> None:
    verify_repartition_counts()
    print()
    print("=== connectivity diameter of the t-triple-partition move graph ===")
    for t in (3, 4):
        verify_diameter(t)
    print()
    print("=== modular safe-pole certificate residues ===")
    for m_ in (31, 127, 255):
        verify_modular_residues(m_)


if __name__ == "__main__":
    main()
