#!/usr/bin/env python3
"""2-adic proof that the bare core's affine cycle-length forms are never
dyadic, for every j >= 4 -- not just the tested j=4,5,6.

``type_t_port_completion.md`` Section 1 reports the bare core's complete
simple-cycle spectrum for j=4,5,6 (61 cycles / up to 35 distinct lengths
each, checked across 9 (a,c) combinations per j with no spectrum change).
Each length is an affine function of Y=2^j (the core's kernel has fixed
topology across every valid (j,a,c); only some kernel edges have
j/a/c-dependent length -- see the completeness discussion in
type_t_port_core_dyadic_avoidance.md). Fitting from the j=5,6 data (whose
multiplicity sequences agree exactly in sorted order, so the pairing is
unambiguous) gives clean integer (A,B) coefficients that reproduce the
j=4 spectrum exactly, including its two accidental same-Y collisions.

Given those 35 (A,B) forms, whether A*2^j+B is ever a perfect power of two
for j>=4 has an exact, finite answer via 2-adic valuation (not floating
point, not a bounded numerical search): if B=0, dyadic iff A is a power of
two; otherwise let v=v2(B) -- for j>v, v2(A*2^j+B)=v exactly (strictly
smaller than v2(A*2^j)=j+v2(A)), so A*2^j+B can only possibly equal a power
of two (specifically 2^v, since valuation forces the power) for some j<=v,
a finite range. This module makes that check exact and reusable.

This is NOT a proof that the 35 forms are the *complete* list of bare-core
cycle lengths for every j (that is a separate, currently open, completeness
question -- see the markdown file above) -- only that, given they are
complete, none of them is ever dyadic.
"""

from __future__ import annotations

from fractions import Fraction


J4_SPECTRUM = "3:1, 6:2, 7:2, 9:3, 10:1, 12:1, 13:1, 14:1, 17:2, 18:2, 19:2, 22:1, 23:1, 24:1, 60:1, 61:1, 62:1, 65:2, 66:2, 67:2, 69:1, 70:2, 71:1, 72:4, 73:2, 74:2, 75:2, 77:6, 78:4, 79:1, 80:1, 82:3, 83:2"
J5_SPECTRUM = "3:1, 6:2, 7:2, 9:3, 10:1, 28:1, 29:1, 30:1, 33:2, 34:2, 35:2, 38:1, 39:1, 40:1, 124:1, 125:1, 126:1, 129:2, 130:2, 131:2, 134:1, 135:1, 136:1, 149:1, 150:1, 152:3, 153:2, 154:2, 155:2, 157:6, 158:4, 159:1, 160:1, 162:3, 163:2"
J6_SPECTRUM = "3:1, 6:2, 7:2, 9:3, 10:1, 60:1, 61:1, 62:1, 65:2, 66:2, 67:2, 70:1, 71:1, 72:1, 252:1, 253:1, 254:1, 257:2, 258:2, 259:2, 262:1, 263:1, 264:1, 309:1, 310:1, 312:3, 313:2, 314:2, 315:2, 317:6, 318:4, 319:1, 320:1, 322:3, 323:2"


def parse_spectrum(text: str) -> list[tuple[int, int]]:
    out = []
    for item in text.split(","):
        length, mult = item.strip().split(":")
        out.append((int(length), int(mult)))
    return out


def fit_affine_forms() -> list[tuple[int, int, int]]:
    """Returns (A, B, multiplicity) for each of the 35 forms, fit from the
    j=5,6 spectra and cross-checked exactly against j=4."""
    p4, p5, p6 = (parse_spectrum(s) for s in (J4_SPECTRUM, J5_SPECTRUM, J6_SPECTRUM))
    if len(p5) != len(p6) or [m for _, m in p5] != [m for _, m in p6]:
        raise AssertionError("j=5/j=6 multiplicity sequences must agree exactly for an unambiguous pairing")
    Y5, Y6, Y4 = 32, 64, 16
    forms = []
    for (l5, m5), (l6, m6) in zip(p5, p6):
        a = Fraction(l6 - l5, Y6 - Y5)
        b = l5 - a * Y5
        if a.denominator != 1 or b.denominator != 1:
            raise AssertionError(f"non-integer affine fit for {(l5, m5)}/{(l6, m6)}")
        forms.append((int(a), int(b), m5))

    from collections import Counter
    predicted4 = Counter()
    for a, b, m in forms:
        predicted4[a * Y4 + b] += m
    actual4 = Counter(dict(p4))
    if predicted4 != actual4:
        raise AssertionError(f"j=4 cross-check failed: predicted={predicted4} actual={actual4}")
    return forms


def v2(n: int) -> int:
    """2-adic valuation of a nonzero integer."""
    if n == 0:
        raise ValueError("valuation undefined at 0")
    n = abs(n)
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def never_dyadic_for_all_j(a: int, b: int, min_j: int = 4, extra_margin: int = 3) -> tuple[bool, list[tuple[int, int]]]:
    """Exact check: is a*2^j+b ever a power of two, for any j>=min_j?

    Returns (safe, offending_js) where offending_js lists any (j, value)
    pairs found to be dyadic within the provably sufficient finite range.
    """
    if a == 0:
        return (not is_power_of_two(b)), ([] if not is_power_of_two(b) else [(None, b)])
    if b == 0:
        # a*2^j is a power of two for EVERY j, or for NO j, depending only
        # on whether a itself is a power of two -- not a finite-range check.
        if is_power_of_two(a):
            return False, [("all j", a * 2**min_j)]
        return True, []
    v = v2(b)
    # For j > v, valuation of the sum is exactly v (strictly less than
    # v2(a*2^j) = j+v2(a)), so a dyadic hit can only occur at j <= v.
    # Checking through max(v, min_j+extra_margin) is a superset of that
    # provably-sufficient range, with margin for direct sanity.
    upper = max(v, min_j + extra_margin)
    offending = []
    for j in range(min_j, upper + 1):
        value = a * (2**j) + b
        if is_power_of_two(value):
            offending.append((j, value))
    return (len(offending) == 0), offending


def check_all_forms(min_j: int = 4) -> dict:
    forms = fit_affine_forms()
    results = []
    all_safe = True
    for a, b, m in forms:
        safe, offending = never_dyadic_for_all_j(a, b, min_j=min_j)
        if not safe:
            all_safe = False
        results.append({"A": a, "B": b, "multiplicity": m, "safe_for_all_j": safe, "offending": offending})
    return {"forms": results, "all_forms_safe_for_all_j": all_safe, "num_forms": len(forms)}


if __name__ == "__main__":
    import json

    print(json.dumps(check_all_forms(), indent=2))
