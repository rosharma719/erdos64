# Order-32 3-connectivity: gap analysis

**Status of this file.** Scoping/triage report. It contains (a) an inventory
of what this repository actually proves about 2-connectivity, 2-cuts, and
terminal-path signatures, with exact citations; (b) three short new
corollaries that follow from already-proved statements by citation only, each
labelled with the project's usual discipline; (c) a list of the specific
missing lemmas between here and the proposed order-32 target; and (d) an
audit of the proposed argument's external premise. **No attempt is made here
to prove the order-32 theorem.** Nothing here is proof-assistant formalized.
No new computation was run for this file.

Standing conventions are lemmas.md's: `G` is a lexicographically minimal
Erdős–Gyárfás counterexample (minimizing `(|V|,|E|)` among graphs with
`δ≥3` and no cycle of length in `F={4,8,16,32,…}`), `n=|V(G)|`,
`m=|E(G)|`.

---

## Part 1 — What is already proved

### 1.1 Connectivity of `G` itself

| Label | Statement | Status | Location |
|---|---|---|---|
| B1 | `G` is connected | `PROVED_IN_MARKDOWN` | lemmas.md §B1 |
| B2 | `G` is 2-connected | **NOT PROVED**; the textbook degree-2-suppression reduction is recorded as unsafe (it shifts cycle lengths by `ℓ−1`) | lemmas.md §B2 |
| S4 | `G` has no bridge | `PROVED_IN_MARKDOWN`, `NOVELTY_SUPPORTED_BY_SEARCH` | lemmas.md §S4; literature.md L16/L17 |
| S5 | If `v` is a cut vertex of `G`: `G−v` has exactly 2 components; `deg_G(v)=4` with exactly 2 neighbours in each; the two lobes have equal order `(n+1)/2` (**so `n` is odd**) and equal edge count; and `G` has **at most one** cut vertex | `PROVED_IN_MARKDOWN` | lemmas.md §S5, Steps 1–6 and "Corollaries recorded for reuse" |
| S6 | `G` is 3-connected | **CONJECTURAL**, the top-level target | two_cut.md §Goal; s6_case_tree.md §1 |
| §26 | `q(G)=2·d(A₁)` for the S5 cut-vertex case, hence `q(G)` is even whenever `G` has a cut vertex; therefore `q(G)=1 ⇒ G` is 2-connected | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED` (500 synthetic configs) | two_cut.md §26 |

So the *only* surviving obstruction to 2-connectivity is S5's single
configuration: one degree-4 cut vertex with two equal-order, equal-size lobes,
`n` odd. s6_case_tree.md §1 lists this as branch **C0** with "FIRST UNPROVED:
exclude or safely replace one lobe."

### 1.2 The 2-cut framework (all of two_cut.md is under the standing
hypothesis "`G` is 2-connected")

| Label | Statement | Status | Location |
|---|---|---|---|
| §1 | `aᵢ=deg_{Bᵢ}(x) ≥ 1` and `bᵢ ≥ 1` for every nontrivial bridge; every internal vertex of `Bᵢ` keeps its full `G`-degree, so `deg_{Bᵢ}(z)=deg_G(z)≥3` | `PROVED` | two_cut.md §1 |
| **T1** | `Bᵢ+xy` is 2-connected for every nontrivial bridge | `PROVED_IN_MARKDOWN` (likely folklore) | two_cut.md §1 |
| **T2** | `Λᵢ` (lengths of simple `x`–`y` paths in `Bᵢ`) contains two values differing by 1 or 2 | `PROVED_IN_MARKDOWN` from Gao–Huo–Liu–Ma (IMRN 2022, arXiv:1904.08126), `KNOWN_FROM_LITERATURE` ingredient | two_cut.md §1; one_pole.md O4′ |
| §2 | Every cycle crossing the cut splits into exactly 2 arcs in 2 different bridges, so `(Λᵢ+Λⱼ)∩F=∅` for `i≠j`; each `Bᵢ` is internally `F`-clean by inheritance | `PROVED` | two_cut.md §2 |
| §2 (Mersenne corollary) | **If `xy∈E(G)` then `Λᵢ ∩ {2^k−1 : k≥2} = ∅`** for every nontrivial bridge | `PROVED` | two_cut.md §2 |
| **T4** | No proper sub-selection of the bridges (plus the `xy` edge if present) has degree `≥3` at both terminals; consequences `aₖ≥deg_G(x)−2` or `bₖ≥deg_G(y)−2`, and `xy∈E(G) ⇒ deg_G(x)=3` or `deg_G(y)=3` | `PROVED_IN_MARKDOWN` (order- and edge-minimality) | two_cut.md §2b |
| §2c | `t≥4` impossible; **every 2-cut has exactly 2 or 3 nontrivial bridges**, giving exactly Types A/B/C | `PROVED_IN_MARKDOWN` | two_cut.md §2c |
| §3 | `qᵢ=max(⌈3/aᵢ⌉,⌈3/bᵢ⌉)∈{2,3}` (`qᵢ=1` excluded by order-minimality) | `PROVED` | two_cut.md §3 |
| **T3** | If `(qᵢcᵢ+2, qᵢeᵢ) <_lex (n,m)` then `(Λᵢ+Λᵢ)∩F ≠ ∅`; ties and losses are explicitly non-informative | `PROVED_IN_MARKDOWN` | two_cut.md §3 |
| **T5** | Type A: if `(cᵢ,eᵢ) <_lex (cₖ,eₖ)` then `(Λᵢ+Λᵢ)∩F≠∅`; so a self-sum-clean bridge is lex-maximal, and if all three are clean the three signatures coincide. Type B version identical with the retained `xy` edge. **No Type-C version is proved.** | `PROVED_IN_MARKDOWN`, `IMPLEMENTATION_FIXED` | two_cut.md §4b |
| **T6** | Unconditional construction: any two-terminal `B` with `q(B)∈{2,3}`, internal degree `≥3`, no power-of-two cycle, `B+xy` 2-connected, `(Λ(B)+Λ(B))∩F=∅`, and `xy∉E(B)`, glued in `q(B)` copies, is a genuine counterexample | `PROVED_IN_MARKDOWN` | two_cut.md §9 |
| **T7** | (overlap reduction toward eliminating dyadic self-sums) | `CONJECTURAL`, gated on finding one internally clean bridge — none exists through order 9 | two_cut.md §14, §19 |
| T8 / T8R / T8P, R1/R1b, R2 | Minimal Type-A gadget edge-criticality; real R- and P-skeleton edge deletion; incidence rules | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED` | two_cut.md §16, §17, §21 |
| T9B | Whole-pair Type-B replacement criticality: no smaller internally clean closure with spectrum contained in `Λᵢ` can replace either bridge | `PROVED_IN_MARKDOWN` | two_cut.md §27; type_b_compatibility.md |
| §26 | Separator-defect formulas: `q(G)=Σd(Bᵢ)−4` (Type A), `−3` (Type B), `−2` (Type C) | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED` | two_cut.md §26 |

### 1.3 The exact Type A/B/C classification (two_cut.md §2c)

- **Type A:** `t=3`, `xy∉E(G)`, `a₁=a₂=a₃=1`, `deg_G(x)=3`, `q₁=q₂=q₃=3`,
  `n=c₁+c₂+c₃+2`, `m=e₁+e₂+e₃`.
- **Type B:** `t=2`, `xy∈E(G)`, `a₁=a₂=1`, `deg_G(x)=3`, `q₁=q₂=3`,
  `n=c₁+c₂+2`, `m=e₁+e₂+1`. The edge `xy` belongs to neither nontrivial
  bridge (two_cut.md §3; type_b_compatibility.md §1).
- **Type C:** `t=2`, `xy∉E(G)`, `a₁+a₂≥3`, `b₁+b₂≥3`, **no bridge has both
  terminal degrees `≥3`** (i.e. `min(aᵢ,bᵢ)≤2`), `qᵢ∈{2,3}`, `n=c₁+c₂+2`,
  `m=e₁+e₂`.

### 1.4 Terminal-path / admissible-path signatures actually established

For every nontrivial bridge of a 2-cut of a 2-connected `G`:

1. `Λᵢ` contains two lengths differing by 1 or 2 (**T2**).
2. `(Λᵢ+Λⱼ)∩F=∅` for `i≠j` (§2).
3. `Λᵢ ∩ {2^k−1} = ∅` whenever `xy∈E(G)` (§2 trivial-bridge corollary) —
   i.e. Type-B terminal-path lengths **avoid** `{3,7,15,31,…}`.
4. `Bᵢ` is internally `F`-clean, in particular `C4`-free and `C8`-free.
5. `(Λᵢ+Λᵢ)∩F ≠ ∅` whenever T3's or T5's lex comparison strictly fires.
6. Exact route/offset templates for theta-anchored configurations
   (contraction_leaf_blocks.md VI.1–VI.2, central_bridge_templates.md), and
   the `{3,7,15}` excluded family for a paired-`K4` union at offset 2
   (contraction_separator_integration.md VII.1).

### 1.5 The finite two-terminal ("F-series") propositions — the repo's real
finite input to the 2-cut program

**F9 / F11** (two_cut.md §20, `COMPUTATIONALLY_VERIFIED`). *Every simple
two-terminal graph `B` with `|V(B)| ≤ 11` satisfying*

- `d_B(x)=1` and `d_B(y)≥1`;
- `xy ∉ E(B)`;
- `d_B(v)≥3` for every `v∉{x,y}`;
- `B+xy` simple and 2-connected

*contains a `C4` or a `C8`.*

Certificates: orders `<5` impossible from the degree conditions; orders 5–8
from the complete E22 closure population (5,212 rooted instances); order 9
from the checksummed E23 artifact (129,040 rooted oriented classes, all
containing an internal `C4` or `C8`); order 10 from the direct E24b search
(`m=13,14` layers, no degree-1 root survives); order 11 from all 245
`ex(11;{C4,C8})=15` extremal graphs and 26,950 ordered terminal choices.
two_cut.md §20 draws only the identical-three-copy T6 consequence:
`|V(G_B)| = 3(12−2)+2 ≥ 32`, explicitly disclaiming any bound for arbitrary
counterexamples or for three nonisomorphic bridges.

**There is no F-series proposition for any other terminal profile.** Nothing
covers `d_B(x)=2`, which is exactly the Type-C `min(aᵢ,bᵢ)=2` case.

### 1.6 Small-order elimination actually established in this repo

| Result | Range | Status | Location |
|---|---|---|---|
| E1 exhaustive `δ≥3` census | `n ≤ 11` (5,203,110 at `n=10`; 577,076,528 at `n=11`) | `COMPUTATIONALLY_REPRODUCED`; `n=12` partial | verification_status.md; experiments.md E1 |
| **P4 / L15: every `δ≥3` graph on `n ≤ 19` contains a `C4` or a `C8`** (strictly stronger than E–G in that range) | `n ≤ 19` | `PROVED_FROM_PUBLIC_EXTREMAL_DATA` + `COMPUTATIONALLY_VERIFIED`; `NOVELTY_UNCHECKED` | proof.md §P4; literature.md L15 |
| L15b: `n=20..23` extremal (top) edge layer cleared; **4 one-below near-cubic cases remain open** (`20/30` cubic, `22/33` cubic, `21/32` `4,3²⁰`, `23/35` `4,3²²`) | `n=20..23` | `INCOMPLETE_RANGE` | literature.md L15b; proof.md §P4; plan.md P1 |
| Hard stop at `n=24` | — | Markström's 24-vertex cubic `{C4,C8}`-free graph exists (literature.md L13/L15), so the "4-or-8" method **cannot** be pushed past 23 | literature.md L15 |
| IV.B order-26 feasibility | — | `INFEASIBLE`: raw `n=22` `C4`-free cubic generation did not finish in 400 s; `n=26` extrapolates to ~6 days for generation alone | verification_status.md |

**Nothing in this repository establishes anything about `δ≥3` graphs of order
24 through 31.**

### 1.7 Edge connectivity

The repo contains **exactly one** edge-connectivity result: **S4**
(bridgelessness = 1-edge-connectivity beyond trivial). There is no lemma
anywhere about 2-edge-cuts or 3-edge-cuts, no cyclic edge-connectivity
definition, and no cubic-specific edge-cut reduction. (Grep over all 62
markdown files: the only "2-edge"/"3-edge" hits are unrelated — arc lengths
in defect.md and port routes in the Type-T files.)

---

## Part 2 — What the existing machinery already delivers at order 32

The following three corollaries are new *statements*, but each is a
citation-only consequence of already-proved results. They are recorded here
because they were not drawn anywhere in the repo, and they change the shape of
the order-32 question substantially.

### Corollary O32-1 [PROVED IN WORKSPACE — immediate from S5]

*If `n` is even, then `G` has no cut vertex; combined with B1 and `n≥3`,
`G` is 2-connected. In particular **every order-32 minimal counterexample is
2-connected**.*

*Proof.* S5 claim 3 (lemmas.md §S5, Step 4) states that if `G` has a cut
vertex then both lobes have order exactly `(n+1)/2`, so `n−1` is even and `n`
is odd. Contrapositive: `n` even ⇒ no cut vertex. `G` is connected (B1), so a
connected graph on `≥3` vertices with no cut vertex is 2-connected. ∎

*Remark on scope.* This does **not** need the proposed external premise, does
not need any new computation, and is not an "order-32" fact at all — it holds
at every even order. It disposes of branch **C0** of s6_case_tree.md §1
(the S5 residual, listed there as a FIRST UNPROVED) for the order-32 target
specifically. It also means two_cut.md's standing hypothesis ("`G` assumed
2-connected") is *discharged*, not assumed, at order 32.

### Corollary O32-2 [PROVED IN WORKSPACE, modulo the `COMPUTATIONALLY_VERIFIED`
status of F11 — immediate from F11 + T1 + §1 + §2c]

*Every nontrivial bridge of a **Type-A** 2-cut of a minimal counterexample has
order `≥12` (i.e. `cᵢ≥10`). Consequently a Type-A 2-cut forces `n ≥ 32`, and
at `n=32` exactly, `c₁=c₂=c₃=10` and all three bridges have order exactly 12.*

*Proof.* Let `{x,y}` be a Type-A 2-cut and `Bᵢ` a nontrivial bridge. By §2c,
`aᵢ=d_{Bᵢ}(x)=1` and `xy∉E(G)`, hence `xy∉E(Bᵢ)`; by §1, `bᵢ=d_{Bᵢ}(y)≥1`
and every internal vertex has `d_{Bᵢ}(v)=deg_G(v)≥3`; by T1, `Bᵢ+xy` is
2-connected, and it is simple because `xy∉E(Bᵢ)`. These are exactly F11's
hypotheses. So if `|V(Bᵢ)|≤11` then `Bᵢ` contains a `C4` or a `C8`. But
`Bᵢ⊆G` and `4,8∈F`, contradicting `F`-cleanness of `G`. Hence
`|V(Bᵢ)|≥12`, i.e. `cᵢ≥10`. Since `n=c₁+c₂+c₃+2` (two_cut.md §4b),
`n≥30+2=32`, with equality forcing every `cᵢ=10`. ∎

*Why this is not already in the repo.* two_cut.md §20 derives the number 32
only for the **identical-three-copy T6 gadget** and explicitly disclaims the
general case: "This is **not** a lower bound for arbitrary Erdős–Gyárfás
counterexamples, does not exclude every three-bridge 2-cut, and does not treat
constructions using three nonisomorphic bridges." That disclaimer is correct
about the T6 route (which needs identical copies to compute `Λ+Λ`), but F11 is
a *standalone* proposition about arbitrary two-terminal graphs, so applying it
bridge-by-bridge needs no identity between the bridges at all. The coincidence
that both routes land on 32 is not an accident: both are `3·10+2`, driven by
the same F11 order floor.

**Sharpening at `n=32` (all by citation).** With `|V(Bᵢ)|=12` and `cᵢ=10`:

- **Edge box.** Degree sum in `Bᵢ` is `≥ 1 + bᵢ + 3·10`, so
  `eᵢ ≥ ⌈(31+bᵢ)/2⌉ ≥ 16`. And `Bᵢ` is `{C4,C8}`-free, so
  `eᵢ ≤ ex(12;{C4,C8}) = 17` (literature.md L15 table). Hence
  **`eᵢ ∈ {16,17}`** and **`bᵢ ≤ 3`** (`bᵢ=4` would force `eᵢ≥18>17`).
- **Degree sequences.** `eᵢ=16` forces `bᵢ=1` and degree sequence `1,1,3¹⁰`.
  `eᵢ=17` allows `1,1,5,3⁹`, `1,1,4,4,3⁸`, `1,2,4,3⁹`, or `1,3,3¹⁰`.
  Maximum degree is at most 5.
- **T3 at `n=32` is a pure tie in the order coordinate.** `qᵢ=3`, so
  `n'ᵢ = 3·10+2 = 32 = n` exactly; T3 therefore fires iff `3eᵢ < m = Σeⱼ`.
  Contrapositive: a self-sum-clean bridge has `3eᵢ ≥ Σeⱼ`. If all three are
  self-sum-clean, all `eᵢ` are equal (this also re-derives T5's
  equal-signature corollary in this instance).
- **Defect.** `m = Σeᵢ ∈ [48,51]`, so `q(G)=2n−2−m = 62−m ∈ [11,14]`,
  comfortably consistent with the proved `q(G)≥4` (defect_three.md Part VIII).
  No contradiction is available from the defect side.

### Corollary O32-3 [PROVED IN WORKSPACE, same status as O32-2]

*Every nontrivial bridge of a **Type-B** 2-cut has order `≥12`, so a Type-B
2-cut forces `n ≥ 22`.*

*Proof.* Identical to O32-2. Type B has `a₁=a₂=1` (§2c) and the edge `xy`
belongs to neither nontrivial bridge (two_cut.md §3; type_b_compatibility.md
§1), so `xy∉E(Bᵢ)` and F11's hypotheses hold verbatim. `n=c₁+c₂+2 ≥ 22`. ∎

**This does not reach 32.** Type B is not eliminated at order 32 by any order
bound currently available.

**[SUPERSEDED — `type_b_11_22_decomposition.md`, later in this session.]** The
above applies F11 to the *bare* bridge `Bᵢ` (`d(x)=1`), whose edge box has one
unit of headroom below `ex(n;{C4,C8})` at every order 13–17. Applying the same
question to the **closed** piece `Jᵢ := Bᵢ+xy = G[Cᵢ∪{x,y}]` instead — legitimate
because `xy∈E(G)` in Type B, so `Jᵢ⊆G` is still `F`-clean, and `d_{Jᵢ}(x)=aᵢ+1=2`
— removes that headroom, pinning `|E(Jᵢ)|` to `ex(n)` exactly for every
`n ≤ 17`. The resulting exhaustive census (**FB22-17**, zero survivors at every
order `≤17`) gives `|V(Jᵢ)| ≥ 18` for **both** bridges, hence
`n = n₁+n₂−2 ≥ 34 > 32`. **Type B is eliminated at order 32.** No cubic
hypothesis needed. Status: `COMPUTATIONALLY_VERIFIED`, same tier as F11/F12/FC-15.

### What Type C gets: nothing

F9/F11 requires `d_B(x)=1`. A Type-C bridge only satisfies
`min(aᵢ,bᵢ)≤2` (from `qᵢ≠1`), so bridges with `(aᵢ,bᵢ)=(2,b)` are entirely
outside the F-series' scope. A pure edge-counting attempt does not close the
gap either: for a `{C4,C8}`-free two-terminal `B` of order `nB` with
`d(x)=2, d(y)=2` and internal degree `≥3`,
`e ≥ ⌈(3nB−2)/2⌉` must be `≤ ex(nB;{C4,C8})`, which rules out
`nB ≤ 7`, `nB = 9`, and `nB = 11` outright but leaves
`nB = 8, 10, 12, 13, 14, …` arithmetically possible (the constraint is not
monotone in `nB`, because `ex` jumps irregularly). So Type C has **no order
bound at all** at present.

---

## Part 3 — The missing lemmas, named

To reach "every order-32 minimal counterexample is 3-connected" one must
eliminate every 2-cut at `n=32`. By O32-1 the cut-vertex branch is already
closed at even order, and by §2c every 2-cut is exactly Type A, B, or C. So
three things are missing, of very different sizes.

### MISSING-1 (small, finite, feasible): **F12**

> **F12.** Every simple two-terminal graph `B` with `|V(B)|=12`, `d_B(x)=1`,
> `d_B(y)≥1`, `xy∉E(B)`, `d_B(v)≥3` for `v∉{x,y}`, and `B+xy` simple and
> 2-connected, contains a `C4` or a `C8`.

F12 would, with O32-2, **eliminate Type A entirely at order 32** (indeed it
would raise the Type-A order floor to `3·11+2=35`). By the sharpening above
the search box is unusually tight: order 12, `m ∈ {16,17}`, exactly one
degree-1 vertex, maximum degree `≤5`, and one of five explicit degree
sequences. The natural command, matching the pattern already used for the
order-18 and order-19 audits, is

```
nauty-geng -c -q -d1 -D5 12 16:17 | <C4/C8 filter> | <degree-1-root + T1-closure filter>
```

`nauty-geng` is present in this worktree (`/usr/bin/nauty-geng`), and
`verifier/type_a_order10_direct.py` and `verifier/type_a_extremal_check.py`
are the existing scripts to extend. **This was deliberately not run in this
pass** (the branch's CPU is committed to other work); it is the single
highest-value cheap follow-up.

Caveat on labelling: F9/F11 are `COMPUTATIONALLY_VERIFIED`, not
`PROVED_IN_MARKDOWN`. F12 would inherit that status, and so would O32-2 and
any Type-A elimination built on it.

### MISSING-2 (medium, finite, no prior art in this repo): a **Type-C
F-series**, e.g. **FC-N**

> **FC-N.** Every simple two-terminal graph `B` with `|V(B)| ≤ N`,
> `d_B(x)=2`, `d_B(y)≥2`, `min(d_B(x),d_B(y))≤2`, `d_B(v)≥3` internally, and
> `B+xy` 2-connected, contains a `C4` or a `C8`.

Even the best possible such lemma only yields `n ≥ 2N+2` for Type C, so
`N=15` would be needed just to reach 32 — and the `nB=8,10,12,14` layers all
have to be checked. This is a genuinely new computational programme, not an
extension of an existing one, and its cost grows the way L15b's `n=20..23`
layers did.

### MISSING-3 (large, needs new mathematics): a Type-B and Type-C
**replacement/elimination** argument

Order bounds alone cannot close Types B and C at 32 (they bottom out at 22).
What is actually needed is per-type elimination, and s6_case_tree.md §1 names
the exact first unproved implication in each branch:

- **Type B:** "control the full spectra/internal cleanliness or construct a
  smaller replacement; no finite R-family follows." T9B forbids
  spectrum-subset replacements but does not make the R-family finite
  (verification_status.md, T9B row). The order-`≥40` results
  (B19 / B20 / B20D2, type_b_b19.md, type_b_one_slack_resolution.md,
  type_b_delta2_zero_slack.md) are **scoped to the 16 frozen `Π` tuples** of
  type_b_realizability.md's irreducible forced-core family, which is *not* an
  exhaustive reduction of Type B — type_b_compatibility.md's own status
  section says it is "not a claim that the surviving spectrum templates are
  realized by bridges in a counterexample," and type_b_realizability.md calls
  `Π` "its one named infinite family." A general Type-B order bound would be a
  new theorem.
- **Type C:** "Type-C replacement/balance implication; then LR\* for a rigid
  leaf." **No T5 analogue is proved for Type C** (two_cut.md §4b, s6_case_tree
  §2 table). This is the weakest branch in the whole framework.
- **Both:** the dyadic-self-sum sub-branch routes into **T7**, which is
  `CONJECTURAL` and has never been instantiated (no internally clean bridge is
  known at any order; the complete order-9 census found none among 129,040).

### MISSING-4 (untouched): everything about edge cuts

The cubic-case variant of the target — "cyclically 4-edge-connected" — has
**no supporting machinery in this repo whatsoever** beyond S4. There is no
2-edge-cut lemma and no 3-edge-cut lemma. Note that in a cubic `G`, a Type-A
2-cut with all `aᵢ=bᵢ=1` presents each bridge as attached by exactly two
edges, i.e. as a 2-edge-cut; excluding those is not implied by S4 and is not
implied by vertex 3-connectivity arguments as currently written. Reaching the
cubic variant requires starting essentially from scratch.

---

## Part 4 — Audit of the proposed argument's external premise

**The premise.** "Every min-degree-`≥3` graph through order 31 has a
power-of-two cycle." This is **external to this repository and unverified
here**, and it must not be assumed by any file in this project. Four separate
problems with it, in increasing order of severity:

### 4.1 It is far beyond anything established here, and beyond the reach of
the method that established what is here

The repo's own elimination is `n ≤ 19` (P4/L15), plus a partial clearing of
`n=20..23` (top edge layer only; 4 near-cubic cases open). The `{C4,C8}`
method **provably stops at `n=24`**, because Markström's 24-vertex cubic
`{C4,C8}`-free graph exists (its only power-of-two cycle length is 16). So for
`n ∈ [24,31]` one would need genuine `C16` detection over the full `δ≥3`
census, and verification_status.md's IV.B row already records order 26 as
`INFEASIBLE` (raw `n=22` `C4`-free cubic generation did not complete in 400 s;
`n=26` extrapolates to ~6 days for generation alone). An exhaustive order-31
result is not plausibly a completed computation; if the external claim is real
it must be a structural theorem, and it should be treated as such — sourced,
read, and audited — before any use.

### 4.2 The closure step in the sketch does not produce a `δ≥3` graph, so an
"every `δ≥3` graph of order `≤31`" premise does not apply to it

This is the decisive objection. Capping bridge `Bᵢ` with the artificial
terminal edge gives `Bᵢ+xy`, in which `deg(x) = aᵢ+1 = 2` for Types A and B
(and `≤3` in Type C). `Bᵢ+xy` is 2-connected (T1) with internal degree `≥3`,
but it is **not** a minimum-degree-3 graph. No theorem about `δ≥3` graphs —
at order 31 or any other order — says anything about it.

The repository already knows this, and its whole design reflects it:

- **T2** uses Gao–Huo–Liu–Ma precisely because that theorem needs only
  "`Bᵢ+xy` 2-connected" plus "internal degree `≥ k+1`", never `δ≥3`.
- **T3/T5/T6** restore `δ≥3` by *gluing `qᵢ` copies* of the bridge at the
  terminals, which is the only device in the repo that produces a genuine
  `δ≥3` object from a bridge — and gluing **increases** order:
  `n'ᵢ = qᵢcᵢ + 2`, typically `≥ n`. That is exactly why T3 is conditional on
  a lex comparison and why two_cut.md §3 spells out that ties and losses are
  non-informative.
- **F9/F11** are stated in the *correct* two-terminal shape (degree-1 root,
  internal degree `≥3`, 2-connected closure) — they are the repo's actual
  finite input, and they are not instances of any `δ≥3` statement.

### 4.3 Even granting the premise, "≤31" misses the critical case by exactly one

The one place a "`δ≥3` graphs of order `≤N`" theorem *would* plug in is T3:
if the glued graph `G'ᵢ` (which does have `δ≥3`) has order `n'ᵢ ≤ N`, then it
has a power-of-two cycle, and since internal-copy cycles are `F`-clean the
culprit must be `(Λᵢ+Λᵢ)∩F ≠ ∅`. But T3 already delivers that for every
`n'ᵢ < n` from `G`'s own minimality. So the premise buys exactly the window
`n ≤ n'ᵢ ≤ N`.

At the order-32 Type-A case, Corollary O32-2 forces `cᵢ=10` and hence
`n'ᵢ = 3·10+2 = 32`. A premise at `N=31` **does not reach it.** A premise at
`N=32` would reach it — but "every `δ≥3` graph of order `≤32` has a
power-of-two cycle" says outright that no order-32 counterexample exists,
which is strictly stronger than, and makes vacuous, the theorem it is being
used to prove. So in the regime where the premise is stated it is too weak,
and in the regime where it would help it is circular.

### 4.4 The `{3,7,15}` conclusion has the wrong sign relative to a fact
already proved here

If the sketch's mechanism worked, a forced power-of-two cycle through the
artificial edge `xy` would be `xy` plus an `x`–`y` path of length `2^k−1`,
i.e. it would force `Λᵢ ∩ {3,7,15,31,…} ≠ ∅`. But two_cut.md §2's
trivial-bridge corollary **proves the opposite** in exactly the case where the
terminal edge is real: if `xy ∈ E(G)` (Type B) then `Λᵢ ∩ {2^k−1} = ∅` for
every nontrivial bridge. So the sketch's conclusion, if it could be
established, would immediately contradict the proved Type-B fact and thereby
eliminate Type B — which is a genuinely attractive target and is presumably
what the sketch is reaching for. The obstruction is §4.2: the closure is not
`δ≥3`, so nothing forces the cycle in the first place. The `{3,7,15}` set also
appears independently in contraction_separator_integration.md VII.1 as the
unsafe family `ℓ=2^j−1` for a paired-`K4` union at offset 2; that is a
separate, already-proved statement and should not be conflated with the
sketch's.

### 4.5 Verdict on the premise

**The 2-cut framework does not need the external order-`≤31` claim, and cannot
use it in the form given.** The correct-shaped finite input is the
two-terminal F-series (F9/F11 → F12 → …), which the repo already has at
`N=11`. The proposed argument should be re-derived on that footing.

---

## Part 5 — Triage verdict

**How close is "every order-32 minimal counterexample is 3-connected"?**

| Branch | Distance | Notes |
|---|---|---|
| Cut-vertex (S5 / branch C0) | **Closed** | O32-1: free at every even order, from S5's parity claim. No new work. |
| Type A 2-cut | ~~**One finite computation away**~~ → **Closed** | O32-2 already forces the unique configuration (three order-12 bridges, `eᵢ∈{16,17}`, `bᵢ≤3`, max degree `≤5`). F12 closes it. [`f12_order12_result.md`, done] |
| Type B 2-cut | ~~**Far**~~ → **Closed** | ~~Best available bound is `n≥22` (O32-3).~~ FB22-17 (`type_b_11_22_decomposition.md`) gives `n≥34`. The `n≥40` results remain scoped to 16 frozen `Π` tuples and were not used. |
| Type C 2-cut | **Farthest — now the only open branch** | FC-15 (`fcn_order15_result.md`) supplies MISSING-2 for the `d_B(x)=2` profile but, per that file's own correction, does not by itself bound Type C's order (the `a_i=1` sub-case takes the weaker route). No T5 analogue. Still needs MISSING-3. The `(2,2)`-closure trick that closed Type B is unavailable: Type C has `xy∉E(G)`, so there is no terminal edge to close with. |
| Cubic / cyclically 4-edge-connected variant | **Not started** | Only S4 exists. No 2-edge-cut or 3-edge-cut lemma anywhere in the repo. |

**Summary judgement.** The order-32 target is *not* a small extension of
existing work, but it is also not uniformly far: it decomposes into one branch
that is already free (cut vertices, by parity), one branch that is within a
single tractable `n=12` census (Type A), and two branches (B and C) that need
substantially new machinery of the kind s6_case_tree.md has been naming as
FIRST UNPROVED for several passes. The proposed external premise is not the
bottleneck and would not help; the bottleneck is the absence of any finite
two-terminal proposition beyond `d_B(x)=1, N=11`, plus the absence of a
Type-C replacement lemma.

**Recommended focused follow-up, in priority order.**

1. **Run F12** (MISSING-1). Cheap, exactly specified above, and it converts
   O32-2 into a complete Type-A elimination at order 32 — the first
   unconditional per-order separator theorem in the project.
2. Record O32-1 and O32-2 in two_cut.md / s6_case_tree.md and update
   verification_status.md, so the Type-A row's "Type-A bridge orders ≤11
   (finite only)" entry is upgraded to the order consequence.
3. Begin MISSING-2 at `nB = 8, 10, 12` for the `(2,2)` terminal profile (the
   arithmetic above already excludes `nB ∈ {5,6,7,9,11}` with no computation).
4. Leave MISSING-3 and MISSING-4 as flagged long-horizon targets; do not
   attempt them under an assumed order-`≤31` premise.

**Discipline note.** O32-1 is `PROVED_IN_MARKDOWN` outright. O32-2 and O32-3
are `PROVED_IN_MARKDOWN` *conditional on* F11, which is
`COMPUTATIONALLY_VERIFIED` and not proof-assistant formal; any downstream
statement inherits that. Nothing in this file is `NOVELTY_CHECKED`.
