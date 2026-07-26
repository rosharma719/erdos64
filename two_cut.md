# two_cut.md — toward 3-connectivity of a minimal counterexample

**Status as of 2026-07-25 (fifth redirection pass).** New main target,
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

**k=3 (three bridges evade simultaneously) [PROVED, forces exact
equality in cᵢ, an inequality in eᵢ].** Each of the 3 needs cᵢ≥N/3; if
any had qᵢ=2 its requirement would be cᵢ≥N/2, and combined with the
other two's ≥N/3 each the sum would exceed N — impossible since these 3
alone must fit within Σcᵢ=N (they may be the *only* bridges, or there
could be room for more only if the sum is strictly less than N — but
qᵢ=2 for even one of the three already forces N/2+N/3+N/3=7N/6>N,
impossible). So **all 3 evading bridges have qᵢ=3 exactly**, and since
each individually needs cᵢ≥N/3 while collectively Σ(these 3)≤N, equality
is forced: **cᵢ=N/3 for all 3** (requires 3∣N), and **t=3 exactly** (no
room for a 4th nontrivial bridge — the three already exhaust N). This is
the order-tied case; **edge inequalities** come from additionally
requiring the edge part not to break the tie either way (survival, not
forced by T3): writing eᵢ:=|E(Bᵢ)|, |E(G)|=e₁+e₂+e₃+[xy∈E(G)]. Requiring
m'ᵢ=3eᵢ≥|E(G)| for i=1,2,3 and summing gives 3Σeᵢ≥3Σeᵢ+3[xy], forcing
**[xy∈E(G)] = 0** (the direct edge cannot be present), and then the
individual conditions reduce to **2eᵢ ≥ eⱼ+eₖ** for every permutation
{i,j,k}={1,2,3} — a genuine "near-balanced" inequality (satisfied by
e₁=e₂=e₃, but not forced to exact equality by this route alone; e.g.
e₁=e₂=e₃=e is one solution family, not the only algebraically consistent
one, though realizability by actual F-clean bridges may narrow this
further — left open).

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

**Summary — the finite list of *fully forced* balanced configurations:**
1. **t=2, q₁=q₂=2, c₁=c₂=N/2, xy∉E(G), e₁=e₂** (exact, both order and
   edges tied — the direct S5 analogue).
2. **t=3, q₁=q₂=q₃=3, c₁=c₂=c₃=N/3, xy∉E(G), 2eᵢ≥eⱼ+eₖ for all
   permutations** (order tied exactly; edges constrained but not forced
   to exact equality by this argument alone).
Plus a non-exhaustively-classified family of partial (k≤2, not both
qᵢ=2) evasions that remain open. **2-cuts are not claimed impossible —**
every one of these cases, plus the open partial-evasion family, needs
further treatment (§6–7) before any such claim could be made.

## 5. Bridge-signature library [see verifier/bridge_signature.py, experiments.md E19]

Σ(B) = (|V(B)|−2, |E(B)|, d_B(x), d_B(y), Λ(B), C(B)) for two-terminal
graphs B with: B+xy 2-connected (T1's requirement); internal min degree
≥3; internal cycles avoiding F. Path spectra Λ(B) and cycle spectra C(B)
are computed with two independent implementations (DFS backtracking and
networkx-based enumeration, the same dual-detector discipline used
throughout this project since E0) and cross-checked. Deduplicated by
signature, retaining ≥1 concrete realizing graph per signature. Results:
experiments.md E19.

## 6. Compatibility search [see verifier/bridge_compatibility.py, experiments.md E20]

Bᵢ∼Bⱼ ⟺ (Λᵢ+Λⱼ)∩F=∅. Search for compatible families with
Σdᵢ(x)≥3, Σdᵢ(y)≥3 (the assembled x,y degree requirement). T2, T3, and
§4's balanced-case constraints are applied **before** the compatibility
search (pruning candidates that already fail a proved theorem, rather
than discovering the failure only after full assembly) — every surviving
family is additionally saved and independently re-verified as an actual
assembled graph immediately upon discovery (not just certified via the
signature arithmetic alone). Results: experiments.md E20.

## 7. Toward the 3-connectivity target [CONJECTURAL]

**Target (kept CONJECTURAL, not claimed):** *Every lexicographically
minimal Erdős–Gyárfás counterexample is 3-connected.*

Candidate incompatibility causes, clustered for a future finite-case
theorem (see experiments.md E20 for which causes actually fire on the
searched population):
1. cross-sum (Λᵢ+Λⱼ) hits a power of two;
2. a bridge's own closure (Bᵢ+xy, or its qᵢ-fold gluing) is already a
   smaller counterexample (T1/§3's direct route, not needing
   compatibility at all);
3. terminal degrees fail to reach 3 when summed;
4. a balanced (§4) order case fails its derived edge inequality;
5. an internal cycle of some Bᵢ already hits a power of two (ruled out
   automatically by construction if drawn from the library of §5, but a
   live failure mode for arbitrarily-assembled candidates);
6. a direct-edge/Mersenne conflict (§2's Λᵢ∩{2ᵏ−1}≠∅ when xy∈E(G)).

No finite theorem excluding every compatible family is established here.
This is the honest state of the target: a conjecture with a precise
combinatorial decomposition (§1–4) and a search infrastructure (§5–6)
built to test it, not a proof.

## 8. Scope note on the K4 census

Per instruction, the O7-filtered K4 census (one_pole.md, experiments.md
E16/E17) is retained as supporting data and **not extended this pass** —
the bridge framework here (§2's global cross-cycle identity across
*every* pair of bridges) subsumes the local, single-rigid-piece analysis
that the relaxed multi-R population lacked.
