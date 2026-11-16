import collections
F = {2**k for k in range(2, 30)}
def first_fail(P, adjacent, M):
    S = {0}; fail = None
    for m in range(1, M + 1):
        S = {s + p for s in S for p in P}
        if (m >= 3 or (m == 2 and not adjacent)) and not (S & F):
            return m
    return None
def longest_run(P):
    best = cur = 0; prev = None
    for p in sorted(P):
        cur = cur + 1 if prev is not None and p == prev + 1 else 1
        best = max(best, cur); prev = p
    return best
for n in range(8, 14):
    rows = [l.split() for l in open(f"pieces_{n}.txt")]
    allp = []; clean = []
    for _, mask, adjc, c8, g6 in rows:
        mask = int(mask); P = [i for i in range(64) if mask >> i & 1]
        rec = (P, int(adjc), int(c8), g6)
        allp.append(rec)
        if not int(c8): clean.append(rec)
    def summ(recs, tag):
        if not recs: print(f"n={n} {tag}: none"); return
        sizes = [len(P) for P, *_ in recs]
        runs = [longest_run(P) for P, *_ in recs]
        ratios = [max(P) / min(P) for P, *_ in recs]
        M = 40 // (n - 1)   # copies allowed if the whole graph had only 41 vertices
        fails = [first_fail(P, a, 60) for P, a, *_ in recs]
        forb41 = sum(1 for f in fails if f is not None and f * (n - 1) < 41)
        nofail = sum(1 for f in fails if f is None)
        sparse = min(recs, key=lambda r: (len(r[0]), r[0]))
        print(f"n={n} {tag}: {len(recs)} pieces; |P| min/max {min(sizes)}/{max(sizes)}; "
              f"shortest longest-run {min(runs)}; min ratio {min(ratios):.2f}; "
              f"never fail (m<=60): {nofail}; ruled out already at order 41: {forb41}; sparsest P={sparse[0]}")
    summ(allp, "all C4-free")
    summ(clean, "C4,C8-free")
