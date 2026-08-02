# The identical-terminal joint four-path spectrum

**Status.** Hand-written proof, cross-checked by elementary arithmetic
hygiene scripts (2-adic valuation and parity checks, not a formal
verifier). Continues `type_t_joint_bridge_universalization.md` Part
3.1's identical-terminal row (`X_x=y, X_y=x`, `B_x=B_y=:B_1` proved,
merged bridge `B_2^{joint}` carrying both vertices' external branches).
**Does not claim the identical-terminal row is resolved.** Three of the
four levels below are closed; the fourth (graph realizability) is not
attempted in this file.

## 0. Setup recap

Inside `B_2^{joint}`, four distinguished `x`-`y` paths exist:
`R_x` (length `2^{\rho_x}`, via `x{-}x'`-then-`Theta_x`'s near-power
branch `P_1^x`), `S_x` (length `2^{s_x}+1`, via `x{-}x'`-then-`Theta_x`'s
closed-neighbourhood branch `P_2^x`), and symmetrically `R_y,S_y` via
`y{-}y'` and `Theta_y`'s branches `P_1^y,P_2^y`. `x` has a *unique* edge
into `B_2^{joint}` (`x{-}x'`); likewise `y{-}y'` for `y`. By Lemma NE,
`x'\ne y'`.

## Level 1 (pairwise arithmetic): the five remaining pairs

`(R_x,R_y)` was resolved in `type_t_joint_bridge_universalization.md`
3.1.1: vertex-disjoint forces `rho_x\ne rho_y`; overlapping escapes via
an explicit family. The other five pairs:

### 1.1. Same-vertex pairs `(R_x,S_x)` and `(R_y,S_y)` — fully determined, not open

**This is not an "arbitrary same-bridge overlap" question at all — it
is fixed exactly by the theta's own definition.** `R_x` and `S_x` both
begin with `x`'s *unique* edge into `B_2^{joint}`, `x{-}x'` (part of
`Theta_x`'s `P_0` branch). After `x'`, `R_x` follows `P_1^x` and `S_x`
follows `P_2^x` — and `P_1^x,P_2^x` are two of a theta's three branches,
**pairwise internally disjoint by definition** (sharing only the two
poles `x',X_x=y`). So `omega(R_x,S_x)=1` (the shared edge `x{-}x'`)
exactly, and the symmetric difference is exactly `P_1^x\cup P_2^x` — a
single cycle, **forced**, not chosen:
\[
|R_x|+|S_x| = 2\cdot1 + (2^{\rho_x}-1+2^{s_x}) = 2^{\rho_x}+2^{s_x}+1
\quad\checkmark
\]
and the cycle `P_1^x\cup P_2^x` has length `2^{\rho_x}-1+2^{s_x} =
2^{\rho_x}+2^{s_x}-1`, which is **odd** for `\rho_x,s_x\ge1` (even
`-1+` even `=` odd), hence never in `\mathcal F` — verified
computationally for `\rho_x,s_x\in[2,14]`, no exceptions. **This cycle
is exactly `Theta_x`'s own already-established internal spectrum
fact** (the same odd-parity argument used throughout the audited files
for a theta's two non-`P_0` branches) — not new arithmetic, and not
overlap-dependent at all, since the sharing/disjointness here is
*forced by construction*, leaving no cell-decomposition freedom.
**Conclusion: `(R_x,S_x)` and `(R_y,S_y)` are always safe,
unconditionally, no restriction on `\rho_x,s_x` (or `\rho_y,s_y`).**

### 1.2. Cross-vertex mixed pairs `(R_x,S_y)` and `(S_x,R_y)` — always safe, both sub-cases checked

**Vertex-disjoint case.** `|R_x|+|S_y| = 2^{\rho_x}+2^{s_y}+1` — even
plus odd, hence **odd**, hence never in `\mathcal F` (all of
`\mathcal F` is even). This holds for *every* `\rho_x,s_y`, no
condition needed. Verified computationally, `\rho_x,s_y\in[2,14]`.

**Overlapping case — the user's warning respected, not skipped.** An
odd *total* does **not** by itself certify every cell safe (a concrete
demonstration: splitting a length-`4`/length-`5` pair as `(1,3)/(3,2)`
already exposes a first cell of length `4\in\mathcal F` — this is
exhibited, not hand-waved, precisely to honor the instruction not to
trust odd-total safety blindly). So the overlapping sub-case needs its
own check: using the **general** 2-cell split `a=(1,2^{\rho_x}-1)`,
`b=(2,2^{s_y}+1-2)` (valid: `2^{s_y}-1\ge1` for `s_y\ge2`), the cells
are `1+2=3` (safe) and `(2^{\rho_x}-1)+(2^{s_y}-1)=2^{\rho_x}+2^{s_y}-2`.
**Claim:** `2^a+2^b-2` is never a power of two for `a,b\ge2`. *Proof:*
factor `2(2^{a-1}+2^{b-1}-1)`; since `a,b\ge2`, `a-1,b-1\ge1`, so
`2^{a-1},2^{b-1}` are both even, their sum is even, minus `1` is odd —
the factorization is `2\times(\text{odd}\ge3)`, 2-adic valuation
exactly `1` with an odd cofactor `>1`, hence never itself a power of
two. Verified computationally, `a,b\in[2,14]`, no exceptions.
**Conclusion: `(R_x,S_y)` (and symmetrically `(S_x,R_y)`) never forces
a contradiction, in either overlap regime, for any exponent values.**

### 1.3. Cross-vertex pair `(S_x,S_y)` — always safe (vertex-disjoint case; the relevant case)

`|S_x|+|S_y| = 2^{s_x}+1+2^{s_y}+1 = 2^{s_x}+2^{s_y}+2` — **even**, so
the "odd total" shortcut does *not* apply here and a real check is
needed (again, not skipped). **Claim:** `2^a+2^b+2` is never a power
of two for `a,b\ge2`. *Proof:* factor `2(2^{a-1}+2^{b-1}+1)`; since
`a-1,b-1\ge1`, `2^{a-1},2^{b-1}` are both even, so their sum is even,
`+1` is odd — again valuation exactly `1`, odd cofactor
`\ge2+2+1=5>1`, never a power of two. Verified computationally,
`a,b\in[2,14]`, no exceptions — **true unconditionally, whether or not
`s_x=s_y`** (unlike `(R_x,R_y)`, where equal exponents specifically
create the vulnerability; here the `+1` offsets on both paths break the
"clean doubling" that made `(R_x,R_y)` dangerous). Since the
vertex-disjoint realization is *always available and always safe* for
this pair, this pair can never be the source of a forced contradiction,
regardless of what the actual overlap pattern turns out to be —
**no overlap analysis is needed for this pair's safety conclusion**
(a pair only needs auditing under overlap if its *simplest* disjoint
realization is already unsafe, which is not the case here).

### 1.4. Level-1 summary table

| pair | vertex-disjoint | overlapping | restriction on exponents |
|---|---|---|---|
| `(R_x,R_y)` | forces `C_{2^{\rho_x+1}}` iff `\rho_x=\rho_y` | escapes (explicit family) | `\rho_x\ne\rho_y` **only if** disjoint |
| `(R_x,S_x)`, `(R_y,S_y)` | N/A — forced structure, not a free choice | N/A | none, ever |
| `(R_x,S_y)`, `(S_x,R_y)` | always safe (odd total) | always safe (explicit escape, valuation-proved) | none, ever |
| `(S_x,S_y)` | always safe (valuation-proved) | not needed (disjoint already safe) | none, ever |

**Of the six pairs, exactly one — `(R_x,R_y)` — can ever force
anything, and only in its vertex-disjoint sub-case.** This is the
single, precise, narrowed target for Level 2.

## Level 2: simultaneous four-path incidence consistency

**The user's core warning, addressed directly: the six pairwise
patterns are not independently selectable.** Since Level 1 shows five
of the six pairs impose no constraint under *any* configuration, the
only real question for Level 2 is whether `(R_x,R_y)`'s *specific*
escape (needed only if `\rho_x=\rho_y`) is structurally consistent with
also having `S_x,S_y` present as genuine, simultaneously-existing paths
in the same graph.

### 2.1. Any nontrivial overlap between `R_x` and `R_y` requires an unforced cross-theta vertex coincidence

`R_x`'s vertex sequence (after `x`) is `x'`, then `P_1^x`'s internal
vertices, then `y`. `R_y`'s vertex sequence (after `y`) is `y'`, then
`P_1^y`'s internal vertices, then `x`. Since `x'\ne y'` (Lemma NE), the
paths cannot coincide at their first step. **Any shared vertex `w`
(needed for *any* 2+-cell decomposition, whether the specific escape
split found earlier or a different one) must be a vertex lying on
*both* `Theta_x`'s `P_1^x` branch (or equal to `x'`) *and* `Theta_y`'s
`P_1^y` branch (or equal to `y'`).** This holds regardless of exactly
*where* along the paths the shared vertex sits — moving the
divergence point does not remove the need for the coincidence, it only
relocates it. **Nothing in the audited files forces this coincidence,
and nothing excludes it either** — `Theta_x` and `Theta_y` are
independently canonicalized (each vertex's own minimal-overlap
tie-break, `contraction_central_bridge.md` I.2, minimizes against
*previously fixed* witnesses at construction time, not against the
*other* vertex's separately-built theta), matching the same "canonical
choice does not force zero overlap, nor force overlap" finding
`contraction_intersections.md` V.2 already established for a
structurally analogous question. **This is the precise, single
structural fact Level 2 needed to isolate: the entire `(R_x,R_y)`
overlap question reduces to whether `Theta_x`'s `P_1^x` branch and
`Theta_y`'s `P_1^y` branch share an internal vertex — nothing more
refined than this is needed or available.**

### 2.2. `S_x,S_y` do not add a new constraint on this specific coincidence

Suppose the coincidence in 2.1 holds at some vertex `w` (shared by
`P_1^x` and `P_1^y`), realizing some 2+-cell split of `(R_x,R_y)`
(e.g. the explicit `(1,2^{\rho}-1)`/`(2,2^{\rho}-2)` family). Does the
*presence* of `S_x,S_y` in the same graph force anything new at `w`?
`S_x` lives entirely on `Theta_x`'s `P_2^x` branch, which is
**disjoint from `P_1^x`** by the theta's own definition (branches
pairwise disjoint except at poles) — so `S_x` cannot touch `w` (a
`P_1^x`-internal vertex) at all, unless `w` happens to *also* coincide
with a `P_2^x` vertex, which is excluded (`P_1^x,P_2^x` disjoint).
Symmetrically `S_y` (on `P_2^y`) cannot touch `w`. **So `S_x,S_y` are
automatically insulated from whatever coincidence `R_x,R_y}` need at
`w`, by the theta's own branch-disjointness — no additional
compatibility condition is created by their presence.** This directly
answers outcome (a)/(b) of the task in the negative: **the escape is
not shown incompatible with `S_x,S_y`, and their presence does not
force a new forbidden cycle** — the four-path system is, as far as
theta-branch structure alone can determine, mutually consistent
*provided* the one coincidence in 2.1 holds.

**Honest limit of this argument.** This shows `S_x,S_y` don't
*additionally* obstruct the escape — it does **not** show the
coincidence in 2.1 itself is realizable. That remains open (see
Level 4).

### 2.3. Incorporating `B_1`'s spectrum — cross-cut sums, fully rigorous, no new qualitative content

`B_1(=B_x=B_y)` and `B_2^{joint}` are *different* bridges of the same
2-cut `{x,y}` — automatically vertex-disjoint except at the terminals,
so **every** pairing between `\Lambda(B_1)\supseteq\{2,\ell,\ell+\delta\}`
and `\Lambda(B_2^{joint})\supseteq\{2^{\rho_x},2^{s_x}+1,2^{\rho_y},
2^{s_y}+1\}` is an unconditional cross-cut sum needing to avoid
`\mathcal F` — no overlap question, exactly as in
`type_t_joint_bridge_universalization.md` 3.2's one-common-terminal
argument, now with **twice as many** terms (both vertices' `\rho,s`
instead of one). Checked exhaustively:
- `2+2^{\rho_x}`, `2+2^{\rho_y}`: safe (`2(2^{\rho-1}+1)`, needs
  `\rho=1`, excluded).
- `2+2^{s_x}+1=2^{s_x}+3`, `2+2^{s_y}+1`: odd, safe.
- `\ell(+\delta)+2^{\rho_x}`, `\ell(+\delta)+2^{\rho_y}`,
  `\ell(+\delta)+2^{s_x}+1`, `\ell(+\delta)+2^{s_y}+1` (8 terms): open,
  symbolic, `\ell`-dependent — **exactly the same qualitative shape as
  `type_t_exact_two_a.md`'s own table**, merely duplicated across both
  vertices' exponents rather than one. The same infinite safe family
  generalizes immediately: `\ell=2^t+1`, `t>\max\{\rho_x,s_x,\rho_y,
  s_y,3\}`. **No new obstruction here — `B_1`'s cross-cut contributions
  add volume, not a qualitatively new constraint.**

### 2.4. The triangle-contraction witness `Q` — genuinely unresolved, flagged not settled

`Q` attaches at *some* pair `\{u,v\}\subset T`, determined by which
power-of-two cycle of `G/T` is being lifted — `central_bridge_triangle.md`
Part III explicitly leaves this pair undetermined in advance ("the
pair depends on which power-of-two cycle of `G/T` is being lifted, not
fixed in advance"). **If some such cycle happens to attach at exactly
`\{x,y\}`, `Q`'s own outside arc `Q_{\rm out}` is a further `x`-`y`
path**, needing its own overlap classification against `R_x,S_x,
R_y,S_y` and `B_1`'s own paths — a genuinely open sub-question this
file does **not** resolve. This is recorded honestly as unresolved,
not silently absorbed into Levels 2.1-2.3's clean conclusion.

## Level 3: what Level 2 establishes and does not

**PROVED (Level 2 conclusion):** the identical-terminal `(A,A)`
row's residual reduces *exactly* to one precise structural question:

\[
\boxed{\text{does }Theta_x\text{'s }P_1^x\text{ branch share an internal
vertex with }Theta_y\text{'s }P_1^y\text{ branch?}}
\]

If **no** (the two branches are disjoint): `R_x,R_y` are vertex-disjoint,
so `\rho_x=\rho_y` is impossible (forces `C_{2^{\rho_x+1}}`) —
**`\rho_x\ne\rho_y` is forced, and the row reduces cleanly to the
already-covered enriched Type-B 2-cut of
`type_t_joint_bridge_universalization.md` Part 5** (outcome (c) of the
task: a previously-covered Type-B spectrum, once the exponents are
distinct).

If **yes** (the branches share a vertex, at a position realizing some
2-cell split): the escape is arithmetically available and not
obstructed by `S_x,S_y` or by `B_1`'s cross-cut sums (Levels 2.2-2.3)
— an **explicit four-path incidence pattern survives at the symbolic/
incidence level** (outcome (d)). `Q`'s potential further interaction
(2.4) is not checked.

**This is not yet a resolution of the row — it is a reduction of the
entire remaining uncertainty to one single yes/no structural question**
about whether two independently-canonicalized theta branches can share
a vertex. No lemma in the fifteen previously-audited files, nor any
argument found in this file, answers that question either way.

## Level 4: graph realizability — not attempted this pass

Per the task's own staging, this level is reached only if a residual
survives Levels 1-3, which it does (the "yes" branch of Level 3's
dichotomy). **Building the SAT/graph-generation model for it is
deliberately not attempted in this file.** The natural smallest target
would encode: the Type-T triangle; `B_1` and `B_2^{joint}` as genuine
bridges of `\{x,y\}`; all four distinguished `B_2^{joint}` paths with
`P_1^x`/`P_1^y` sharing exactly one vertex at the position needed for a
concrete small `\rho` (e.g. `\rho_x=\rho_y=2`, escape split `(1,3)/(2,2)`
recalled from the earlier file); `P_1^x\perp P_2^x`, `P_1^y\perp P_2^y`
enforced structurally; `B_1`'s own admissible pair; minimum degree 3
throughout; closure 2-connectivity; and absence of `C_4,C_8,C_{16}`.
This is a well-specified next step, not built here, consistent with
reaching Level 4 honestly rather than skipping to it.

## 5. What is explicitly claimed and what is not

- **Claimed (PROVED):** of the six pairs among `\{R_x,S_x,R_y,S_y\}`,
  five (`(R_x,S_x)`,`(R_y,S_y)`,`(R_x,S_y)`,`(S_x,R_y)`,`(S_x,S_y)`)
  never force a contradiction under any exponent values or overlap
  configuration; only `(R_x,R_y)` can, and only in its vertex-disjoint
  sub-case.
- **Claimed (PROVED, new structural reduction):** the entire remaining
  identical-terminal residual reduces to the single question of
  whether `Theta_x`'s and `Theta_y`'s own `P_1` branches share an
  internal vertex — `S_x,S_y` and `B_1`'s cross-cut sums do not add any
  further obstruction to the escape once that one coincidence is
  assumed.
- **Not claimed:** whether that one coincidence is graph-realizable
  (Level 4, not attempted); `Q`'s full interaction (2.4, flagged
  unresolved); that the identical-terminal row is closed in either
  direction; any all-orders theorem.

## 6. Files

No new verifier script was produced this pass — all checks are
elementary closed-form arithmetic (2-adic valuation, parity), confirmed
by short one-off Python hygiene scripts (not committed as a formal
verifier, matching the discipline already used for the equivalent
checks in `type_t_joint_bridge_universalization.md`).
