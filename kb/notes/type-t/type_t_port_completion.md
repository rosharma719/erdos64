# Type-T port completion

**Status (2026-07-28): COMPLETION — FIXED-INSTANCES CLOSED; PARAMETRIC
FAMILY OPEN.**  The weighted `E2_parallel` residual is now an ordinary graph,
its same-vertex completion problem is an exact perfect-matching problem, and
three representative `j=4` translations are certified UNSAT.  This is a real
completion result, but it is not yet an all-translation theorem: 321 of the
324 rooted `j=4` translations have compatibility screening only.

No degree-five geometry, longer local-route census, `Q` placement, or
added-vertex completion is used here.

## 1. Independent ordinary core

Put `Y=2^j`, `j>=4`.  The exporter in
`verifier/type_t_port_core_export.py` does not import the affine cycle
enumerator.  It creates a fresh internal vertex for every unit subdivision of

\[
 |A|=4Y-1,\quad |B|=4,\quad |C|=Y-1,\quad |D|=4,
\]

with common first edges `AC` and `BD`, attachment coordinates `a,a+7` on
`A`, attachment coordinates `c,c+7` on `C`, and the two literal port paths
`r_x-u_x-s_x` and `r_y-u_y-s_y`.

There are 13 suppressed vertices and 19 suppressed edges.  The sum of the
19 edge lengths is `5Y+13`; hence subdivision gives

\[
 n_0=13+(5Y+13)-19=5Y+7,\qquad m_0=5Y+13,
\]

and cycle rank `m_0-n_0+1=7`.  The exact degree distribution is

\[
 n_2=5Y-4,\qquad n_3=10,\qquad n_4=1.
\]

The unique degree-four vertex is `z0`.  Every degree-two vertex has deficit
one, including `u_x,u_y`; every other vertex is already saturated.  Thus a
same-vertex completion is exactly a perfect matching on the `5Y-4`
deficient vertices, avoiding core edges.  After adding it, `z0` remains
degree four and every other vertex has degree three.  The completed size and
rank would be

\[
 m=\frac{15Y+22}{2},\qquad \beta=\frac{5Y}{2}+5.
\]

| `j` | `Y` | core order | core size | deficits | matching edges | completed size | completed rank |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 16 | 87 | 93 | 76 | 38 | 131 | 45 |
| 5 | 32 | 167 | 173 | 156 | 78 | 251 | 85 |
| 6 | 64 | 327 | 333 | 316 | 158 | 491 | 165 |

The independent checker materialized 27 cores: all nine extreme/interior
cross-combinations for each `j=4,5,6`.  It checked simplicity,
connectivity, the four canonical branch lengths, both common prefixes, the
two exact port neighbourhoods, the degree vector, and every ordinary simple
cycle.  Every core has 61 cycles and no dyadic cycle.  For reference, the
complete spectra with multiplicity `length:count` are:

- `j=4`: `3:1, 6:2, 7:2, 9:3, 10:1, 12:1, 13:1, 14:1, 17:2,
  18:2, 19:2, 22:1, 23:1, 24:1, 60:1, 61:1, 62:1, 65:2, 66:2,
  67:2, 69:1, 70:2, 71:1, 72:4, 73:2, 74:2, 75:2, 77:6, 78:4,
  79:1, 80:1, 82:3, 83:2`.
- `j=5`: `3:1, 6:2, 7:2, 9:3, 10:1, 28:1, 29:1, 30:1, 33:2,
  34:2, 35:2, 38:1, 39:1, 40:1, 124:1, 125:1, 126:1, 129:2,
  130:2, 131:2, 134:1, 135:1, 136:1, 149:1, 150:1, 152:3,
  153:2, 154:2, 155:2, 157:6, 158:4, 159:1, 160:1, 162:3,
  163:2`.
- `j=6`: `3:1, 6:2, 7:2, 9:3, 10:1, 60:1, 61:1, 62:1, 65:2,
  66:2, 67:2, 70:1, 71:1, 72:1, 252:1, 253:1, 254:1, 257:2,
  258:2, 259:2, 262:1, 263:1, 264:1, 309:1, 310:1, 312:3,
  313:2, 314:2, 315:2, 317:6, 318:4, 319:1, 320:1, 322:3,
  323:2`.

The raw audit is
`data/type_t_port_completion/phase0_core_audit.json`.

## 2. Rooted translations and first-order compatibility

For `j=4`,

\[
 2\le a\le55,\qquad 2\le c\le7,
\]

so there are `54*6=324` parameter pairs.  There is no legitimate translation
quotient here.  In the rooted, path-coloured object, `z0,x,xprime,y,yprime`,
both prefix vertices, both ports, and the `A/B/C/D` colours are fixed.  The
pair

\[
 (a,c)=(|\text{prefix}_{AC}+A_{left}|,
        |\text{prefix}_{AC}+C_{left}|)
\]

is therefore an automorphism invariant.  All 324 pairs are distinct rooted
orbits.

Define the first-order compatibility graph `K(j,a,c)` on the deficient
vertices.  A pair is an edge exactly when it is not a core edge and the core
has no simple path between its endpoints of length `2^k-1`; otherwise adding
that single matching edge already closes a dyadic cycle.  Every one of the
324 `j=4` compatibility graphs has a perfect matching.  Their safe-edge
counts range from 656 to 843 and their minimum degrees range from 4 to 11.
Consequently the ordinary compatibility graph has no Tutte obstruction that
can eliminate the family.  The live obstruction is higher-order: two or
more individually safe matching edges can close a forbidden cycle together.

The complete per-orbit screen is
`data/type_t_port_completion/j4_rooted_orbit_screen.json`.

## 3. Exact matching formulation and fixed-instance UNSAT

For every safe pair `e`, introduce a Boolean variable `x_e`.  At every
deficient vertex impose exactly one incident selected edge.  Given a SAT
model, expand it with the core and search for `C4,C8,C16,C32,C64`.  If a
dyadic cycle uses selected matching edges `e_1,...,e_t`, add

\[
 \neg x_{e_1}\vee\cdots\vee\neg x_{e_t}.
\]

This is a sound lazy cut: every later matching containing those same edges
contains the same ordinary cycle.  The loop always rechecks from `C4`
upward.  An UNSAT result after finitely many cuts is therefore a complete
fixed-instance proof, even when cycle enumeration per individual model is
capped, because every admitted cut is independently valid.

| parameters | encoding | variables | base clauses | cycle cuts | models | shortest-cycle models `(4,8,16)` | result |
|---|---|---:|---:|---:|---:|---:|---|
| `(4,2,2)` | sequential counter | 2,033 | 3,990 | 105,429 | 2,585 | `(489,2035,61)` | UNSAT |
| `(4,2,2)` | pairwise | 703 | 13,922 | 104,079 | 2,600 | `(468,2071,61)` | UNSAT |
| `(4,28,4)` | sequential counter | 2,408 | 4,740 | 245,497 | 4,799 | `(667,3982,150)` | UNSAT |
| `(4,55,7)` | sequential counter | 1,892 | 3,708 | 43,493 | 1,414 | `(344,1045,25)` | UNSAT |

All four computations become UNSAT using only cycle cuts of lengths 4, 8,
and 16.  The `(4,2,2)` final CNF was then solved independently by CaDiCaL
1.9.5 and Lingeling; both returned UNSAT.  Glucose also emitted a DRAT trace.
An independently built `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` verified that trace against the
preserved final CNF in 11.497 seconds.  The checker reported a core of 12,473
input clauses, 55,809 proof lemmas, and 8,385,461 resolution steps.

Artifacts are in `data/type_t_port_completion/`, including the compressed
final CNF and DRAT trace.  These results close three translations, not all
324, so they do not yet eliminate the parametric family.

## 4. Near miss and independent verification

A seeded degree-preserving 2-switch heuristic finds a perfect matching for
`(j,a,c)=(4,2,2)` with no `C4` or `C8` after 959 steps.  Two independent
exact detectors agree that its dyadic spectrum is

\[
 C_{16},C_{32},C_{64}\text{ present};\qquad C_4,C_8\text{ absent}.
\]

The graph has order 87, size 131, minimum degree three, and its graph6 and
sparse6 encodings are stored with the matching.  Exhaustive radius-one
repair tests give:

- all 131 single-edge deletions invalidate minimum degree three and still
  leave a `C16`;
- among the 1,406 formal matching 2-switch reconnections, 68 try to add a
  core edge and are invalid;
- of the 1,338 valid degree-preserving switches, 187 first expose `C4`, 1,018
  first expose `C8`, and 133 first expose `C16`; none is power-cycle-free.

The matching, independent verification, and repair census are the three
`j4_a2_c2_c4_c8_near_miss*.json` files in the data directory.

## 5. Stopping point

The same-vertex completion problem is now explicit and executable, and
fixed-instance UNSAT is certified.  But the valid rooted orbit count is 324,
not one, and the compatibility graphs themselves remain matchable.  The next
completion task is therefore an all-orbit `j=4` higher-order obstruction or
an exhaustive all-orbit SAT run.  Only after that is sound should the search
move to `j=5` and then to completions with added vertices.

No completed power-cycle-free candidate exists here, so the requested `Q`
attachment has not been placed.  Degree five remains deferred.
