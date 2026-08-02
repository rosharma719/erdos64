# contraction_mixed_witness.md — mixed power/near-power path systems at a Type N vertex

**Standing reminder, per project discipline.** Every proof below is a
hand-written Markdown argument, cross-checked computationally wherever
the claim is unconditional. Nothing here is proof-assistant formal
verification. Builds on `contraction_atoms.md` (nontriangle-edge
witnesses `P_x`, the two functional-digraph orientation types, the
five-lemma toolkit) and `contraction_neighborhood.md` (the
closed-neighbourhood witness `Q_{pq}`, `|Q_{pq}|=2^s`).

## Two more arithmetic lemmas

**Lemma E (theta third branch, `-1` variant) [PROVED, new].** *For
`x,y\ge2`, `2^x+2^y-1` is never a power of two.* *Proof, mod 4.*
`x,y\ge2\Rightarrow2^x\equiv2^y\equiv0\pmod4`, so `2^x+2^y-1\equiv3
\pmod4`. Powers of two are `\equiv1\pmod4` (`2^0`), `\equiv2\pmod4`
(`2^1`), or `\equiv0\pmod4` (`2^m`, `m\ge2`) — never `\equiv3`. ∎

**Lemma F (`2^s+2` is always safe) [PROVED, new].** *For `s\ge2`,
`2^s+2` is never a power of two.* *Proof, mod 4.* `2^s\equiv0\pmod4`
(`s\ge2`), so `2^s+2\equiv2\pmod4`, matching only `2^1=2` — but
`2^s+2\ge6>2`. ∎

*(Both brute-force confirmed over `x,y\in\{2,\dots,9\}` by
`verifier/mixed_witness.py`'s `check_arithmetic_extensions`, together
with the two further identities used below: `2^x+2^y+1` never a power
of two, `x,y\ge2`, by the same odd-parity argument as
`contraction_atoms.md` VI.1a; `2^x+2^y+2^z-2` never a power of two,
`x,y,z\ge2`, mod-4 argument analogous to Lemma D3.)*

## Part III: the combined endpoint system at a Type N vertex

At a Type N vertex `v`, `N(v)=\{a,b,c\}`, the nontriangle-edge lemma
gives `P_x:x\to f(x)`, `|P_x|=2^{r_x}-1`, for a loopless function `f`
(two orientation types, `contraction_atoms.md` V.0). The
closed-neighbourhood lemma (CN1) additionally gives an **unordered**
pair `\{p,q\}\subseteq\{a,b,c\}` and a path `Q_{pq}:p\to q`,
`|Q_{pq}|=2^s`.

### III.1. Orbits of the combined system `(f,\{p,q\})`, derived rigorously [PROVED]

**Orientation 1 (directed 3-cycle), `f=(a\,b\,c)`.** `\mathrm{Stab}(f)`
under the relabelling action of `S_3` is exactly the cyclic group
`\langle f\rangle` of order 3 (a reflection sends a 3-cycle to its
inverse, a *different* labelled 3-cycle, so no reflection stabilizes a
fixed `f`). No nontrivial element of this order-3 group fixes any of the
3 unordered pairs `\{a,b\},\{b,c\},\{c,a\}` (each nontrivial rotation
permutes all three pairs cyclically), so the **combined** stabilizer of
`(f,\{a,b\})` inside the full `S_3` is trivial, giving one orbit of size
`6/1=6` — covering all `2\times3=6` labelled instances of this
orientation (both 3-cycles, all 3 pairs each; the orbit necessarily
mixes in `f`'s inverse, since elements of `S_3` outside `\mathrm{Stab}(f)`
send `f` to the other 3-cycle). **Exactly one combined orbit.**
Representative: `f=(a\,b\,c)`, `\{p,q\}=\{a,b\}`.

**Orientation 2 (2-cycle + feeder).** The 6 labelled functions of this
type form a single `S_3`-orbit (`contraction_atoms.md` V.0), so
`|\mathrm{Stab}(f)|=6/6=1` — **trivial stabilizer**, for every such `f`.
The diagonal action of `S_3` on the 18 pairs `(f,\{p,q\})` (6 functions
`\times` 3 pairs each) therefore has trivial stabilizers everywhere
(a subgroup of the trivial `\mathrm{Stab}(f)`), i.e. it is **free**:
exactly `18/6=3` orbits. Fixing `f(a)=b,f(b)=a,f(c)=a` (2-cycle
`\{a,b\}`, feeder `c\to a`) as one representative function, direct
tracking of the transposition `(a\,b)` (which sends this `f` to the
*different* labelled function `f'` with `f'(c)=b`, while mapping pairs
`\{a,b\}\to\{a,b\}`, `\{a,c\}\to\{b,c\}`, `\{b,c\}\to\{a,c\}`) shows the
3 pair-choices are **pairwise inequivalent as relative positions** —
"the 2-cycle pair itself," "feeder-with-its-target," and
"feeder-with-the-other-cycle-element" are three genuinely distinct
combined orbits, not further reducible. **Exactly three combined
orbits**, representatives (fixing `f(a)=b,f(b)=a,f(c)=a`):
- **T2a:** `\{p,q\}=\{a,b\}` (the 2-cycle pair).
- **T2b:** `\{p,q\}=\{a,c\}` (feeder `c` with its target `a=f(c)`).
- **T2c:** `\{p,q\}=\{b,c\}` (feeder `c` with the non-target cycle
  element `b`).

**Total: exactly four combined endpoint orbits — T1, T2a, T2b, T2c —
derived from stabilizer/orbit-counting, not from inspecting all
`8\times3=24` labelled instances directly** (matching the requirement
not to rely on labelled enumeration alone). Each orbit has size exactly
`6` (`24/4`), consistent with every combined stabilizer being trivial —
orientation 1's included, once the full `S_3` action (not merely
`\mathrm{Stab}(f)`) is used, exactly as derived above.

**Computational cross-check.** `check_combined_orbits` enumerates all
24 labelled `(f,\{p,q\})` pairs, partitions them under the diagonal
`S_3` action, and confirms exactly 4 orbits, each of size 6.

### III.2. Joint canonical witness choice [definitional, extends `contraction_atoms.md` V.1]

Among all available `(P_a,P_b,P_c,Q_{pq})` tuples (finite, `G` finite),
fix the one minimizing, in order: (1) the largest exponent among
`\{r_a,r_b,r_c,s\}`; (2) the sum of all four exponents; (3) total
pairwise common-edge count across all six pairs of the four witnesses;
(4) total number of common-path components across all six pairs; (5) a
fixed lexicographic tie-break. A unique minimizer exists (finite set,
total order).

**What this licenses, precisely.** Criteria (1)–(2) fix an *exponent
profile* first, before any overlap consideration; criteria (3)–(4) then
select, *among all witness realizations of that exact profile*, the one
with least overlap. Consequently: **if some realization of the chosen
profile achieves a fully clean (pairwise internally-disjoint) system,
the canonical choice achieves it too** (or something at least as
clean) — so a "clean case" analysis below is never vacuously about an
artificially poor choice. Conversely, **if every realization of a given
profile forces some nonzero overlap, the canonical choice exhibits that
same forced overlap** — a "non-clean" finding at the canonical witness
is then a genuine structural fact about `G` at that profile, not an
artifact of choosing badly. This is the exact sense in which later
"assume clean" steps are licensed by minimal overlap *relative to a
fixed exponent profile*, not relative to some other comparison class.

## Part IV: near-power theta systems (NPT)

For an endpoint orbit where `\{p,q\}=\{x,f(x)\}` for some `x`
(T1, T2a, T2b — checked case by case below), `Q_{pq}` and `P_x` share
the *same two endpoints*. Together with the length-2 path `x{-}v{-}f(x)`
(always available, `v\sim x` and `v\sim f(x)` both hold), assuming all
three are pairwise internally disjoint (a genuine theta graph
`\Theta(x,f(x))`), the three branch lengths are
\[
2,\qquad 2^r-1\ (r:=r_x),\qquad 2^s,
\]
and the three pairwise-combined cycles have lengths
\[
\boxed{2^r+1},\qquad\boxed{2^s+2},\qquad\boxed{2^r+2^s-1}.
\]

**None of these three is ever a power of two, for any `r,s\ge2`
whatsoever [PROVED, unconditional].**
- `2^r+1`: odd for `r\ge1`, and `\ge5>1` — never a power of two.
- `2^s+2`: Lemma F.
- `2^r+2^s-1`: Lemma E.

**This is stronger than "not automatically forbidden": the clean NPT
theta is arithmetically safe for *every* exponent combination, with no
equality ever excluded and none ever required** — call this configuration
`\mathrm{NPT}(r,s)`, per the task's naming, and record explicitly: *it
supplies no arithmetic leverage toward a contradiction by itself.* This
is the first canonical obstruction the task anticipated, now made
precise and unconditional rather than merely "not obviously forbidden."

### IV.1. Case-by-case classification of all four orbits [PROVED]

**T1** (`\{p,q\}=\{a,b\}`, `f(a)=b`). Matches `P_a` uniquely (`\{b,f(b)\}
=\{b,c\}\ne\{a,b\}`, `\{c,f(c)\}=\{c,a\}\ne\{a,b\}`). `\mathrm{NPT}(r_a,s)`
applies; all three lengths unconditionally safe (above). The
*pre-existing* pairwise constraints among `P_a,P_b,P_c` themselves
(`contraction_atoms.md` V.2: `r_a\ne r_b\ne r_c\ne r_a` in their own
clean case) are untouched by this theta and continue to apply
independently — the theta neither strengthens nor weakens them.

**T2a** (`\{p,q\}=\{a,b\}`, the 2-cycle pair). Matches **both** `P_a`
(`\{a,f(a)\}=\{a,b\}`) and `P_b` (`\{b,f(b)\}=\{b,a\}`) — a genuine
4-branch fan between `a,b`: the `v`-path (length 2), `P_a`
(`2^{r_a}-1`), `P_b` (`2^{r_b}-1`), `Q_{ab}` (`2^s`). If all four are
pairwise internally disjoint, all `\binom42=6` pairwise cycles are
realized; **every one is unconditionally safe:**
\[
2^{r_a}+1,\ \ 2^{r_b}+1,\ \ 2^s+2\quad(\text{single-branch-vs-}v),
\]
\[
2^{r_a}+2^{r_b}-2\ \ (\text{Lemma A}'),\qquad
2^{r_a}+2^s-1,\ \ 2^{r_b}+2^s-1\ \ (\text{Lemma E}).
\]
**Complete resolution: the fully clean 4-branch fan at T2a adds no
leverage whatsoever — all six combinations, exhaustively enumerated,
are safe for every exponent choice.**

**T2b** (`\{p,q\}=\{a,c\}`, feeder+target). Matches `P_c` uniquely
(`\{c,f(c)\}=\{c,a\}`). `\mathrm{NPT}(r_c,s)` applies, same
unconditional safety as T1.

**T2c** (`\{p,q\}=\{b,c\}`, feeder+non-target). **No `P_x` shares these
endpoints** (`\{a,b\},\{b,a\},\{c,a\}` — none equals `\{b,c\}`): *no
direct NPT theta is available here.* **The clean three-terminal network
instead, via Lemma C (vertex-hub merge) [PROVED].** `Q_{bc}` shares one
endpoint with each `P_x` (`b` with `P_a,P_b`; `c` with `P_c`); hub `v`
is adjacent to all of `a,b,c`, so each pairing closes via `v`:
\[
v\text{-}a\text{-}P_a\text{-}b\text{-}Q_{bc}\text{-}c\text{-}v:\ \ 2^{r_a}+2^s+1,
\]
\[
v\text{-}a\text{-}[P_b\text{ rev}]\text{-}b\text{-}Q_{bc}\text{-}c\text{-}v:\ \ 2^{r_b}+2^s+1,
\]
\[
v\text{-}b\text{-}Q_{bc}\text{-}c\text{-}P_c\text{-}a\text{-}v:\ \ 2^s+2^{r_c}+1.
\]
Each is a sum of two even terms (`r,s\ge2`) plus 1 — **odd, `\ge9`,
never a power of two**, unconditionally safe (same "always safe by
Lemma A+1" pattern first found in `contraction_atoms.md` VI.1a for
Type T). **A fourth combination, the closed triangle `P_a,Q_{bc},P_c`
(avoiding `v` entirely, if pairwise disjoint),** has length
`(2^{r_a}-1)+2^s+(2^{r_c}-1)=2^{r_a}+2^{r_c}+2^s-2` — safe by the new
`2^x+2^y+2^z-2` identity (mod-4 argument, magnitude check rules out the
one compatible residue class). **Complete resolution: T2c's natural
combinations are also all unconditionally safe.**

**Summary table.**

| orbit | mechanism | branch lengths | cycle lengths | status |
|---|---|---|---|---|
| T1 | NPT theta (`P_a,Q_{ab},v`\text{-path}) | `2,2^{r_a}-1,2^s` | `2^{r_a}+1,2^s+2,2^{r_a}+2^s-1` | all unconditionally safe |
| T2a | 4-branch fan (`P_a,P_b,Q_{ab},v`\text{-path}) | `2,2^{r_a}-1,2^{r_b}-1,2^s` | all 6 pairwise sums | all unconditionally safe |
| T2b | NPT theta (`P_c,Q_{ac},v`\text{-path}) | `2,2^{r_c}-1,2^s` | `2^{r_c}+1,2^s+2,2^{r_c}+2^s-1` | all unconditionally safe |
| T2c | vertex-hub merges + closed triangle | various, no theta | 4 combinations listed above | all unconditionally safe |

**No exponent equality is ever forced impossible by any of these
combinations — every `(r_x,s)` pair, equal or not, remains arithmetically
viable.** This is the honest, complete answer IV.1 asked for: not "safe"
asserted in the abstract, but every reachable combination enumerated and
resolved exactly, with the conclusion that **the clean local system by
itself (theta or three-terminal network) never produces a contradiction
at a Type N vertex, regardless of exponents** — motivating Part VI's
shift to *saturating* these safe structures with the additional
incidences `G`'s minimum degree forces at their internal vertices.

**Computational cross-check.** `verifier/mixed_witness.py`'s
`check_npt_theta_arithmetic` brute-forces Lemma E/F and the two further
identities over `r,s\in\{2,\dots,9\}` (0 violations); `check_orbit_gadgets`
builds explicit graph gadgets realizing each of T1/T2a/T2b/T2c's clean
configuration for small `(r,s)` and confirms every predicted cycle length
against direct construction with both cycle checkers.
