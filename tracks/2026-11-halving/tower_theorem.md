# Pass XII — Triangle-tower theorem

**Status: PROVED** (self-contained inductive argument; finite cases checked separately by two implementations).
**Scope:** the recursively defined triangle-built family only. Nothing in this proof classifies arbitrary clean 3-poles.

## Definitions

A *three-port network* has three labelled dangling half-edges. The **identity** `I` is one vertex carrying three half-edges. It is an auxiliary network, **not** a graph with three distinct degree-2 vertices and hence **not a clean 3-pole**.

A *triangle composition* `Δ(A,B,C)` attaches the second and third half-edges of each child to the corresponding half-edges of the other two children to form the three connecting edges of a triangle. One half-edge of each child remains exterior. The resulting graph has three external half-edges. Every non-identity composed network has three *distinct* degree-2 vertices carrying those half-edges; all its other vertices have degree 3. Its order is the sum of the child orders.

A network is **clean** when its underlying internal graph contains no simple cycle of length `2^k` (`k ≥ 2`; only 4,8,16,... matter for simple graphs). A clean composed network has clean children because each child is an induced subgraph up to external port edges.

A terminal-to-terminal path has length measured in *internal edges*, so the path between two ports of `I` has length zero. When a component is represented by graph6, its terminals are *exactly its internal degree-2 vertices*. Never transplant numeric terminal labels from separately serialized `make_gadget()` objects.

## Three elementary lemmas

**PROVED — Cycle decomposition.** Every cycle in `Δ(A,B,C)` is either internal to one child or traverses *all three* connecting edges, using one simple path between the two connecting ports of each child. Indeed, a simple cycle crossing the boundary of any one child must use both incident connecting edges; the same argument propagates to all three. Consequently its crossing-cycle length set is exactly

`3 + X_A + X_B + X_C`,

where `X_i` is the internal path-length set between the two connecting ports of child `i` and `+` denotes the Minkowski sum of sets of integers.

**PROVED — Hamiltonian terminal span.** Every triangle-built network of order `N`, clean or not, has a simple path of length `N−1` between *each pair of distinct external half-edges*, starting and ending at their supporting vertices (the identity case has length zero). Induct on the construction. Given external ports on children `A` and `B`, travel from the first outer port through `A`, across the triangle edge to `C`, through `C`, across the triangle edge to `B`, and through `B` to the second outer port. The inductively available Hamiltonian terminal paths within the disjoint children cover all `N` vertices. This establishes a Hamiltonian path between every terminal pair and hence an upper path-length endpoint of exactly `N−1`.

**PROVED — Interval addition.** If each child connecting-port path set is a complete integer interval `[a_i,b_i]`, then the crossing-cycle set is the complete integer interval `[3+Σa_i,3+Σb_i]`. By Hamiltonian terminal span, `b_i=n_i−1`; therefore the upper endpoint equals `N=n_A+n_B+n_C`.

The interval hypothesis is essential. For example, the unclean five-vertex composition `Δ(I,I,T)` has an external terminal-pair path set `{1,3,4}` with a gap. Thus it would be false to assert complete intervals for *all* triangle-built networks. The induction below asserts them **simultaneously with cleanness**, and never applies them to an unclean child.

## Profiles of the four possible clean children

The induction maintains the following full spectra; the port-pair order is immaterial:

| Symbol | Order | Three terminal-pair path sets | Allowed connecting-port minimum `a` |
|---|---:|---|---|
| `I` | 1 | `{0}`, `{0}`, `{0}` | 0 |
| `T` | 3 | `[1,2]`, `[1,2]`, `[1,2]` | 1 |
| `S` | 7 | `[2,6]`, `[2,6]`, `[3,6]` | 2 or 3 |
| `H` | 15 | `[3,14]`, `[3,14]`, `[5,14]` | 3 or 5 |

These are obtained directly from the two possible routes between outer terminals: the direct connecting edge between their children and the route passing through the third child. Each route contributes a sum of child intervals with 1 or 2 connecting edges. For the three surviving compositions below the two resulting integer intervals overlap or abut, giving exactly the indicated profiles. The standalone NetworkX and independent C bit-mask verifiers reproduce these explicit finite spectra, including paths of length `n−1`.

## The induction and complete case table

**THEOREM (PROVED).** A clean triangle-built network is isomorphic, with its three outer half-edges preserved as an unordered set, to exactly one of `I` (order 1), `T=Δ(I,I,I)` (order 3), `S=Δ(I,T,T)` (order 7), or `H=Δ(I,S,S)` (order 15), where in the last composition both `S` pieces use their unique port-pair of minimum length 3 as their connecting ports. Each of the latter three is clean and has the profiles above.

*Proof.* Proceed by strong induction on network order. Every child of a clean composition is clean, so by induction each is one of `I,T,S,H`. The exact crossing-cycle window for any choice of connecting ports is

`[L,N]`, `L=3+a_A+a_B+a_C`, `N=n_A+n_B+n_C`.

The finite enumeration of **all 20** unordered three-child multisets yields the following table. In every row marked `excluded`, **every** possible connecting-port orientation produces a window containing at least one of 4,8,16,32. The symbolic verifier independently reproduces this table in Python and C.

| Children | Order N | Clean central window possible? |
|---|---:|---|
| I,I,I | 3 | yes, `[3,3]` |
| I,I,T | 5 | excluded (4) |
| I,I,S | 9 | excluded (8) |
| I,I,H | 17 | excluded (8 or 16) |
| I,T,T | 7 | yes, `[5,7]` |
| I,T,S | 11 | excluded (8) |
| I,T,H | 19 | excluded (8 or 16) |
| I,S,S | 15 | **only** the pair of minima `(3,3)`, giving `[9,15]` |
| I,S,H | 23 | excluded (8 or 16) |
| I,H,H | 31 | excluded (16) |
| T,T,T | 9 | excluded (8) |
| T,T,S | 13 | excluded (8) |
| T,T,H | 21 | excluded (8 or 16) |
| T,S,S | 17 | excluded (8 or 16) |
| T,S,H | 25 | excluded (16) |
| T,H,H | 33 | excluded (16) |
| S,S,S | 21 | excluded (16) |
| S,S,H | 29 | excluded (16) |
| S,H,H | 37 | excluded (16 or 32) |
| H,H,H | 45 | excluded (16 or 32) |

In the three surviving rows, the children have no internal forbidden cycle by induction, and the displayed central window avoids powers of two. The two nontrivial constructions have symmetric pairs of identical children, and their connecting-port restrictions determine their terminal-marked isomorphism class uniquely. Computing the two possible outer-terminal routes gives the full profiles tabulated above. This also proves the interval property required by the next induction step. ∎

**PROVED — A stronger `K4`-root rule with a non-tower letter.** The clean uniform seven-vertex gadget `U` has order 7 and all three connecting-port path sets `[2,6]`. If the three vertices of `K4−r` are independently replaced by members of `{I,T,S,U,H}`, the same window test now has 35 unordered triples. The only clean outcomes are still `III`, `ITT`, and `ISS` (using the special `S` orientation). Every triple containing `U` contains a forbidden crossing cycle. This is a useful extension for a conditional prime-decomposition reduction; it does **not** assert that `U` is triangle-built.

**PROVED — Identification of `H`.** The explicit `H=Δ(I,S,S)` graph has the same adjacency as the Exoo 15-vertex gadget under the bijection supplied by `h15_isomorphism_certificate.json`. The bijection sends the three degree-2 vertices of the constructed `H` to the three degree-2 vertices of the reference graph. This is a finite explicit isomorphism certificate, not an inference from an untrusted port ordering.

## What is and is not needed from the proposed proof line

- **PROVED:** The Hamiltonian span lemma is unconditional, even for unclean recursive pieces.
- **PROVED:** The interval lemma holds for *clean* triangle-built pieces, via the simultaneous induction above. It fails for some unclean ones (already at five vertices).
- **PROVED:** On the four clean types, the maximum shortest terminal-path lengths are `0,1,3,5` for orders `1,3,7,15`, respectively. No vague logarithmic growth assertion is required: the finite closure argument already classifies every clean order.
- **PROVED:** The only use of the triangle's `{1,2}` interval, rather than generic prime-base structure, is the availability of an uninterrupted set of lengths for each connecting-port path, propagated by interval addition into `[L,N]`. On a generic prime base, paths can have gaps and the union of different base cycles need not be an interval.
- **COMPUTED:** The submitted verifiers check all four finite clean profiles, explicit unclean counterexamples at orders 5 and 9, all 20 tower type triples, and all 35 `K4` triples including `U`. They do **not** enumerate every distinct *unclean* recursive structure through order 31; the proof does not rely on such an enumeration, and the earliest explicit counterexample already invalidates an unconditional interval lemma.

**OPEN:** Conjecture T for *arbitrary* clean 3-poles. The present theorem covers only the triangle-built family and a `K4` composition extension with the `U` atom.
