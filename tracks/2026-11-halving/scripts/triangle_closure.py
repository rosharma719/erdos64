#!/usr/bin/env python3
# Usage: python3 triangle_closure.py [NMAX]   (default 31; the note used 63)
"""Clean three-poles in the triangle-substitution class.

A three-pole has three ports. Signature: (N, C, (P01, P02, P12)) where C is the set of internal
cycle lengths and Pij the set of lengths of simple paths between ports i and j (bitmasks).
The identity pole is a single vertex: N=1, no cycles, all path sets {0}.
Composition: take a triangle and replace its three corners by poles X0, X1, X2. Corner i keeps one
port as the new external port i and uses its other two ports for the triangle edges to the other
two corners. Each sub-pole is traversed at most once by any cycle or port path, so the signature
of the composite is determined exactly by the signatures of the parts.
A pole is CLEAN if no internal cycle has length 4, 8, 16, ...
"""
import itertools, sys
from functools import lru_cache
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 31
F = 0
k = 4
while k <= 4 * NMAX:
    F |= 1 << k; k *= 2
def msum(a, b):
    r = 0; i = 0; aa = a
    while aa:
        if aa & 1: r |= b << i
        aa >>= 1; i += 1
    return r
def pair(sig, i, j):
    i, j = min(i, j), max(i, j)
    return sig[2][{(0, 1): 0, (0, 2): 1, (1, 2): 2}[(i, j)]]
def canon(N, C, P):
    best = None
    for perm in itertools.permutations(range(3)):
        q = tuple(P[{(0, 1): 0, (0, 2): 1, (1, 2): 2}[tuple(sorted((perm[a], perm[b])))]] for a, b in ((0, 1), (0, 2), (1, 2)))
        if best is None or q < best: best = q
    return (N, C, best)
IDENT = (1, 0, (1, 1, 1))
def compose(X):
    """X = three (sig, role) with role = (ext, to_next, to_prev) port indices of the sub-pole."""
    N = sum(s[0] for s, _ in X)
    C = 0
    for s, _ in X: C |= s[1]
    inner = [pair(s, r[1], r[2]) for s, r in X]
    tri = msum(msum(inner[0], inner[1]), inner[2]) << 3
    C |= tri
    if C & F: return None
    P = []
    for i, j in ((0, 1), (0, 2), (1, 2)):
        kk = 3 - i - j
        def toward(a, b):   # port of corner a facing corner b
            s, r = X[a]
            return r[1] if (b - a) % 3 == 1 else r[2]
        si, ri = X[i]; sj, rj = X[j]; sk, rk = X[kk]
        direct = msum(pair(si, ri[0], toward(i, j)), pair(sj, toward(j, i), rj[0])) << 1
        via = msum(msum(pair(si, ri[0], toward(i, kk)), pair(sk, toward(kk, i), toward(kk, j))),
                   pair(sj, toward(j, kk), rj[0])) << 2
        P.append(direct | via)
    return canon(N, C, tuple(P))
ROLES = list(itertools.permutations(range(3)))
clean = {IDENT: None}
by_size = {1: {IDENT}}
for N in range(3, NMAX + 1, 2):
    found = {}
    sizes = [n for n in by_size]
    for a in sizes:
        for b in sizes:
            c = N - a - b
            if c not in by_size or not (a <= b <= c): continue
            for x in by_size[a]:
                for y in by_size[b]:
                    for z in by_size[c]:
                        for parts in set(itertools.permutations((x, y, z))):
                            for rs in itertools.product(ROLES, repeat=3):
                                sig = compose(list(zip(parts, rs)))
                                if sig is not None and sig not in found:
                                    found[sig] = (parts, rs)
    if found:
        by_size[N] = set(found)
        clean.update(found)
def show(m): 
    L = [i for i in range(m.bit_length()) if m >> i & 1]
    if L and L == list(range(L[0], L[-1] + 1)) and len(L) > 2: return f"[{L[0]},{L[-1]}]"
    return "{" + ",".join(map(str, L)) + "}"
for N in sorted(by_size):
    print(f"N={N}: {len(by_size[N])} clean signature(s)")
    for sig in sorted(by_size[N])[:6]:
        print("    paths:", [show(p) for p in sig[2]], " cycles:", show(sig[1]),
              " built from sizes:", None if clean[sig] is None else [p[0] for p in clean[sig][0]])
print("sizes with clean poles:", sorted(by_size))
