"""Derive the allowed-e intersection table for a given t, by the same method
used in the externally-supplied t=4 table's own documented derivation.
Validated by exactly reproducing the audited t=4 table before being trusted
to produce the (independently needed, source unavailable) t=3 table."""
FORBIDDEN = {4, 8, 16}

def allowed_e(L, tmax):
    out = []
    for e in range(0, tmax + 1):
        if e > L:
            continue
        lo, hi = L + e, L + 2 * e
        if any(f in range(lo, hi + 1) for f in FORBIDDEN):
            continue
        if L == 3 and e == 0:
            continue  # an unmarked quotient triangle is always an extra triangle
        out.append(e)
    return out

known_t4 = {
    3: [2], 4: [1], 5: [0,1,4], 6: [0,3,4], 7: [0,2,3,4], 8: [1,2,3],
    9: [0,1,2,3], 10: [0,1,2], 11: [0,1,2], 12: [0,1], 13: [0,1,4],
    14: [0,3,4], 15: [0,2,3,4], 16: [1,2,3,4],
}

if __name__ == "__main__":
    mismatches = sum(1 for L in range(3, 17) if allowed_e(L, 4) != known_t4[L])
    assert mismatches == 0, f"derivation method disagrees with audited t=4 table: {mismatches} mismatches"
    print("t=4 self-check: PASS (0 mismatches)")
    print("derived t=3 table:")
    for L in range(3, 17):
        print(f"  L={L}: {allowed_e(L, 3)}")
