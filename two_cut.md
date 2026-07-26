# two_cut.md — toward 3-connectivity of a minimal counterexample

**Status as of 2026-07-25 (sixth redirection pass — T4, the exact
bridge-count classification, the corrected balanced census, and T5
added).** New main target,
replacing the one-pole gadget theory as the project's top priority (that
work is frozen, not abandoned — see one_pole.md). This file works in the
**2-connected case specifically**: G a lexicographically minimal
counterexample (δ≥3, no cycle of length in F={4,8,16,…}, minimizing
(|V|,|E|) lexicographically), **assumed 2-connected** for everything
below. This is honestly scoped, not overclaimed: S5 (lemmas.md) proved
"at most one cut vertex," leaving one surviving cut-vertex case open;
one_pole.md's logical-scope section already identified "the 2-connected
minimal-counterexample case" as the separate remaining task, and this file
is exactly that task. Nothing here establishes 2-connectivity itself for
every minimal counterexample — it is the standing hypothesis of this
entire file, matching the case split already on record.

**Goal:** *Every lexicographically minimal Erdős–Gyárfás counterexample is
3-connected.* Kept CONJECTURAL throughout — see §7.

## 1. The exact 2-cut decomposition

Let {x,y} be a 2-cut of G (so G−{x,y} is disconnected — the standard
sense in which a 2-element vertex set "cuts"). Let C₁,…,C_t (t≥2) be the
components of G−{x,y}; the **nontrivial xy-bridges** are Bᵢ := G[Cᵢ∪{x,y}]
(i=1,…,t). If xy∈E(G), that edge is a separate **trivial bridge** B₀ with
Λ₀={1} (handled explicitly in §2). Write aᵢ:=deg_{Bᵢ}(x),
bᵢ:=deg_{Bᵢ}(y).

**aᵢ,bᵢ≥1 for every bridge [PROVED, uses 2-connectivity of G].** If
aᵢ=0 (no edge x–Cᵢ), then Cᵢ's only external connection is through y
(its edges are entirely internal to Cᵢ or to y — bridges are pairwise
non-adjacent except via x,y), so G−y would disconnect Cᵢ from the rest —
making y a cut vertex, contradicting G 2-connected. Symmetric for bᵢ. ∎

### T1. Bridge closure is 2-connected [PROVED IN WORKSPACE — likely standard/folklore in structural graph theory, not claimed novel]

*For every nontrivial xy-bridge Bᵢ, Bᵢ+xy (add the edge if absent) is
2-connected.*

*Proof.* Suppose Bᵢ+xy has a cut vertex w.
- **w=x** (symmetrically w=y): (Bᵢ+xy)−x = Bᵢ−x (the added edge vanishes
  with x). G−x is connected (2-connectivity of G) and contains y with all
  of Cᵢ's vertices, whose only external gateway (with x removed) is y
  (bridges are pairwise non-adjacent except via x,y). So within G−x, every
  path reaching Cᵢ must pass through y — meaning Cᵢ∪{y} cannot itself
  split into pieces some of which fail to reach y (any such piece would be
  entirely isolated in G−x, contradicting G−x connected). Hence Bᵢ−x is
  connected — contradicting w=x a cut vertex.
- **w=z, an internal vertex** (z∈Cᵢ): z's neighbors are entirely inside
  Bᵢ (bridges pairwise non-adjacent except via x,y, and z≠x,y), so
  removing z affects no other bridge. G−z is connected (2-connectivity of
  G). **Using 2-connectivity of G:** every component of (Bᵢ−z) must
  attach to x or to y in G−z — else that component would be isolated in
  G−z entirely (its only gateways to the rest of G, absent z, are x and
  y), contradicting G−z connected. So (Bᵢ−z)'s components partition into
  those touching x, those touching y (possibly overlapping if a component
  touches both). In (Bᵢ+xy)−z, the added edge xy directly joins x and y,
  so every x-touching component, every y-touching component, and {x,y}
  themselves all merge into **one** connected graph — contradicting w=z a
  cut vertex.

All cases contradict, so Bᵢ+xy is 2-connected. ∎

### T2. Endpoint admissible paths [T2 PROVED IN WORKSPACE; underlying theorem KNOWN FROM LITERATURE]

Λᵢ := {lengths of simple x–y paths in Bᵢ}.

*Proof.* Apply Gao–Huo–Liu–Ma (cited and verified in one_pole.md O4′:
Jun Gao, Qingyi Huo, Chun-Hung Liu, Jie Ma, "A Unified Proof of
Conjectures on Cycle Lengths in Graphs," IMRN 2022(10):7615–7653,
arXiv:1904.08126) with G:=Bᵢ, x,y as given, k=2. Hypothesis "Bᵢ+xy
2-connected" is exactly T1. Hypothesis "every vertex of Bᵢ∖{x,y} has
degree ≥k+1=3": every internal vertex z∈Cᵢ has all its G-edges inside Bᵢ
(shown above), so deg_{Bᵢ}(z)=deg_G(z)≥3 (G has δ≥3) — **automatic from
G's own minimum degree, no extra hypothesis needed** (unlike the one-pole
setting, where this needed the one-pole definition itself). Both
hypotheses hold, giving 2 admissible x–y paths: **Λᵢ contains 2 values
differing by 1 or 2.** ∎

## 2. The global bridge-spectrum identity [PROVED]

**Every cycle crossing the 2-cut (using ≥2 distinct bridges' interiors)
visits both x and y, and decomposes into exactly 2 arcs, each an x–y path
lying entirely within one bridge, in two *different* bridges.**

*Proof.* A simple cycle visits x at most once, y at most once. Bridges
are pairwise non-adjacent except through x,y, so between consecutive
visits to {x,y} the cycle must stay in one bridge. A cycle avoiding y
entirely, using ≥2 bridges' interiors, is impossible (leaving x into one
bridge's interior, the only way to reach a second bridge or return to
close the cycle is via y); symmetrically avoiding x. So such a cycle uses
both x,y, splitting into exactly 2 arcs (consecutive-visit segments),
each confined to one bridge; using ≥2 bridges forces the 2 arcs into 2
*different* bridges (using only 1 bridge would mean the whole cycle lies
in that bridge, not "crossing"). ∎

**Exact identity:** for i≠j, {lengths of cycles crossing via bridges i,j}
= Λᵢ+Λⱼ (the converse direction — any ℓᵢ∈Λᵢ, ℓⱼ∈Λⱼ concatenate into a
genuine simple cycle, since Bᵢ,Bⱼ share only x,y — is immediate). Since G
is F-clean:
[
(\Lambda_i+\Lambda_j)\cap\mathcal F=\varnothing\qquad(i\ne j).
]

**Internal cycle spectra, recorded separately [PROVED, trivial by
inheritance].** Any cycle lying entirely within one Bᵢ is a cycle of G
(Bᵢ⊆G), hence F-clean automatically — no new argument needed, just
recorded as a distinct bookkeeping category from the cross-bridge sums
above (matching the same discipline as one_pole.md's terminal-spectrum
section).

**Trivial bridge, if xy∈E(G) [PROVED, corollary].** Treating xy as bridge
B₀ with Λ₀={1}, the identity with j=0 gives (Λᵢ+{1})∩F=∅ for every
nontrivial i, i.e.
[
\Lambda_i\cap\{2^k-1:k\ge2\}=\varnothing.
]

## 2b. T4: minimal terminal cover [PROVED — 2026-07-25, sixth pass]

Recall aᵢ=deg_{Bᵢ}(x), bᵢ=deg_{Bᵢ}(y), s=1 if xy∈E(G) else 0.

**T4.** *No proper sub-selection of {B₁,…,B_t}∪{the xy edge, if present}
has degree ≥3 at both x and y.* Precisely: for every proper subset
S⊊{1,…,t} of the nontrivial bridges and every e∈{0,…,s} (i.e. e=0
always allowed, e=1 only if s=1), the union Uₛ,ₑ := (∪_{i∈S}Bᵢ) ∪
({xy} if e=1) satisfies deg_U(x)<3 or deg_U(y)<3 — **except** when S is
the full bridge set {1,…,t} *and* e=s (that selection is just G itself).

*Proof.* Every internal vertex of a selected bridge keeps its full
G-degree (its edges never leave that bridge). Every cycle of U is a
cycle of G (U⊆G). Suppose some proper U had deg_U(x)≥3 and deg_U(y)≥3
(so U also has δ(U)≥3, combining with the internal-vertex fact — this is
a genuine δ≥3, F-clean candidate). Two ways U can be proper:
- **Omits a nontrivial bridge Bₖ** (S⊊{1,…,t}). Bₖ is nonempty (a
  genuine component of G−{x,y}), so |V(U)|<|V(G)| strictly — U is then a
  smaller δ≥3, F-clean graph, contradicting G's **order**-minimality.
- **Includes every bridge but omits the edge** (S={1,…,t}, e=0<s=1).
  Here |V(U)|=|V(G)| exactly (no vertex lost), but |E(U)|=|E(G)|−1
  strictly — U is then a same-order, strictly-fewer-edges δ≥3, F-clean
  graph, contradicting G's **edge**-minimality (given the order tie).

Either way, contradiction. So no proper U reaches degree ≥3 at both
terminals. ∎

**Immediate per-bridge consequence.** Applying T4 to S={1,…,t}∖{k}, e=s
(omit just bridge k, keep everything else): Σ_{i≠k}aᵢ+s<3 or
Σ_{i≠k}bᵢ+s<3, i.e. (using Σᵢaᵢ+s=deg_G(x)): **aₖ≥deg_G(x)−2 or
bₖ≥deg_G(y)−2**, for every bridge k.

**Consequence when xy∈E(G).** Applying T4 to S={1,…,t}, e=0 (omit just
the edge): Σaᵢ<3 or Σbᵢ<3, i.e. deg_G(x)−1<3 or deg_G(y)−1<3. Since
δ(G)≥3 forces deg_G(x),deg_G(y)≥3, "<4" means "=3" exactly: **if
xy∈E(G), then deg_G(x)=3 or deg_G(y)=3.**

## 2c. The exact bridge-degree classification [PROVED — 2026-07-25]

**Pairwise lemma, t≥3 [PROVED].** For t≥3, every 2-element subfamily
{Bᵢ,Bⱼ} is proper, so T4 (with e=0) gives aᵢ+aⱼ<3 or bᵢ+bⱼ<3 for every
pair i≠j. Since aᵢ,bᵢ≥1 always (§1), "<3" with 2 terms each ≥1 forces
**both terms =1**: for every pair, **aᵢ=aⱼ=1 or bᵢ=bⱼ=1**.

**Common-coordinate lemma [PROVED — short combinatorial argument].**
*For t≥3, either all aᵢ=1, or all bᵢ=1.* Let A′={i : aᵢ≠1}. If A′=∅,
done (all a=1). Otherwise pick q∈A′; for any other bridge p (p=q
excluded), the pair {p,q} cannot be a-linked (aq≠1), so must be b-linked:
**bₚ=b_q=1**. This holds for every p≠q — in particular for every p∈A′
too (chaining through q) and every p∉A′ — so **every** bridge has
b=1. ∎ (This is the t=3 argument from the fifth pass, shown to extend
verbatim to any t≥3: the pairwise dichotomy plus one "hub" bridge q with
a_q≠1 forces the b-coordinate universally.)

**t≥4 is impossible [PROVED — new in this pass].** By the lemma above,
t≥3 forces a common coordinate =1 for *all* t bridges — WLOG all aᵢ=1
(else swap x,y). If t≥4, pick any 3 of the t bridges; this triple is a
*proper* subfamily (t≥4>3), so T4 gives: (sum of a over the 3)<3 or (sum
of b over the 3)<3. The a-sum is exactly 1+1+1=3 (not <3 — fails). The
b-sum is ≥1+1+1=3 (each bᵢ≥1, three terms — also fails, regardless of
the actual values). **Both disjuncts fail simultaneously — contradicting
T4.** So t≥4 is impossible.

**Conclusion: every 2-cut has exactly 2 or 3 nontrivial bridges** (t≥2
always, by definition of a disconnecting 2-cut).

**Type A (t=3).** All 3 share a common coordinate =1; WLOG (swap x,y)
**a₁=a₂=a₃=1**. Then deg_G(x)=Σaᵢ+s=3+0=**3** (s=0, since t=3 already
saturates T4's pairwise dichotomy without needing an edge — if xy∈E(G)
too, deg_G(x) would be 4, but then the pairwise argument's "<3" bound
aᵢ+aⱼ<3 would need to be checked against 2, still fine numerically, but
turning to the "if xy∈E(G)" consequence above, deg_G(x)=3 or deg_G(y)=3
would be needed *in addition* — consistent only if s=0 here, since
deg_G(x)=3 exactly with 3 unit contributions from the bridges leaves no
room for a 4th unit from an edge; **so Type A has xy∉E(G)** exactly as
stated). qᵢ=max(⌈3/1⌉,⌈3/bᵢ⌉)=max(3,·)=**3** for all i (the aᵢ=1 term
dominates regardless of bᵢ). **Type A: t=3, xy∉E(G), a₁=a₂=a₃=1,
deg_G(x)=3, q₁=q₂=q₃=3.**

**Type B (t=2, xy∈E(G)).** From the "xy∈E(G)" consequence: deg_G(x)=3 or
deg_G(y)=3; WLOG deg_G(x)=3. Then a₁+a₂+s=a₁+a₂+1=3, so **a₁+a₂=2**,
forcing (both ≥1) **a₁=a₂=1** exactly. Consistency check against the
single-bridge conditions {Bᵢ,xy} (i=1 or 2): aᵢ+1<3 or bᵢ+1<3 — satisfied
automatically via aᵢ=1<2. qᵢ=max(3,⌈3/bᵢ⌉)=**3** for both. **Type B: t=2,
xy∈E(G), a₁=a₂=1, deg_G(x)=3, q₁=q₂=3.**

**Type C (t=2, xy∉E(G)).** T4 on each single bridge {Bᵢ} alone: aᵢ<3 or
bᵢ<3 — i.e. **neither bridge has both terminal degrees ≥3**. Since s=0,
deg_G(x)=a₁+a₂≥3 and deg_G(y)=b₁+b₂≥3 are just G's own min-degree,
restated. qᵢ∈{2,3} for both (qᵢ=1 excluded exactly by "neither bridge has
both ≥3", matching the fifth pass's self-forcing lemma, now derived
directly from T4 instead of a separate order-minimality argument). **Type
C: t=2, xy∉E(G), a₁+a₂≥3, b₁+b₂≥3, neither bridge has both terminal
degrees ≥3, q₁,q₂∈{2,3}.**

## 3. The bridge self-forcing lemma

For nontrivial bridge Bᵢ: aᵢ=deg_{Bᵢ}(x), bᵢ=deg_{Bᵢ}(y),
qᵢ = max(⌈3/aᵢ⌉, ⌈3/bᵢ⌉).

**qᵢ=1 is impossible [PROVED, by order-minimality].** qᵢ=1 ⟺ aᵢ≥3 AND
bᵢ≥3. If so, Bᵢ *itself* already has δ(Bᵢ)≥3 (internal vertices ≥3 as in
T2; x,y have Bᵢ-degree aᵢ,bᵢ≥3), and Bᵢ's cycles are F-clean (inherited
from G). Since {x,y} is a genuine disconnecting 2-cut, t≥2, so some other
bridge Bⱼ (j≠i) contributes vertices not in Bᵢ, giving |Bᵢ|<|G| strictly.
Bᵢ is then a smaller δ≥3, F-clean graph — contradicting G's
order-minimality. So **qᵢ∈{2,3}** for every nontrivial bridge (aᵢ,bᵢ≥1
always, by §1, so qᵢ≤3 always; qᵢ=1 just excluded).

**The qᵢ-fold gluing [PROVED].** Glue qᵢ disjoint copies of Bᵢ,
identifying all copies' x's into x\*, all copies' y's into y\* (the
direct edge xy — if present in G — is handled as its own separate bridge,
**not** duplicated; Bᵢ itself never contains it by definition, so no
multi-edge issue arises from the gluing itself).
- **Simple.** Each copy's internal vertices are fresh (disjoint across
  copies); only x\*,y\* are shared. No two copies share an edge (edges are
  internal-to-copy or copy-to-{x\*,y\*}, all distinct pairs across
  copies).
- **δ≥3 everywhere.** Internal (copy-local) vertices: unchanged Bᵢ-degree
  ≥3. deg(x\*) = qᵢ·aᵢ ≥ aᵢ⌈3/aᵢ⌉ ≥ 3 (standard ceiling inequality, using
  qᵢ≥⌈3/aᵢ⌉ by definition of qᵢ as the max of the two ceilings).
  Symmetrically deg(y\*) = qᵢ·bᵢ ≥ 3.
- **New cycles use exactly 2 copies, lengths exactly Λᵢ+Λᵢ.** A simple
  cycle visits x\*,y\* each at most once; copies share only these 2
  vertices, so (same argument as §2) any cycle not confined to 1 copy
  splits into exactly 2 arcs in 2 *different* copies — but since **every**
  copy has the *same* spectrum Λᵢ, "different copies" contributes exactly
  the self-sumset Λᵢ+Λᵢ regardless of which 2 of the qᵢ copies are used.
  Cycles confined to 1 copy inherit Bᵢ's own F-clean (inherited from G)
  spectrum.

**Parameters:** n'ᵢ = qᵢ(|V(Bᵢ)|−2)+2 (each copy contributes
|V(Bᵢ)|−2 fresh internal vertices; x\*,y\* counted once). m'ᵢ = qᵢ|E(Bᵢ)|
(edges never shared across copies).

### T3 [PROVED]

*If (n'ᵢ,m'ᵢ) <_lex (|V(G)|,|E(G)|), then (Λᵢ+Λᵢ)∩F≠∅.*

*Proof.* If the glued graph G'ᵢ were ALSO F-clean, its only possible
forbidden-length source (internal-copy cycles are already safe by
inheritance; cross-copy cycles are exactly Λᵢ+Λᵢ) would have to be
avoided, i.e. (Λᵢ+Λᵢ)∩F=∅ — making G'ᵢ a genuine δ≥3, F-clean graph with
(order,edges) strictly lex-smaller than G, contradicting G's
lexicographic minimality. So G'ᵢ is not F-clean, and since internal
cycles are ruled out as the cause, (Λᵢ+Λᵢ)∩F≠∅. ∎

**Order and edge ties, handled explicitly.** (n'ᵢ,m'ᵢ) <_lex (|V(G)|,
|E(G)|) means *either* n'ᵢ<|V(G)| (edges irrelevant), *or* n'ᵢ=|V(G)| AND
m'ᵢ<|E(G)|. If instead n'ᵢ=|V(G)| AND m'ᵢ=|E(G)| (**full tie**), or
n'ᵢ>|V(G)|, or (n'ᵢ=|V(G)| and m'ᵢ>|E(G)|): **no contradiction is
extractable and T3's conclusion does not follow** — G'ᵢ merely ties or
loses to G in the lex order, which is not informative on its own. This is
the case analyzed combinatorially in §4.

## 4. Classifying bridges that evade T3 (the balanced 2-cut census)

cᵢ := |V(Bᵢ)|−2 (bridge i's internal vertex count), N := |V(G)|−2 =
Σᵢcᵢ (all bridges partition G's non-{x,y} vertices).

**Evading the order part of T3** means n'ᵢ = qᵢcᵢ+2 ≥ |V(G)| = N+2, i.e.
**qᵢcᵢ ≥ N**.

**At most 3 bridges can evade simultaneously [PROVED].** Since qᵢ≤3
always (§3), an evading bridge has cᵢ ≥ N/qᵢ ≥ N/3. If k bridges evade,
Σ over just those k gives ≥ kN/3 ≤ Σ_all cᵢ = N (evading bridges are a
subset of all bridges, each cᵢ>0), so **k≤3**.

**k=3 (three bridges evade simultaneously) [PROVED, forces exact equality
in BOTH cᵢ and eᵢ — corrected from the fifth pass, which stopped at an
inequality; the inequality does force exact equality after all, shown
below].** Each of the 3 needs cᵢ≥N/3; if any had qᵢ=2 its requirement
would be cᵢ≥N/2, and combined with the other two's ≥N/3 each the sum
would exceed N — impossible since these 3 alone must fit within Σcᵢ=N
(qᵢ=2 for even one of the three already forces N/2+N/3+N/3=7N/6>N,
impossible). So **all 3 evading bridges have qᵢ=3 exactly**, and since
each individually needs cᵢ≥N/3 while collectively Σ(these 3)≤N, equality
is forced: **cᵢ=N/3 for all 3** (requires 3∣N), and **t=3 exactly** (no
room for a 4th nontrivial bridge — the three already exhaust N). **This
is evading only the order part of T3** — the weaker, order-only
statement.

**Evading T3's full lexicographic conclusion** (order tied *and* the
edge tie-break also fails to produce a contradiction, i.e. m'ᵢ≥|E(G)|
for every i, not just ≥ for the winner) is strictly stronger. Writing
eᵢ:=|E(Bᵢ)|, |E(G)|=e₁+e₂+e₃+[xy∈E(G)]: requiring m'ᵢ=3eᵢ≥|E(G)| for
i=1,2,3 and summing gives 3Σeᵢ≥3Σeᵢ+3[xy], forcing **[xy∈E(G)]=0**, and
each individual condition reduces to **2eᵢ≥eⱼ+eₖ** for every permutation
{i,j,k}={1,2,3}. **Correction to the fifth pass: this inequality, applied
to all 3 simultaneously, DOES force exact equality** — the earlier
statement that it left a nontrivial solution family was an incomplete
derivation, not a genuine gap. *Proof:* order the three values
e_(1)≥e_(2)≥e_(3) (relabeling). The condition for the smallest, e_(3):
2e_(3)≥e_(1)+e_(2). But e_(1)≥e_(3) and e_(2)≥e_(3) give
e_(1)+e_(2)≥2e_(3) unconditionally. Combining: 2e_(3) ≥ e_(1)+e_(2) ≥
2e_(3), forcing **e_(1)+e_(2)=2e_(3) exactly**; since both e_(1),e_(2)
are individually ≥e_(3) and their sum equals exactly 2e_(3), neither can
exceed e_(3) (that would force the other below e_(3), contradicting
minimality) — so **e_(1)=e_(2)=e_(3)**. Hence **e₁=e₂=e₃ exactly.** ∎

**k=2, both qᵢ=2 [PROVED, forces exact equality in both cᵢ and eᵢ — the
closest analogue to S5's equal-lobe result].** Both need cᵢ≥N/2; sum
≥N=Σ(all cᵢ), forcing **c₁=c₂=N/2 exactly** (2∣N) and **t=2 exactly** (no
room for other bridges). Edge side: m'ᵢ=2eᵢ≥|E(G)|=e₁+e₂+[xy] for i=1,2.
Adding: e₁≥e₂+[xy] and e₂≥e₁+[xy]; combining forces **[xy∈E(G)]=0** and
then **e₁=e₂ exactly** — a clean, fully forced equality, directly
analogous to S5's "equal edge count" conclusion for its 2-lobe cut-vertex
case.

**k=2, mixed or both qᵢ=3; k=1.** These do **not** force exact equalities
— they leave a genuine range of consistent (cᵢ,eᵢ) values (e.g. k=2 with
q₁=2,q₂=3: c₁≥N/2, c₂≥N/3, sum ≥5N/6, leaving room (possibly zero) for
further non-evading bridges; k=1 leaves even more freedom). **Recorded
honestly as not uniquely classified** rather than forced into a false
precise statement — this matches the instruction not to claim 2-cuts are
impossible until every balanced case is treated, and not every case
*can* be pinned to a unique configuration the way S5's single surviving
case was.

**Summary — the finite list of *fully forced* balanced configurations
(corrected):**
1. **t=2, q₁=q₂=2, c₁=c₂=N/2, xy∉E(G), e₁=e₂ exactly** (S5 analogue).
2. **t=3, q₁=q₂=q₃=3, c₁=c₂=c₃=N/3, xy∉E(G), e₁=e₂=e₃ exactly**
   (corrected — full equality, not merely an inequality).
Both are now fully pinned S5-style equal-signature configurations, not
one exact and one merely constrained. Plus a non-exhaustively-classified
family of partial (k≤2, not both qᵢ=2) evasions that remain open —
**2-cuts are not claimed impossible**; every one of these cases, plus the
open partial-evasion family, needs further treatment (§7) before any
such claim could be made. (§2b–2c's t∈{2,3} classification is logically
independent of and stronger than this k-evasion census — it holds for
*every* 2-cut, not just the balanced ones; the two are cross-referenced
in §7.)

## 4b. T5: replacement forcing [PROVED — 2026-07-25, sixth pass]

### Three-bridge version (Type A: t=3, xy∉E(G), a₁=a₂=a₃=1)

For distinct i,j,k∈{1,2,3}, build **H_{ij}** := 2 copies of Bᵢ + 1 copy
of Bⱼ, glued at shared x\*,y\* (bridge k is entirely excluded).

**δ(H_{ij})≥3 [PROVED].** Internal vertices: unchanged copy-degree ≥3.
deg(x\*) = 2aᵢ+aⱼ = 2·1+1 = 3 (Type A: all a=1). deg(y\*) = 2bᵢ+bⱼ ≥
2·1+1 = 3 (bᵢ,bⱼ≥1 always) — automatically ≥3 regardless of the actual
b-values.

**Only potentially new cycle lengths lie in Λᵢ+Λᵢ [PROVED].** H_{ij} has
3 "copies" total (2 of Bᵢ, 1 of Bⱼ) sharing x\*,y\*. A cycle confined to
1 copy inherits that bridge's own F-clean (inherited from G) spectrum.
A cycle crossing 2 copies could in principle pair (copyᵢ,copyᵢ) →
Λᵢ+Λᵢ, or (copyᵢ,copyⱼ) → Λᵢ+Λⱼ — but **(Λᵢ+Λⱼ)∩F=∅ is already
guaranteed** by §2's global bridge-spectrum identity (Bᵢ,Bⱼ are genuine
bridges of the *same* 2-cut in the *actual* G, so their real spectra are
already cross-clean) — no new information there. The **only** genuinely
untested combination is Λᵢ+Λᵢ (pairing 2 *different* copies of the *same*
bridge — a configuration that never occurs in G itself, which has only
one copy of each bridge).

**Parameters and the reduction to comparing bridge i against bridge k
directly [PROVED].** |V(H_{ij})|=2cᵢ+cⱼ+2, |E(H_{ij})|=2eᵢ+eⱼ.
Using |V(G)|=cᵢ+cⱼ+cₖ+2, |E(G)|=eᵢ+eⱼ+eₖ (xy∉E(G) in Type A):
[
|V(H_{ij})|-|V(G)| = c_i-c_k,\qquad
|E(H_{ij})|-|E(G)| = e_i-e_k
]
— **bridge j's own (cⱼ,eⱼ) cancels out of both comparisons entirely.**
So H_{ij} beats G lexicographically **exactly when** (cᵢ,eᵢ) <_lex
(cₖ,eₖ) — comparing the doubled bridge to the dropped one, directly.

**T5 (three-bridge version) [PROVED].** *If (cᵢ,eᵢ) <_lex (cₖ,eₖ), then
(Λᵢ+Λᵢ)∩F≠∅.* If H_{ij} were F-clean, it would be a genuine δ≥3,
F-clean graph strictly lex-smaller than G (contradiction); since the
only untested cycle source is Λᵢ+Λᵢ, that must be the culprit. ∎

**Corollary: every self-sum-clean bridge is lexicographically maximal
[PROVED].** If (Λᵢ+Λᵢ)∩F=∅ ("bridge i is self-sum-clean"), the
contrapositive of T5 gives: for every k≠i, NOT[(cᵢ,eᵢ)<_lex(cₖ,eₖ)], i.e.
**(cᵢ,eᵢ) ≥_lex (cₖ,eₖ) for every other bridge k** — bridge i's own
signature is lex-maximal among the 3.

**Corollary: if all 3 are self-sum-clean, all 3 signatures coincide
exactly [PROVED].** Each of the 3 being lex-maximal simultaneously forces
(cᵢ,eᵢ)≥(cⱼ,eⱼ) and (cⱼ,eⱼ)≥(cᵢ,eᵢ) for every pair — a total order forces
equality both ways — so **(c₁,e₁)=(c₂,e₂)=(c₃,e₃) exactly.** This
reconfirms §4's corrected "k=3 full-evasion" conclusion via a completely
independent route (T5's replacement construction, rather than the direct
gluing-parameter inequality), a genuine cross-check.

### Two-bridge-plus-edge version (Type B: t=2, xy∈E(G), a₁=a₂=1)

For i≠j∈{1,2}, build **H_i** := 2 copies of Bᵢ + the retained edge xy,
glued at x\*,y\* (bridge j excluded, edge kept).

**δ(H_i)≥3.** deg(x\*)=2aᵢ+1=2·1+1=3 (Type B: aᵢ=1). deg(y\*)=2bᵢ+1≥3
(bᵢ≥1) automatically.

**Only new cycles: Λᵢ+Λᵢ.** Cycles within 1 copy: safe (inherited).
Cycles using the retained edge plus one copy's path: length ℓ+1 for
ℓ∈Λᵢ — already guaranteed safe by §2's Mersenne corollary
(Λᵢ∩{2ᵏ−1}=∅, since Bᵢ is a genuine bridge of G with xy∈E(G)). Cycles
crossing the 2 copies of Bᵢ (not using the edge): Λᵢ+Λᵢ — the only
untested source, exactly as in the three-bridge version.

**Parameters:** |V(H_i)|=2cᵢ+2 vs |V(G)|=cᵢ+cⱼ+2 ⟹ difference cᵢ−cⱼ.
|E(H_i)|=2eᵢ+1 vs |E(G)|=eᵢ+eⱼ+1 ⟹ difference eᵢ−eⱼ. Bridge j's own
signature again cancels out entirely.

**T5 (two-bridge-plus-edge version) [PROVED].** *If (cᵢ,eᵢ) <_lex
(cⱼ,eⱼ), then (Λᵢ+Λᵢ)∩F≠∅.* Same argument as the three-bridge version.
∎ **Same corollaries apply**: a self-sum-clean bridge is lex-maximal
between the 2, and if both are self-sum-clean, (c₁,e₁)=(c₂,e₂) exactly —
matching Type B's own analogue of the S5-style equal-signature
conclusion, derived independently of §4's direct route.

## 5. Bridge-signature library [see verifier/bridge_signature.py, experiments.md E19]

Σ(B) = (|V(B)|−2, |E(B)|, d_B(x), d_B(y), Λ(B), C_F(B)) for
two-terminal graphs B with: **xy∉E(B)** (the direct terminal edge is
modeled separately); B+xy 2-connected (T1's requirement); internal
minimum degree ≥3; and internal cycles avoiding F. Here C_F(B):=
C(B)∩F is the **dyadic internal-cycle spectrum**, not the complete cycle
spectrum. Both Λ(B) and C_F(B) are computed with two independent
implementations (DFS backtracking and networkx-based enumeration, the
same dual-detector discipline used throughout this project since E0) and
cross-checked. Deduplicated by signature, retaining ≥1 concrete realizing
graph per signature. Results: experiments.md E19.

## 6. Compatibility search, refactored to the 3 exact types [see verifier/bridge_compatibility.py, experiments.md E20]

**Refactored per instruction: do not search arbitrary signature cliques.**
§2c proved every 2-cut is *exactly* one of 3 types, so the search now
only ever assembles candidates from those types:
1. **Type C** (2 bridges, no xy edge): {Bᵢ,Bⱼ} with aᵢ+aⱼ≥3, bᵢ+bⱼ≥3,
   neither bridge alone reaching both terminal degrees ≥3.
2. **Type B** (2 bridges sharing a degree-1 terminal, plus xy): {Bᵢ,Bⱼ}
   with aᵢ=aⱼ=1 (up to swapping x,y), edge xy included.
3. **Type A** (3 bridges sharing a degree-1 terminal, no xy edge):
   {B₁,B₂,B₃} with a₁=a₂=a₃=1 (up to swap).

**T5 is applied before cross-spectrum checks**: for Types A and B, every
candidate triple/pair is first tested against T5 (is some bridge
non-maximal while self-sum-clean? does the maximal one's own status
follow correctly?) before the (Λᵢ+Λⱼ)∩F=∅ compatibility test is even run
— pruning on a proved theorem before the more expensive sumset check,
matching the discipline requested. Bᵢ∼Bⱼ ⟺ (Λᵢ+Λⱼ)∩F=∅ remains the
underlying compatibility relation; families need Σdᵢ(x)≥3, Σdᵢ(y)≥3.

**Reporting, for the three-bridge (Type A) case specifically**, per each
candidate as requested: the ordered signature triple; which bridges have
a dyadic self-sum (Λᵢ+Λᵢ hits F); which are self-sum-clean; whether every
self-sum-clean bridge is lex-maximal (T5's corollary, checked directly on
the candidate, not just assumed); pairwise cross-spectrum compatibility;
and the admissible path pairs each Λᵢ contains (T2's own conclusion,
verified per bridge). Every surviving family is additionally saved and
independently re-verified as an actual assembled graph immediately upon
discovery (not just certified via the signature arithmetic alone).
Results: experiments.md E20.

**Integrity status.** `verifier/bridge_compatibility.py` now implements
only these three types. For Types A/B it evaluates T5 before computing
cross-spectra; Type C uses its exact T4 coverage conditions. Each candidate
record includes terminal degrees, (cᵢ,eᵢ), self-sum and internal cleanliness,
T5, cross-compatibility, and abstract/realizable provenance. Because E19's
real library is empty through n=7, nonvacuous synthetic fixtures exercise
all three accepted paths and their structural/T5/cross-sum rejection paths.

## 7. Abstract additive conditions are insufficient [PROVED — 2026-07-25, seventh pass; corrects the previous framing]

**The abstract program (searching signature triples under T2+T4+T5+
pairwise compatibility alone, previous pass) is retired as a route to
excluding Type A.** It cannot work, provably:

**Proposition (infinite equal-signature family) [PROVED].** *For
infinitely many integers m, setting Λ₁=Λ₂=Λ₃={m,m+1} (all three
signatures literally equal) satisfies (Λᵢ+Λⱼ)∩F=∅ for every i,j
(including i=j), provided neither 2m nor 2m+2 is a power of two.*

*Proof.* {m,m+1}+{m,m+1} = {2m, 2m+1, 2m+2} regardless of which two
(possibly equal) indices are summed — the sum is symmetric since all
three Λᵢ coincide. 2m+1 is odd, hence never in F={4,8,16,…} (all
even) automatically. So the sumset avoids F exactly when 2m∉F and
2m+2∉F. Since F is sparse (density 0), this holds for all but finitely
many m in any bounded range and for **infinitely many m overall** —
verified computationally (`verifier/three_bridge_search.py`,
experiments.md E21: 1,979 of the first 1,999 integers m qualify). ∎

**Consequence for T5.** With all three signatures literally *equal*
((c₁,e₁)=(c₂,e₂)=(c₃,e₃) trivially, by construction — nothing forces
them apart), T5's corollary ("a self-sum-clean bridge is lex-maximal")
imposes **no constraint at all**: every bridge ties for maximal, and a
tie is never a strict inequality, so T5's hypothesis (cᵢ,eᵢ)<_lex(cₖ,eₖ)
never fires. **T5 does not exclude the equal-signature family either.**

**Recorded conclusion.** T2, T4, T5, and pairwise sumset compatibility —
every currently-proved additive/combinatorial condition — are jointly
**insufficient** to exclude Type A abstractly: an explicit infinite
family of signatures survives all of them simultaneously. **The
remaining problem is realizability by degree-constrained two-terminal
graphs** — does some *actual graph* B realize a signature of this shape
(or any other surviving shape) while also satisfying T1 (B+xy
2-connected), internal min-degree-3, and internal F-cleanness? Per
instruction: **abstract survivor counts are no longer reported as if they
could establish the three-bridge exclusion** — §9 onward replaces the
abstract program with a direct construction/search over real two-terminal
graphs (T6's copy-gadget criterion and the bridge-closure generator).
E21 is corrected accordingly (experiments.md) to (a) support tied
signatures explicitly rather than only strict permutations, and (b) state
this insufficiency proposition rather than continue tallying finite-range
abstract counts as progress.

**Exact E21 reconciliation (regression only).** The old strict-order model
kept 318 triples; the corrected tied-signature model keeps 547. Their
difference is 229, consisting exactly of 203 triples with two self-sum-clean
bridges and 26 with three. These are precisely the cases requiring partial
or full maximum ties, which a strict permutation cannot encode. Neither
count is evidence toward resolving the conjecture; the mathematical result
is that the abstract conditions are insufficient. Canonical provenance:
`manifests/E21_manifest.json`.

**Candidate incompatibility causes**, still useful as a checklist for
*realizable* candidates once found (not for the abstract program, which
is now known insufficient on its own):
1. cross-sum (Λᵢ+Λⱼ) hits a power of two;
2. a bridge's own closure (Bᵢ+xy, or its qᵢ-fold gluing) is already a
   smaller counterexample (T1/§3's direct route);
3. terminal degrees fail to reach 3 when summed;
4. a balanced (§4) order case fails its derived edge inequality;
5. an internal cycle of some Bᵢ already hits a power of two;
6. a direct-edge/Mersenne conflict (§2's Λᵢ∩{2ᵏ−1}≠∅ when xy∈E(G)).

## 9. T6: the copy-gadget criterion [PROVED — 2026-07-25, seventh pass]

A **standalone, unconditional** construction — no minimal G assumed to
exist at all. Let B be a two-terminal graph, terminals x,y, with:
(i) q(B):=max(⌈3/d_B(x)⌉,⌈3/d_B(y)⌉) ∈{2,3}; (ii) every internal vertex
has degree ≥3; (iii) B has no power-of-two cycle; (iv) B+xy is
2-connected; (v) (Λ(B)+Λ(B))∩F=∅; **and (implicit, needed for
simplicity, stated explicitly here) xy∉E(B)** — B does not itself
contain the direct terminal edge (else gluing ≥2 copies would create
parallel x\*–y\* edges).

**T6.** *Gluing q(B) disjoint copies of B at both terminals (identifying
all copies' x's into x\*, all copies' y's into y\*) produces a genuine
Erdős–Gyárfás counterexample.*

*Proof.*
- **Simplicity [verified explicitly].** Distinct copies share only
  x\*,y\*; internal vertices are fresh per copy, so no edge is
  duplicated across copies — **except** a copy's own would-be xy edge,
  which is excluded by hypothesis (v)'s addendum above. So the glued
  graph is simple.
- **δ≥3 everywhere [verified explicitly].** Internal (copy-local)
  vertices: unchanged B-degree ≥3. deg(x\*)=q(B)·d_B(x) ≥
  d_B(x)·⌈3/d_B(x)⌉ ≥3 (standard ceiling inequality, using
  q(B)≥⌈3/d_B(x)⌉). Symmetrically deg(y\*)=q(B)·d_B(y)≥3.
- **Cycle classification, exhaustive [verified explicitly].** Every
  simple cycle either (a) lies entirely within one copy — inheriting
  B's own F-clean spectrum (hypothesis iii), safe — or (b) crosses
  between exactly 2 of the q(B) copies (a simple cycle visits x\*,y\*
  each at most once; copies share only these two vertices, so between
  consecutive visits it stays in one copy — same mechanism used
  throughout this project). Since every copy is a literal replica of
  B, case (b) always has length ℓ+ℓ′ for ℓ,ℓ′∈Λ(B) — **exactly**
  Λ(B)+Λ(B), regardless of which 2 of the q(B) copies are used. This
  is exhaustive: no other cycle type is possible.
- **F-cleanness.** Case (a) safe by (iii); case (b) safe by (v)
  ((Λ(B)+Λ(B))∩F=∅). **The glued graph has δ≥3 and no cycle of length in
  F: a genuine Erdős–Gyárfás counterexample, unconditionally.** ∎

**Type-A case, stated separately.** If d_B(x)=1, then
q(B)=max(⌈3/1⌉,·)=max(3,·)=**3** exactly (⌈3/1⌉=3 is already the largest
possible ceiling value, dominating regardless of d_B(y)) — matching Type
A's earlier characterization. **A single B satisfying T6's hypotheses
with d_B(x)=1 resolves the full Erdős–Gyárfás conjecture negatively**:
no minimal-counterexample context, no lexicographic comparison, no
master-minimality trick is needed — T6 is a direct, checkable
construction recipe.

## 10. The focused positive conjecture [CONJECTURAL]

> **Conjecture.** *Every Type-A bridge B (d_B(x)=1, B+xy 2-connected,
> every internal vertex degree ≥3, B internally power-of-two-cycle-free,
> xy∉E(B)) has (Λ(B)+Λ(B))∩F≠∅.*

This is the exact negation of T6's self-sum hypothesis, restricted to
Type A. The dichotomy is sharp: **if TRUE**, T6 can never fire on a
Type-A bridge, eliminating the entire "fully-balanced three-identical-
bridge" route (§4/§4b's k=3 case, and more generally any Type-A
construction attempt) from ever producing a survivor — a genuine
structural theorem toward 3-connectivity. **If FALSE** — i.e. some
Type-A bridge is self-sum-clean — T6 immediately manufactures a full
counterexample via the single-B construction above. **Labeled
CONJECTURAL**; not claimed either way here.

## 11. Linkage data: disjoint-pair spectra and the symmetric-difference identity [PROVED — 2026-07-25]

For a two-terminal graph B (terminals x,y), beyond the plain path
spectrum Λ(B)={|P| : P an x–y path}, define:
- **𝒟(B) := {(|P|,|Q|) : P,Q internally vertex-disjoint x–y paths}**
  (ordered or unordered pairs of genuinely disjoint paths);
- **ω(P,Q) := |E(P)∩E(Q)|** for any two x–y paths P,Q (not necessarily
  disjoint) — their shared-edge count.

**Every pair in 𝒟(B) gives a cycle of length |P|+|Q| [PROVED,
immediate].** P,Q share only the endpoints x,y (internal disjointness),
so P∪Q is a genuine simple cycle of that length.

**No pair in 𝒟(B) has dyadic sum [PROVED, immediate corollary].** Since
B has no power-of-two cycle (standing hypothesis throughout this
section), every cycle P∪Q from a disjoint pair has length ∉F: for every
(ℓ,ℓ′)∈𝒟(B), ℓ+ℓ′∉F.

**Every dyadic self-sum witness must involve overlapping paths [PROVED,
immediate contrapositive].** If ℓ,ℓ′∈Λ(B) with ℓ+ℓ′∈F, witnessed by
paths P (length ℓ), Q (length ℓ′): if P,Q were internally disjoint,
(ℓ,ℓ′)∈𝒟(B), contradicting the previous fact. So **P,Q share at least
one internal vertex** — not necessarily an edge (ω(P,Q) could still be
0 if they cross at a shared vertex via different edge pairs); the
precise overlap is measured next.

**The symmetric-difference identity [PROVED].** *For any two x–y paths
P,Q:*
[
|P|+|Q| = 2\,\omega(P,Q) + \sum_C |C|,
]
*where the sum ranges over the cycles in the edge-disjoint cycle
decomposition of the symmetric difference E(P)△E(Q).*

*Proof.* Standard inclusion–exclusion on edge sets: |E(P)|+|E(Q)| =
|E(P)∩E(Q)| + |E(P)∪E(Q)| = |E(P)∩E(Q)| + (|E(P)∩E(Q)|+|E(P)△E(Q)|) =
2ω(P,Q) + |E(P)△E(Q)|. It remains to show E(P)△E(Q) decomposes into
edge-disjoint cycles, i.e. every vertex has even degree in the symmetric
difference. At any vertex v, writing e₁=deg among P's edges at v,
e₂=deg among Q's edges at v, and c=edges at v common to both: degree in
the symmetric difference = e₁+e₂−2c ≡ e₁+e₂ (mod 2). For v∉{x,y}:
e₁∈{0,2} (v is either off P entirely, or P-internal with degree 2) and
likewise e₂∈{0,2} — sum always even. For v=x (symmetrically y): e₁=1
(x is P's own endpoint, path-degree 1) and e₂=1 (x is also Q's
endpoint) — sum=2, even. **Every vertex has even symmetric-difference
degree**, so E(P)△E(Q) is a disjoint union of edge-disjoint cycles
(standard fact: an all-even-degree graph decomposes into edge-disjoint
cycles). ∎

**Cross-checked with two independent implementations**
(`verifier/linkage_data.py`) — a direct combinatorial computation of
ω(P,Q) and the cycle decomposition of the symmetric difference via
connected-component/Eulerian-subgraph extraction, versus a brute-force
recomputation of |P|+|Q| from the path lengths directly — tested on every
bridge example generated in this pass (experiments.md E22).

## 12. Type-A suppression: the canonical representation [PROVED]

For a Type-A bridge B (d_B(x)=1), let u be x's unique neighbor and
K:=B−x (terminals u,y). Define **M(B) := {lengths of simple u–y paths in
K}**.

**Λ(B) = 1+M(B) [PROVED].** Every x–y path in B must begin with x's
unique edge (to u), then continue as a u–y path in K=B−x (which
automatically avoids x, since x is removed) — a bijection between x–y
paths of B and u–y paths of K, shifting length by exactly 1.

**Equivalence [PROVED, corollary].** (Λ(B)+Λ(B))∩F=∅ ⟺
((1+M(B))+(1+M(B)))∩F=∅ ⟺ (2+M(B)+M(B))∩F=∅ ⟺ for every m,m′∈M(B):
m+m′∉F−2={2ᵏ−2 : k≥2}, i.e.
[
(M(B)+M(B)) \cap \{2^k-2 : k\ge2\} = \varnothing.
]

This is the **canonical Type-A representation** used throughout §13–14:
K (one vertex smaller than B, terminals u,y) replaces B entirely, and
the target set shifts from F={4,8,16,…} to {2ᵏ−2}={2,6,14,30,…}.

## 13. Bridge-closure generation and near-gadget ranking [see verifier/bridge_closure_search.py, experiments.md E22]

**Generation, matching the one-pole search structure exactly.** J:=B+xy
is precisely a **one-pole graph** with root x (degree exactly 2, per
T6's Type-A case) — reusing the frozen one-pole search machinery
directly, relaxed only in that y is allowed degree ≥2 (not required ≥3,
since y is B's *other* terminal, not a generic internal vertex).
Generated via `geng -c -d2` (connected, min degree ≥2), filtering to:
exactly one degree-2 vertex x; every vertex other than x,y has degree
≥3; d_J(y)≥2. B is recovered by deleting the distinguished edge xy (one
of x's two incident edges — both choices of "which neighbor is y" are
tried). Deduplicated by edge-rooted isomorphism class (not just graph
isomorphism — the same graph with a different edge distinguished counts
separately, since B differs).

**Per B, computed and independently cross-checked (two
implementations):** internal power-of-two-cycle cleanliness; Λ(B); self-
sum dyadic hits (Λ(B)+Λ(B))∩F; the disjoint-pair spectrum 𝒟(B); the
minimum ω(P,Q) among any dyadic-self-sum-witnessing pair (§11); and the
SPQR node type at the divergence/reconvergence structure (via the same
`spqrtree` package used throughout this project). Results:
experiments.md E22.

**Ranking function.** h(B) := |(Λ(B)+Λ(B))∩F|. Priority order, exactly
as specified: (1) h(B)=0 — an outright T6 gadget (escalate and
independently re-verify **immediately**, not just log it); (2) h(B)=1;
(3) minimum overlap ω among the dyadic witnesses; (4) witness pairs
whose symmetric difference is a single cycle (the simplest possible
"near-miss" structure per §11's identity); (5) witnesses confined to
one rigid SPQR component. For every h(B)=1 bridge found, the exact
witness pair (P,Q) producing the unique dyadic hit is preserved (not
just its existence).

## 14. Toward T7: the minimum-overlap reduction [CONJECTURAL, searched not proved]

For a Type-A bridge, among all dyadic-self-sum-witnessing pairs (P,Q),
select one minimizing, in order: (1) ω(P,Q); (2) |V(P)∪V(Q)|; (3) the
number of cycles in the symmetric-difference decomposition (§11).

> **Target T7 (searched, not proved or disproved here).** *Such a
> minimum-overlap pair either (a) directly exhibits an internal
> power-of-two cycle (one of the symmetric-difference cycles itself hits
> F), or (b) identifies a proper two-terminal subpiece of B whose
> qᵢ-fold copy-closure is a lexicographically smaller gadget than B
> itself* (a T3/T5-style replacement, now applied recursively within a
> single bridge rather than across bridges of a 2-cut).

Searched for the smallest counterexample to T7 before any proof attempt,
per instruction — see experiments.md E22 for what the bridge-closure
generator actually finds at the sizes reached. **Status: neither proved
nor refuted this pass** — the generator's population at the sizes
reached (see E22) did not yet produce a genuine dyadic-self-sum witness
to test T7 against directly; the target is recorded precisely so it can
be tested the moment one appears, rather than left vague.

## 15. Scope note on the K4 census

Per instruction, the O7-filtered K4 census (one_pole.md, experiments.md
E16/E17) is retained as supporting data and **not extended this pass** —
the bridge framework here (§2's global cross-cycle identity across
*every* pair of bridges) subsumes the local, single-rigid-piece analysis
that the relaxed multi-R population lacked.

## 16. T8: minimal Type-A gadget criticality [PROVED — 2026-07-25]

Fix a Type-A copy gadget B with terminals x,y, chosen lexicographically
minimally by (|V(B)|,|E(B)|), and put J:=B+xy. Thus d_B(x)=1,
d_B(y)≥1, xy∉E(B), every vertex outside {x,y} has B-degree at least 3,
J is simple and 2-connected, B is internally F-clean, and
(Λ(B)+Λ(B))∩F=∅.

**Deletion monotonicity [PROVED].** For every e∈E(B), every cycle of B−e
was already a cycle of B, so deleting e cannot create an internal cycle.
Likewise every simple x–y path in B−e was already such a path in B:
Λ(B−e)⊆Λ(B). Consequently

[
  \Lambda(B-e)+\Lambda(B-e)\subseteq\Lambda(B)+\Lambda(B),
]

so edge deletion cannot create a new self-sum length, dyadic or otherwise.

**T8 [PROVED].** *For every e∈E(B), at least one of the following holds:*

1. *B−e violates the internal minimum-degree condition;*
2. *B−e violates a terminal-degree condition; or*
3. *J−e is not 2-connected.*

*Proof.* Suppose none holds. Edge deletion preserves simplicity and cannot
introduce xy; because e∈E(B), e≠xy and (B−e)+xy=J−e exactly. The assumed
degree statements give d_{B−e}(x)=1, d_{B−e}(y)≥1, and internal minimum
degree at least 3. The assumed 2-connectivity of J−e also implies B−e is
connected: deleting its edge xy from the 2-connected graph J−e cannot
disconnect it. Internal F-cleanness and self-sum F-cleanness follow from
the two monotonicity inclusions above. Thus B−e satisfies every T6/Type-A
hypothesis—including looplessness, absence of parallel edges, and exclusion
of xy—but has the same order and one fewer edge than B. This contradicts
the chosen lexicographic minimality. ∎

**Exact degree-critical locations.** The unique edge incident with x is
terminal-critical. An edge incident with an internal degree-3 vertex is
degree-critical at that vertex. An edge incident with y is terminal-critical
at y exactly when d_B(y)=1; if d_B(y)≥2 its deletion leaves positive
y-degree. In particular, if both endpoints are internal vertices of degree
at least 4, deleting the edge preserves every degree condition.

## 17. R1: deletion of a real R-skeleton edge [PROVED]

The convention is the reduced SPQR convention fixed in one_pole.md: an
R-skeleton is a simple 3-connected graph; each virtual edge uv represents
a pertinent graph P_{uv} meeting the rest only at u,v, and
P_{uv}+uv is 2-connected. The latter closure formulation matters: an S-piece
expansion can itself be a path even though its pole-edge closure is
2-connected.

**R1a (skeleton deletion) [PROVED].** *If R is a 3-connected skeleton and
e is an edge, R−e is 2-connected.* For any vertex w, if w is an endpoint of
e then (R−e)−w=R−w is connected. Otherwise R−w is 2-connected (3-connectivity
of R), hence has no bridge; deleting e leaves it connected. Thus deletion of
any vertex from R−e leaves a connected graph, exactly 2-connectivity. Notice
that no claim of preserved 3-connectivity is made. ∎

**R1b (expansion preservation) [PROVED].** *Replacing edges of a
2-connected skeleton H by two-terminal pertinent graphs P_{uv} satisfying
P_{uv}+uv 2-connected preserves 2-connectivity.*

Delete an arbitrary vertex z from the expanded graph.

- If z is internal to one expansion P_{uv}, every component of P_{uv}−z
  contains u or v; otherwise that component would remain isolated in
  (P_{uv}+uv)−z. The other expansions realize H−uv, which is connected
  because a 2-connected graph has no bridge, so u and v and all those
  components remain joined.
- If z is a skeleton vertex, H−z is connected. Every expansion not incident
  with z remains connected (remove its pole edge from a 2-connected closure),
  while an incident expansion P_{zv}−z is connected and attached at its other
  pole v because (P_{zv}+zv)−z=P_{zv}−z is connected.
- Deleting a pole is exactly the second case. Virtual edges incident with the
  deleted pole are not treated as surviving literal edges: their incident
  pertinent graphs remain attached through their other poles, as just shown.

Hence deletion of every vertex leaves the expanded graph connected. ∎

**R1 [PROVED].** Let e≠xy be a real edge in an R-node skeleton of J. Apply
R1a to that skeleton and then R1b to all its virtual-edge expansions (and
recursively to the rest of the reduced tree). The resulting graph is exactly
J−e, so J−e is 2-connected. ∎

**T8R [PROVED, T8+R1].** *Every real edge of B lying in an R-node skeleton
is incident with x, an internal degree-3 vertex, or y when d_B(y)=1.* The
closure edge xy is excluded because it is not in B. Indeed R1 rules out
T8's connectivity failure, so one of the exact degree failures must occur.

**Implementation hardening and finite audit.** The installed
`spqrtree==0.1.2` can be insertion-order-sensitive: on graph6 `GCpbeo` one
ordering labels a connectivity-2 skeleton R and falsely places edge 3–6
there, although a valid reduced decomposition places 3–6 in an S-node. On
`FCZv_` every tested package ordering leaves a crossing separation pair
unsplit. Therefore no theorem now trusts an R label without independently
checking 3-connectivity. `verifier/brute_spqr.py` supplies an exhaustive
split-pair decomposition for n≤9 and validates real-edge coverage, paired
virtual edges, tree topology, node types, and reduction. It validates all
538 biconnected graphs in NetworkX's graph atlas. On the 5,212 relaxed E22
closures, 64,596 genuine real R-skeleton B-edge instances satisfy R1 with
zero violations; 25,914 meet T8R's degree-critical incidence condition and
38,682 have an explicit noncritical deletion certificate, proving those
relaxed fixtures cannot be minimal gadgets.

## 18. Closure classes for the order-nine search [PROVED]

For J=B+xy:

- **SP-eligible:** d_B(y)=1. Both x and y have degree 2 in J. A
  series-parallel closure is possible (not guaranteed), so its complete
  reduced S/P decomposition must be recorded.
- **Rigid-forced:** d_B(y)≥2. Then x is the unique degree-2 vertex of J:
  y has J-degree at least 3 and every other vertex already has B-degree at
  least 3. If J were series-parallel, the proved partial-2-tree lemma in
  one_pole.md would give at least two degree-2 vertices, contradiction.
  Thus J has a K4 minor and its reduced SPQR tree contains an R-node.

The order-nine census keeps these classes separate. For the rigid-forced
class it records every R-node, every real R-edge with its T8R annotation,
and every skeleton-vertex degree profile.

## 19. Order-nine outcome [COMPUTATIONALLY VERIFIED]

The complete rooted oriented census is experiments.md E23b, with canonical
provenance in `manifests/E23_order9_manifest.json`. From 193,510 unlabeled
biconnected closures, 129,040 rooted oriented Type-A isomorphism classes
remain. They split into 4,214 SP-eligible and 124,826 rigid-forced closures;
none of the SP-eligible class is actually series-parallel.

Every one of the 129,040 bridges already contains an internal C4 or C8:
5,980 have only C4 among those lengths, one has only C8, and 123,059 have
both. Thus no bridge reaches the self-sum/overlap stage, no three-copy lift is
power-cycle-free, and T7 remains empirically uninstantiated. This is a
complete order-9 negative computation, not a general nonexistence theorem.
