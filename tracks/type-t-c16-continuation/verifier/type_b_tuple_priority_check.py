#!/usr/bin/env python3
"""Reproduces the tuple priority audit table in type_b_tuple_priority_audit.md.
Pure arithmetic, no graph generation: recomputes each tuple's forced spectra
and original/current bounds directly from the frozen definition in
type_b_realizability.md Section 1-3, and applies the B19/B20 chain to
whichever bridge role has longest-required-length exactly 18 (delta=1 or
epsilon=1), per the dependency audit in type_b_b19.md (which never
references rho or s)."""

TUPLES = [
    (1,2,2,4,4,1,1),(2,2,3,4,4,1,1),(3,3,2,4,4,1,1),(4,3,3,4,4,1,1),
    (5,2,2,4,4,1,2),(6,2,2,4,4,2,1),(7,2,2,4,4,2,2),(8,2,3,4,4,1,2),
    (9,2,3,4,4,2,1),(10,3,2,4,4,1,2),(11,3,2,4,4,2,1),(12,2,3,4,4,2,2),
    (13,3,2,4,4,2,2),(14,3,3,4,4,1,2),(15,3,3,4,4,2,1),(16,3,3,4,4,2,2),
]

EXPECTED_ORIG = {
    1:(19,19,36),2:(19,19,36),3:(19,19,36),4:(19,19,36),
    5:(19,20,37),6:(20,19,37),7:(20,20,38),8:(19,20,37),
    9:(20,19,37),10:(19,20,37),11:(20,19,37),12:(20,20,38),
    13:(20,20,38),14:(19,20,37),15:(20,19,37),16:(20,20,38),
}

def main():
    rows = []
    for rank, rho, s, t, u, delta, eps in TUPLES:
        ell = 2**t + 1
        m = 2**u + 1
        s1 = sorted({2, ell, ell + delta})
        s2 = sorted({2**rho, 2**s + 1, m, m + eps})
        n1_orig = ell + delta + 1
        n2_orig = max(m + eps + 1, 2**rho + 2**s)
        nG_orig = n1_orig + n2_orig - 2
        assert (n1_orig, n2_orig, nG_orig) == EXPECTED_ORIG[rank], (rank, n1_orig, n2_orig, nG_orig)

        b1_touched = (delta == 1)
        b2_touched = (eps == 1)
        n1_new = 21 if b1_touched else n1_orig
        n2_new = 21 if b2_touched else n2_orig
        nG_new = n1_new + n2_new - 2

        rows.append({
            "rank": rank, "rho": rho, "s": s, "t": t, "u": u,
            "delta": delta, "epsilon": eps,
            "S1": s1, "S2": s2,
            "orig": [n1_orig, n2_orig, nG_orig],
            "b1_touched": b1_touched, "b2_touched": b2_touched,
            "new": [n1_new, n2_new, nG_new],
        })

    min_new_bound = min(r["new"][2] for r in rows)
    strict_minimum_ranks = [r["rank"] for r in rows if r["new"][2] == min_new_bound]

    print(f"{'rank':>4} {'orig_nG':>8} {'new_nG':>7}")
    for r in rows:
        print(f"{r['rank']:>4} {r['orig'][2]:>8} {r['new'][2]:>7}")
    print()
    print("strict minimum new_nG across all orig<=40 tuples:", min_new_bound)
    print("achieved by ranks:", strict_minimum_ranks)
    assert min_new_bound == 38
    assert strict_minimum_ranks == [7, 12, 13, 16]
    print("CONFIRMED: Pi0 (rank 1, new bound 40) is not the minimum; ranks 7,12,13,16 (bound 38) are.")

if __name__ == "__main__":
    main()
