"""Which finite sets P of positive integers have (m-fold sumset of P) ∩ {4,8,16,...} nonempty
for every m in a range?  Checks the necessary conditions derived by hand and looks at survivors."""
import itertools, math
from functools import reduce

def first_fail(P, M=400, start=3):
    S = {0}
    POW = {2**k for k in range(2, 40)}
    for m in range(1, M + 1):
        S = {s + p for s in S for p in P}
        if m >= start and not (S & POW):
            return m
    return None

def stats(P):
    a, b = min(P), max(P)
    g = reduce(math.gcd, [p - a for p in P], 0)
    godd = g
    while godd and godd % 2 == 0:
        godd //= 2
    e = (g // godd).bit_length() - 1 if g else 0
    return a, b, g, godd, e

N = 14
viol = {"ratio": 0, "odd": 0, "two": 0, "single": 0}
survivors = []
total = 0
for r in range(1, 5):
    for P in itertools.combinations(range(1, N + 1), r):
        total += 1
        a, b, g, godd, e = stats(P)
        f = first_fail(P)
        # (i) single length must fail at m=3
        if r == 1 and f != 3:
            viol["single"] += 1
        # (ii) odd part g' >= 3 of the gcd of differences forces a failure at some m <= g'
        if r > 1 and godd >= 3 and not (f is not None and f <= godd):
            viol["odd"] += 1
        # (iii) if 2^e does not divide a (e = 2-adic valuation of g), m = 3 fails
        if r > 1 and e >= 1 and a % (2**e) != 0 and f != 3:
            viol["two"] += 1
        # (iv) b < 2a forces a failure at some 3 <= m < 8a/(2a-b)
        if b < 2 * a and not (f is not None and f < 8 * a / (2 * a - b)):
            viol["ratio"] += 1
        if f is None:
            survivors.append(P)
print("sets checked:", total, "violations of the hand-derived conditions:", viol)
print("survivors (no failure for 3 <= m <= 400):", len(survivors))
# describe survivors after dividing out the power-of-two scale
prim = {}
for P in survivors:
    a, b, g, godd, e = stats(P)
    scale = 2**e
    Q = tuple(p // scale for p in P)
    prim.setdefault(Q, []).append(scale)
ratios = sorted({(max(Q) / min(Q)) for Q in prim})
print("primitive survivor shapes:", len(prim), " min ratio max/min among them:", ratios[0])
print("survivors with max < 2*min:", [Q for Q in prim if max(Q) < 2 * min(Q)])
print("survivors with max == 2*min:", [Q for Q in prim if max(Q) == 2 * min(Q)][:20])
two = sorted(Q for Q in prim if len(Q) == 2)
print("two-element primitive survivors:", two)
# non-survivors that are primitive with max > 2*min: where do they fail?
late = []
for r in range(2, 4):
    for P in itertools.combinations(range(1, N + 1), r):
        a, b, g, godd, e = stats(P)
        if g == 1 and b > 2 * a:
            f = first_fail(P)
            if f is not None:
                late.append((f, P))
late.sort()
print("primitive, max > 2*min, yet failing:", len(late), "latest failures:", late[-8:], "earliest:", late[:8])
