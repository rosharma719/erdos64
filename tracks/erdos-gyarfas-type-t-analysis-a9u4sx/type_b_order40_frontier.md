# The order-40 frontier: normalizing the two order-21 bridge geometries

**Status.** Hand-written structural derivation. No new computation is
reported in this file; it fixes the exact normalized data structures,
degree/edge bounds, and role tables that the order-21 generators (to be
built next) must satisfy. No proof-assistant formalization exists.

## 0. A genuine external-data limitation, reported honestly

Resolving the exact edge range for `|E(R)|` at order 21 needs an upper
bound from `ex(20;{C4,C8})`. `manifests/external_s6_manifest.json` lists
McKay's authoritative source
(`https://users.cecs.anu.edu.au/~bdm/data/extremal/c48_n20e31.s6`,
expected 94 graphs, expected SHA-256
`4b4e0670c63e365d3e26401e3ade4843ea7868077865234e7cadd61af21a9160`) but
its `local_status` is `MISSING` — this file has never actually been
downloaded or checksum-verified in this repository; the filename itself
encodes the claimed value `ex(20;{C4,C8})=31` under McKay's own naming
convention, but that is not the same as a verified certificate.

A fetch was attempted this session:

```text
curl -sS https://users.cecs.anu.edu.au/~bdm/data/extremal/c48_n20e31.s6
```

Result: the egress proxy returned a **403 policy denial**
(`gateway answered 403 to CONNECT (policy denial or upstream failure)`,
host `users.cecs.anu.edu.au:443`). Per this environment's explicit
protocol, a 403 is an organization policy denial and must not be retried
or routed around — it is reported here, not silently worked around.

**Consequence for this file's scope.** `ex(20;{C4,C8})=31` is treated
strictly as an **unverified hypothesis**, not a fact. Section 2 instead
derives a genuinely provable (if much looser) upper bound from the
classical Kővári–Sós–Turán/Reiman `C4`-free counting argument, which
needs no external data at all. Both the narrow hypothesis (29-31) and the
wide provable range (29-48) are tracked explicitly below; no theorem in
this file's successors may cite `ex(20;{C4,C8})=31` as certified without
either (a) successfully fetching and checksum-verifying the McKay file, or
(b) an independently reproduced extremal search on this repository's own
compute.

**A directly reusable, regenerable fact.** `z3_lifts.md`'s IV.B benchmark
table already measured (not merely estimated) **36,101 raw connected,
`C4`-free, cubic graphs on 20 vertices** via
`nauty-geng -c -f -d3 -D3 20`, in 88.21 seconds. This is exactly the
population needed for the all-cubic (`E=30`, every vertex at its
exactly-cubic value) degree-sequence sublayer derived below (Section 3),
and is cheap enough to regenerate and independently re-verify rather than
merely cite.

## 1. Normalized structure for each gap type

Let `B` be an order-21 bridge role, terminals `x,y`, gateway `a` (`x`'s
unique neighbour, `d_B(x)=1`), `R=B-x`, so `|V(R)|=20`.

### Gap-one role (`delta=1` or `epsilon=1`)

The longest required path in `B` has length 18 (`ell+delta=18` for `B1`,
or `m+epsilon=18` for `B2`), using 19 vertices of `B` including `x`.
Deleting `x` leaves a required `a`-`y` path of length 17, using 18
vertices of `R`. Since `|V(R)|=20`, exactly **2 vertices of `R` lie off
this path** — call them `z1,z2`.

```text
gap type:              1
path:                  p_0 p_1 ... p_17   (p_0=a, p_17=y; 18 vertices, 17 edges)
off-path vertices:     z1, z2             (2 vertices)
terminal roles:        a=p_0 (gateway, loses edge xa), y=p_17
forced path witnesses: S1 always contains "2" (forced edge a-y in B1's role,
                       independent of delta) OR the two theta suffixes of
                       B2's role (structural, independent of epsilon) --
                       whichever mechanism applies, per type_b_b19.md's
                       dependency table
```

*Proof this is exact, not assumed.* A simple path of length 17 has
exactly 18 vertices (17 edges connect 18 distinct vertices). `R` has
exactly `20-18=2` remaining vertices, by direct arithmetic on `|V(R)|=20`
— not an assumption.

### Gap-two role (`delta=2` or `epsilon=2`)

The longest required path in `B` has length 19, using 20 vertices of `B`
including `x`. Deleting `x` leaves a required `a`-`y` path of length 18,
using 19 vertices of `R`. Since `|V(R)|=20`, exactly **1 vertex of `R`
lies off this path** — call it `z`.

```text
gap type:              2
path:                  p_0 p_1 ... p_18   (p_0=a, p_18=y; 19 vertices, 18 edges)
off-path vertices:     z                  (1 vertex)
terminal roles:        a=p_0, y=p_18
forced path witnesses: same mechanisms as gap-one, generic across rho,s
                       (type_b_delta2_zero_slack.md Section 2)
```

*Proof.* A simple path of length 18 has 19 vertices; `R` has exactly
`20-19=1` remaining vertex, by direct arithmetic.

This is structurally identical in vertex-count logic to B20's original
one-slack derivation (`type_b_one_slack.md`) and to
`type_b_delta2_zero_slack.md`'s zero-slack derivation, one order higher
throughout: every "off-path count" here is exactly one more than the
corresponding order-20 case, because the bridge order increased by
exactly one while the required path length (hence its own vertex count)
stayed fixed.

## 2. Degree and edge bounds, both gap types

**Generic across both roles (no `rho,s` dependence), by the identical
mechanism established in `type_b_b19.md`'s dependency table and reused
throughout `type_b_one_slack_resolution.md`/`type_b_delta2_zero_slack.md`:**

- Every path-internal vertex and every off-path vertex is internal to
  `B`, unaffected by deleting `x`, hence has ambient degree `>=3` in `R`.
- `d_R(a)>=2` (loses only edge `xa`).
- `d_R(y)>=2` (forced edge from `S1`'s constant `2`, or the two-branch
  theta-suffix structure for the `B2` role — neither depends on `rho,s`).

**Gap-one count of "ordinary" (degree `>=3`) vertices:** 16 true
path-internal vertices (`p_1,...,p_16`) + 2 off-path (`z1,z2`) = **18**.

**Gap-two count:** 17 true path-internal vertices (`p_1,...,p_17`) + 1
off-path (`z`) = **18**.

**Both gap types give the same total of 18 "ordinary" vertices** (a
direct consequence of `|V(R)|=20` minus the 2 terminal-role vertices
`a,y`, independent of how the off-path/path-internal split occurs).
Hence, for both gap types:

\[
 2|E(R)| \ge 18\cdot3 + 2\cdot2 = 58, \qquad |E(R)| \ge 29.
\]

### Upper bound: hypothesis vs. provable fallback

- **Unverified hypothesis** (McKay filename convention, not fetched):
  `ex(20;{C4,C8})=31`, giving `|E(R)| in {29,30,31}`.
- **Provable fallback** (Kővári–Sós–Turán/Reiman, `C4`-free only, needs no
  external data): for a `C4`-free graph on `n` vertices,
  `m <= n(1+sqrt(4n-3))/4`. For `n=20`: `sqrt(77)~8.775`,
  `m <= 20*9.775/4 = 48.87`, so `|E(R)| <= 48`. This is far looser (it
  ignores `C8`-freeness entirely) but is unconditionally true without any
  external file.

This file adopts a **staged plan**: resolve the tight, most-likely-decisive
layers `E=29,30,31` first (matching the pattern of every prior phase,
where the true extremal-adjacent layers were the ones that actually
mattered), and only extend into the wider Reiman range `32..48` if a
survivor is found in `29..31` or if time/resources permit a full
uncontestable sweep. No claim of "no order-21 bridge exists" will be made
until either the full Reiman range is exhausted, or an authoritative,
checksum-verified `ex(20;{C4,C8})` certificate is obtained and used
instead.

## 3. Degree-sequence classification by edge count

Write the total excess `q = 2|E(R)| - 58 >= 0` (excess over the 18-vertex,
`>=3` / 2-vertex, `>=2` minimum). Each vertex's own excess over its lower
bound is a non-negative integer; these excesses sum to exactly `q`.

### `E=29` (`q=0`): unique degree sequence, both gap types

Every vertex sits exactly at its lower bound: `a=2, y=2`, all 18
"ordinary" vertices `=3`. Degree sequence `2^2,3^18`. This is the **only**
possible degree sequence at `E=29` — no branching, since `q=0` forces
every excess to be exactly `0`.

- **Gap-one, `E=29`:** `2^2,3^18` on 20 vertices, with the specific
  labeling: `a,y` at degree 2, all of `p_1,...,p_16,z1,z2` at degree 3.
  Non-path edges: path has 17 edges, so `29-17=12` non-path edges.
- **Gap-two, `E=29`:** `2^2,3^18` on 20 vertices, with `a,y` at degree 2,
  all of `p_1,...,p_17,z` at degree 3. Non-path edges: path has 18 edges,
  so `29-18=11` non-path edges.

### `E=30` (`q=2`): two sub-families, both gap types

Excess `2` distributed as either **one vertex `+2`** or **two vertices
`+1` each**, over 20 vertices with lower bounds `(2,2,3,3,...,3)`:

- **Sub-family A (one `+2`):** one vertex jumps by 2 from its lower
  bound. If it is `a` or `y`: degree `2->4`. If it is an "ordinary"
  vertex: degree `3->5`. Degree sequences: `2,4,3^18` (a or y at 4,
  17 ordinary at 3 — wait, only one of `a,y` jumps, so the sequence is
  `4,2,3^18`, i.e. one 4, one 2, eighteen 3s) or `2^2,3^17,5` (one
  ordinary vertex at 5, seventeen at 3, both terminals at 2).
- **Sub-family B (two `+1`):** two vertices each jump by 1. Cases:
  both `a,y` (giving `3^20` — **fully cubic**, the reusable population
  from Section 0); `a` (or `y`) plus one ordinary vertex (giving
  `3,2,3^17,4 = 2,3^18,4`, one terminal at 2, one ordinary bumped to 4,
  the other terminal stays at 3 — wait, only if the OTHER terminal is
  the one NOT bumped; recompute below); or two distinct ordinary vertices
  (giving `2^2,3^16,4^2`).

*Exact enumeration, not hand-waving:* label the 20 vertices' lower-bound
deviations `d_v=deg(v)-lb(v)>=0` with `sum d_v=2`. Partitions of `2` over
non-negative integers: `(2)` on one vertex, or `(1,1)` on two vertices.
This is a complete case list by definition of integer partitions — no
case is omitted.

| sub-case | which vertices gain | resulting degree sequence |
|---|---|---|
| A1 | `a` (or `y`, symmetric) gains 2 | `4,2,3^18` |
| A2 | one ordinary vertex gains 2 | `2^2,3^17,5` |
| B1 | `a` and `y` both gain 1 | `3^20` (fully cubic) |
| B2 | `a` (or `y`) and one ordinary vertex each gain 1 | `3,2,3^17,4` = `2,3^18,4` |
| B3 | two distinct ordinary vertices each gain 1 | `2^2,3^16,4^2` |

Five sub-cases at `E=30`, each further split by **where** the "ordinary"
role lands (path-internal vs. off-path, and which specific off-path
vertex for gap-one's `z1`/`z2`), giving the full `gap1_order21` and
`gap2_order21` role tables below.

### `E=31` and beyond: growing branching, deferred pending Section 0's plan

At `E=31`, `q=4`, with partitions `(4),(3,1),(2,2),(2,1,1),(1,1,1,1)` —
five integer partitions, each producing one or more degree-sequence
families depending on which vertices (terminal vs. ordinary) absorb the
excess. This file does not enumerate `E=31`'s cases in full here; it is
deferred to the generator-construction phase (next commit), where the
partition logic above is implemented directly in code (so the case count
is verified by exhaustive computation, not manual transcription) rather
than hand-listed for a larger partition count.

## 4. Exhaustive role tables

### `gap2_order21_roles` (19-vertex path `p_0..p_18`, 1 off-path vertex `z`)

| row | `|E(R)|` | degree sequence | non-path edges | degree-4/5 role location | depends on `rho,s`? |
|---|---:|---|---:|---|:---:|
| G2-29 | 29 | `2^2,3^18` | 11 | none (unique sequence) | no |
| G2-30-A1 | 30 | `4,2,3^18` | 12 | `a` or `y` (2 choices) | no |
| G2-30-A2 | 30 | `2^2,3^17,5` | 12 | one of `p_1..p_17,z` (18 choices) | no |
| G2-30-B1 | 30 | `3^20` | 12 | none (fully cubic; `a,y` no longer degree-2) | no |
| G2-30-B2 | 30 | `2,3^18,4` | 12 | one terminal at 2 (2 choices) x one of `p_1..p_17,z` at 4 (18 choices) | no |
| G2-30-B3 | 30 | `2^2,3^16,4^2` | 12 | two distinct of `p_1..p_17,z` at 4 (`C(18,2)=153` choices) | no |
| G2-31-* | 31 | (deferred, Section 3) | 13 | (deferred) | no |

### `gap1_order21_roles` (18-vertex path `p_0..p_17`, 2 off-path vertices `z1,z2`)

| row | `|E(R)|` | degree sequence | non-path edges | degree-4/5 role location | depends on `rho,s`? |
|---|---:|---|---:|---|:---:|
| G1-29 | 29 | `2^2,3^18` | 12 | none (unique sequence) | no |
| G1-30-A1 | 30 | `4,2,3^18` | 13 | `a` or `y` (2 choices) | no |
| G1-30-A2 | 30 | `2^2,3^17,5` | 13 | one of `p_1..p_16,z1,z2` (18 choices) | no |
| G1-30-B1 | 30 | `3^20` | 13 | none (fully cubic) | no |
| G1-30-B2 | 30 | `2,3^18,4` | 13 | one terminal at 2 (2 choices) x one of `p_1..p_16,z1,z2` at 4 (18 choices) | no |
| G1-30-B3 | 30 | `2^2,3^16,4^2` | 13 | two distinct of `p_1..p_16,z1,z2` at 4 (`C(18,2)=153` choices) | no |
| G1-31-* | 31 | (deferred, Section 3) | 14 | (deferred) | no |

Neither table depends on `rho` or `s` at any row: every ingredient used
(vertex counts, lower bounds, excess partitions) traces back only to the
generic Type-B degree profile and the length of the longest required
path (18 or 19), exactly as audited for B19/B20/B20D2.

**Non-path edge counts, checked:** gap-two path has 18 edges
(`29-18=11`, `30-18=12`, `31-18=13`); gap-one path has 17 edges
(`29-17=12`, `30-17=13`, `31-17=14`) — each row above matches.

## 5. What this file does and does not establish

- **Establishes:** the exact normalized vertex/path structure for both
  gap types at order 21 (Section 1, proved from vertex-count arithmetic,
  not assumed); the shared lower bound `|E(R)|>=29` (Section 2); the
  complete, exhaustive degree-sequence classification at `E=29,30`
  (Section 3-4, derived from integer-partition case analysis, not
  extrapolated from the order-20 tables).
- **Does not yet establish:** any elimination or survival of any role;
  the exact value of `ex(20;{C4,C8})` (explicitly flagged unverified,
  Section 0); the `E=31`+ degree-sequence case list (deferred to the
  generator phase).
- **Explicit external-data gap:** McKay's `c48_n20e31.s6` could not be
  fetched (403 policy denial, not retried). Any future claim that
  `ex(20;{C4,C8})=31` must either successfully verify that file's
  checksum or independently reproduce the bound computationally.
