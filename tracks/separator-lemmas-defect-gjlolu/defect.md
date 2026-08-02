# defect.md — the ordering-defect parameter D (arbitrary-order redirection)

**Status as of 2026-07-25.** This file is new (redirection of the main project
toward structures that apply to arbitrary order, per the 2026-07-25 task).
Every claim is labeled per the project discipline in README.md. G always
denotes a minimal counterexample (δ≥3, no cycle of length in F={4,8,16,…},
minimizing (|V|,|E|) lexicographically) *if one exists* — none is known to
exist (the conjecture is OPEN), so results here are conditional statements
about G, exactly like B0–B4/M1–M4/S4/S5.

## 1. Elimination ordering and forward degree — setup [PROVED, elementary]

For a simple graph H on n vertices and an ordering x₁,…,xₙ of V(H), define the
**forward degree** d⁺(xᵢ) = |N(xᵢ) ∩ {x_{i+1},…,xₙ}| (neighbors that come
later in the order). Every edge has a unique "earlier" endpoint under any
total order, so **Σᵢ d⁺(xᵢ) = m** for *any* ordering of *any* simple graph.
Also **d⁺(xₙ) = 0** always (nothing comes after the last vertex), and
**d⁺(x_{n-1}) ≤ 1** always (at most one vertex, xₙ, comes after x_{n-1}) —
these last two facts hold for *every* graph and *every* ordering; they are
not special to G and impose no real constraint. This matters below: two of
the five terms in the task's "defect identity" are vacuous by construction,
so the identity's only real content is in the x₁ and middle terms.

## 2. Definition of D and the exact identity [PROVED, pure algebra]

For any simple graph H (n vertices, m edges), define
**D := 2n − 2 − m**.

**Claim.** For *any* ordering x₁,…,xₙ of *any* simple graph,
D = (3 − d⁺(x₁)) + Σ_{i=2}^{n-2} (2 − d⁺(xᵢ)) + (1 − d⁺(x_{n-1})).

*Proof.* RHS = [3 + 1 + 2(n−3)] − [d⁺(x₁) + Σ_{i=2}^{n-2} d⁺(xᵢ) + d⁺(x_{n-1})]
= (2n−2) − Σ_{i=1}^{n-1} d⁺(xᵢ) = (2n−2) − Σ_{i=1}^{n} d⁺(xᵢ) (since
d⁺(xₙ)=0) = (2n−2) − m = D. ∎

This is **pure arithmetic** — it holds for every ordering of every graph,
with no hypothesis on H at all (not even δ≥3). It does **not** by itself
show D ≥ 0, let alone D ≥ 2: the individual terms (3−d⁺(x₁)) etc. can be
negative for a "bad" ordering. What would make the terms a genuine
nonnegative "defect decomposition" is the *existence* of an ordering
realizing the caps d⁺(x₁)≤3, d⁺(xᵢ)≤2 (2≤i≤n−2), d⁺(x_{n-1})≤1 — and by
§1 the last cap is free, so only two things need proving:

**2a. [PROVED] x₁ can be chosen with d⁺(x₁) = 3 exactly.** Take x₁ to be any
degree-3 vertex of G — one exists by M1's corollary (B3). Since x₁ is first
in the order, *all* its neighbors are "later," so d⁺(x₁) = deg_G(x₁) = 3.

**2b. [OPEN — gap, not established here] Middle cap d⁺(xᵢ) ≤ 2 for
2≤i≤n−2.** Equivalently: does G − x₁ admit *some* ordering with all forward
degrees ≤ 2, i.e. **is G − x₁ 2-degenerate** (every subgraph of G−x₁ has a
vertex of degree ≤2, equivalently G−x₁ has no subgraph of minimum degree
≥3)? This is the "known result on graphs without a proper minimum-degree-3
subgraph" the redirection asks to invoke. I could not derive it here from
B0–B4/M1–M4/S4/S5:
- B3 says G itself has no *proper edge-subgraph* of min degree ≥3 (every
  edge has a degree-3 endpoint) — this is a fact about G, not about G−x₁,
  and does not imply G−x₁ is 2-degenerate (B3 does not prevent a min-degree-3
  chunk of G from surviving entirely inside G−x₁, far from x₁).
- The natural orientation argument (orient every edge toward a degree-3
  endpoint, using B3+B4) gives in-degree 0 at every degree-≥4 vertex and
  in-degree ≤3 at every degree-3 vertex, hence only **m ≤ 3n₃ ≤ 3n** — far
  too weak, and it is really just M3 restated, not a 2-degeneracy bound.
- I therefore do **not** assert m(G) ≤ 2n−4 or D ≥ 2 as proved. Both remain
  open pending either (i) a proof that G−x₁ is 2-degenerate (which, if true,
  gives only m ≤ 2n−2, i.e. D≥0 — see the arithmetic below, not yet D≥2),
  or (ii) an independent sharper argument. Flagging this explicitly rather
  than citing an unverified "known result," per the project's no-overclaim
  rule.

Arithmetic check on the gap: if G−x₁ *were* shown 2-degenerate, the standard
tight 2-degenerate edge bound (build from a triangle seed, each further
vertex adds ≤2 edges) gives m(G−x₁) ≤ 2(n−1)−3 = 2n−5, so
m(G) = 3 + m(G−x₁) ≤ 2n−2, i.e. **D ≥ 0** only — not yet D ≥ 2. Reaching
D ≥ 2 needs *either* a strictly sub-extremal 2-degeneracy bound (e.g. using
C4-freeness, B0, to rule out the triangle-heavy extremal 2-degenerate
graphs) *or* a different argument entirely. Left open.

## 3. What IS provable about D from existing lemmas [PROVED]

**3a. Σ_v (deg(v) − 3) = n − 4 − 2D.** *Proof.* Σ(deg(v)−3) = 2m − 3n (S1,
already proved). And n − 4 − 2D = n − 4 − 2(2n−2−m) = n−4−4n+4+2m = 2m−3n.
Same quantity — this is again pure algebra from the definition of D, no new
hypothesis. Matches the redirection's requested identity exactly. ∎

**3b. D ≤ ⌊n/2⌋ − 2.** *Proof.* By S1, m ≥ ⌈3n/2⌉ (δ≥3). So
D = 2n−2−m ≤ 2n−2−⌈3n/2⌉. For n even: ⌈3n/2⌉=3n/2, giving D ≤ n/2−2 =
⌊n/2⌋−2. For n odd: ⌈3n/2⌉=(3n+1)/2, giving D ≤ 2n−2−(3n+1)/2 =
(4n−4−3n−1)/2 = (n−5)/2; since D is an integer and (n−5)/2 = ⌊n/2⌋−2 exactly
when n is odd (⌊n/2⌋=(n−1)/2, so ⌊n/2⌋−2=(n−5)/2), equality of the bound
holds in both parities. So **D ≤ ⌊n/2⌋−2 in general**, with equality iff G
is regular (cubic, by M4) — the excess Σ(deg−3)=0 case. ∎ This reuses only
S1 (already in lemmas.md) — no gap.

**3c. D ≥ 2 remains OPEN**, tied to the §2b gap (an upper bound m ≤ 2n−4 is
exactly equivalent to D ≥ 2 by the definition of D). Not claimed here.

## 4. The central target, taken literally, is DISPROVED [DISPROVED — 2026-07-25]

The redirection's "central proof target": *every power-of-two-cycle-free
minimal graph satisfies n ≤ 2D+3*, with D := 2n−2−m as defined above. Taken
literally (exactly this D, exactly this inequality), this is **false for
every graph with δ≥3** — not just for a hypothetical counterexample G, for
*any* simple graph with minimum degree ≥3 whatsoever. No cycle-length
information is even needed to refute it; S1 alone suffices.

*Proof.* n ≤ 2D+3 ⟺ n ≤ 2(2n−2−m)+3 = 4n−2m−1 ⟺ 2m ≤ 3n−1 ⟺
**m ≤ (3n−1)/2**. But S1 gives m ≥ ⌈3n/2⌉, and ⌈3n/2⌉ ≥ 3n/2 > (3n−1)/2
strictly, for every n ≥ 1. So m > (3n−1)/2 always when δ≥3 — the required
inequality m ≤ (3n−1)/2 **never holds**. Hence n ≤ 2D+3 never holds for any
δ≥3 graph. ∎

**Worked example (cubic case, the extremal case of §3b).** If H is cubic
(m=3n/2, n even), D = 2n−2−3n/2 = n/2−2 = ⌊n/2⌋−2 (equality in 3b), and
2D+3 = n−1 < n = n — off by exactly 1, always. E.g. K₄ (n=4,m=6): D=0,
2D+3=3<4. The Petersen graph (n=10,m=15, cubic): D=3, 2D+3=9<10. This is
not a special pathology of small or specific graphs — §4's proof shows the
gap n−(2D+3) = 2m−3n+1 = (excess)+1 ≥ 1 always, by S1's excess≥0.

**Consequence for the redirection.** Because a cubic δ≥3 graph is not
excluded by any lemma proved so far (M4 only says *if* G is regular it is
cubic; no lemma rules out a cubic minimal counterexample outright — the
Royle–Markström cubic search, L11, only rules it out below n=30, leaving
n≥30 fully open), a literal reading of "n≤2D+3 for every minimal graph"
is inconsistent with what is currently known/open about G's regularity.
**Methodological conclusion:** D as a pure edge-count quantity (a function
of (n,m) alone) cannot by itself bound n — the excess/defect identity in
§3a shows D is just an affine reparametrization of the excess 2m−3n, so any
inequality of the form n ≤ αD+β is *equivalent to* a pure edge-count bound
m ≤ (2n−β)/α, which is either already implied by S1 (if weak) or
contradicted by S1 (if it demands a stronger *lower* bound on excess than
δ≥3 gives, as here). **A correct bound bridging D and n must use the
cycle-length-avoidance structure, not the (n,m) pair alone.** This sharpens
the redirection's own instruction ("search aggressively for
counterexamples") into a precise diagnosis of *why* the naive form fails,
and points Part 3/4's vine/two-tree machinery at the right target: D must
be coupled to the missing-dyadic-length count, not substituted for it.

**Open question for a corrected statement.** The most natural repair
compatible with 3a/3b is to conjecture a bound of the shape
*n ≤ f(D) for some f growing faster than 2D+3* (since D≤⌊n/2⌋−2 already
forces n ≥ 2D+4 in the cubic-extremal case — matching the disproof above
exactly, n = 2D+4 there, one more than the false target) **or** to restrict
the target to non-extremal excess (e.g. state it only for graphs with
excess ≥ 1, which the disproof's gap formula (excess+1) shows would need
excess ≥ 1 exactly to reach n ≤ 2D+4, still not 2D+3). Neither repair is
attempted as a theorem here; both are flagged as the next concrete target,
labeled CONJECTURAL, and require the cycle-spectrum argument (§5/vine
experiment) rather than pure counting.

## 5. Small-D empirical data [COMPUTATIONALLY VERIFIED — see experiments.md E7]

`verifier/defect_model.py` computes (n,m,D,excess) and the full cycle-length
spectrum for real small graphs (connected, δ≥3, generated by `geng`) and
checks both (i) the proved bound D≤⌊n/2⌋−2 and (ii) the disproof in §4. See
experiments.md E7 for the full run log.

**Result: both proved facts hold with 0 exceptions** across 2,762 generic
connected δ≥3 graphs (n=4..8) and 98,066 C4-free connected δ≥3 graphs
(n=10..15) — exactly as guaranteed by the unconditional proofs in §3b/§4
(this is a consistency check on the algebra, not new information).

**The §2b gap is real, not just a missing proof — it computationally
FAILS on a nontrivial fraction of C4-free δ≥3 graphs.** For every graph
tested, and every choice of degree-3 vertex x₁, `defect_model.py` checked
whether G−x₁ is 2-degenerate:

| n range | C4-free δ≥3 graphs | every deg-3 x₁ works | some but not all | **no x₁ works** |
|---|---|---|---|---|
| 10–13 | 574 | 375 | 160 | 39 (6.8%) |
| 14–15 | 97,492 | 33,428 | 48,430 | 15,632 (16.0%) |

The "no x₁ works" fraction is growing with n, not shrinking. **This directly
refutes the naive hope that §2b can be proved by "pick any degree-3 vertex
as x₁"** — smallest concrete witness at n=12: g6 `K?`DA_wdeQKc`, D=1, every
one of its 6 degree-3 vertices leaves a non-2-degenerate remainder. If §2b
(hence m≤2n−4, D≥2) is true at all for genuine minimal counterexamples, the
proof must use F-cycle-freeness beyond C4-freeness (C8, C16, … avoidance)
and/or a cleverer/adaptive choice of x₁ than "arbitrary," not a
universal fact about C4-free δ≥3 graphs. Recorded as an honest negative
result, per the project's discipline of keeping failed approaches with
their exact obstruction.

## 6. Vine construction and cycle spectrum [see experiments.md E8, DISPROVED]

A **vine graph** V(n; chords) realizes the target forward-degree pattern
literally: forward path x₁–x₂–…–xₙ, x₁ additionally joined to 2 further
later vertices (chords), each internal xᵢ (2≤i≤n−2) additionally joined to
at most 1 further later vertex (a "vine" chord) so that its forward degree
is ≤2 (1 path edge + ≤1 chord), and x_{n-1} joined only to xₙ. The natural
charging conjecture to test:

**V1 (candidate lemma).** *"A graph with D defects has at most D missing
dyadic cycle lengths among {4,8,…,≤n}."*

**First (uninformative) test — `verifier/vine_experiment.py`.** Randomized
vine construction (path + minimal/near-minimal chord sets) at n=9..21,
D=0..8: **116/116 instances satisfy V1**, but this is a false positive —
random chord placement makes these graphs cycle-*rich* (missing-count is 0
or 1 in every single instance regardless of D, see experiments.md E8), so
the test never actually stresses the inequality. Recorded as a
methodology note: naive random vine sampling cannot find V1's failure mode,
because avoiding dyadic cycles is an adversarial property random
construction essentially never produces (this is itself informative — it
is a small piece of evidence for *why* Erdős–Gyárfás is hard: "generic"
sparse graphs already satisfy it easily).

**Second test (the real one) — reusing E7's C4-free data.** Every C4-free
graph has length 4 in its missing set by definition (B0 applies to any
C4-free graph, counterexample or not), so num_missing ≥ 1 always among
C4-free graphs — meanwhile D=0 is achievable (D≤⌊n/2⌋−2 only upper-bounds
D; nothing lower-bounds it above the trivial D matching S1's equality
case). **V1 is DISPROVED**, both in general (the argument just given) and
concretely: smallest witness found by `defect_model.py --c4free`, n=13,
g6 `L?AB?vOLDPHa\`o`, D=0, missing={4} (num_missing=1 > D=0). 629/98,066
C4-free graphs (n=10–15) violate V1 outright (experiments.md E7/E8).
**Status: DISPROVED**, recorded per the redirection's explicit instruction
to keep a disproved lemma with its exact obstruction rather than discard
it — see lemmas.md V1 entry.
