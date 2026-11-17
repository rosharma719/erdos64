# Research pass XI: spectral isolation and independent-switch amplification

**Date:** 16 November 2026. **Status:** Proven elementary conditional lemmas, independent graph-level verification, and a concrete two-ear rooted certificate in the Petersen graph. **No proof of Erdős–Gyárfás or of a universal connectivity-to-switching theorem is claimed.** The results here should be considered a proposed research framework, not publication-level novelty without literature comparison.

## Why a change of focus is justified

Pass X derived an exact boundary-linkage signature and a sharp additive-density certificate. It is tempting to prove that cyclic connectivity automatically makes individual terminal-path spectra dense. That ambition is much stronger than what the available combinatorial evidence supports. Even established minimum-degree-three results only guarantee some close cycle lengths, e.g. the Bondy–Vince difference-one-or-two result discussed in Li–Pan–Shi (2026); stronger cycle-length arithmetic-progression theorems typically demand stronger minimum-degree hypotheses (Bai–Grzesik–Li–Prorok, JCTB 2026).

Two steps offer a more precise target: prove why boundary path *sets cannot generally be compressed*, and isolate a **graph-theoretic mechanism** that does make spectra rich. Both are exact.

## Theorem 1: dyadic spectral isolation

Let `X` be a finite set of nonnegative integers, and let `x` be any nonnegative integer. For sufficiently large powers of two `q=2^k`, the integer `c=q-x` is positive and satisfies

\[
\{\ell\in X: c+\ell\text{ is a power of two of at least 4}\}=X\cap\{x\}.
\]

**Proof.** Choose `q` with `q>2\max_{\ell\in X}|\ell-x|`, and `q>x+3`. If `\ell=x` then `c+\ell=q`. If `\ell<x`, then `q/2<q+\ell-x<q`; if `\ell>x`, then `q<q+\ell-x<2q`. Neither open interval contains a power of two. QED.

**Consequence (two-terminal boundary optimality).** Let `P` and `P'` be two finite graphs with distinct designated terminals `s,t` (their internal edge sets need not be equal), neither containing a power-of-two cycle. Let `X(P)` and `X(P')` be the sets of lengths of simple `s-t` paths. If `X(P) != X(P')`, then a **single simple path context**, connected by two new cut edges to `s,t`, distinguishes dyadic-cycle existence in the two glued graphs.

**Proof.** Pick `x` in the symmetric difference, and let `X=X(P)\cup X(P')`. Choose `q` as in the isolation lemma, with a context path of length `m=q-x-2>=1`. Every new cycle traverses exactly two cut edges and one terminal path of the pole, so its length is `m+2+\ell=q+(\ell-x)`. By the lemma, a new dyadic cycle exists precisely in the pole whose spectrum contains `x`. Neither pole has an internal dyadic cycle, and the context is acyclic. QED.

Thus, **any universally correct, context-independent classifier for dyadic-cycle existence, even restricted to dyadic-free two-terminal poles, must distinguish different terminal path-length sets.** In particular, no *fixed finite-state* classifier exists without imposing a size bound or further structural restrictions: single-path poles of infinitely many different lengths already require infinitely many distinguishable states. This does not rule out bounded-size dynamic programming or useful sufficient invariants. It says that a universal **lossless** bounded signature is impossible.

An explicit graph check uses two theta poles with terminal spectra `{2,7}` and `{2,3,7}`. Their internal cycles have lengths `9` and `{5,9,10}` respectively, all nondyadic. The same path context isolates the length `3`, forcing an 8-cycle in the second glued graph and none in the first.

## Theorem 2: independent-switch path-spectrum amplification

Let `P` be a simple `s-t` path of length `a`, and let `R_1,...,R_t` be pairwise interior-disjoint *bypasses* replacing respective pairwise edge-disjoint subpaths of `P`, whose interiors avoid `P` and each other. Consecutive replaced subpaths may share an endpoint, but must not overlap in an edge or interior vertex. Let `d_i` be the number of edges in bypass `R_i` minus the number in the replaced subpath. Assume `d_i>0`.

Each subset `I` of bypasses produces a simple `s-t` path of length

\[
 a+\sum_{i\in I} d_i.
\]

This is a **constructive inclusion** in the pole's terminal spectrum; it does not assert that the pole has no additional paths.

Let `g=gcd(d_1,...,d_t)` and write the sorted normalized increments as `b_1<=...<=b_t`, `b_i=d_i/g`. If

\[
b_1=1,\qquad b_j\le 1+\sum_{i<j}b_i \quad (2\le j\le t),
\]

then the terminal spectrum contains **every** length in

\[
 \{a,a+g,a+2g,\ldots,a+\sum_i d_i\}.
\]

**Proof.** The subset sums of `b_1` are `{0,1}`. If the first `j-1` weights cover all integers from `0` to `S`, then adding `b_j<=S+1` gives intervals `[0,S]` and `[b_j,b_j+S]` with no gap. Induct. Multiplying by `g` and adding `a` gives the claim. QED.

**Gluing corollary.** Suppose the pole is joined across a cut in a compatible state to another pole that has *one* matching linkage of total length `b`, and the cut uses `h` edges. Assume the local bypasses preserve the required vertex-disjoint linkage. The glued graph contains cycles of every length in

\[
 L+g\{0,1,\ldots,(\sum d_i)/g\},\qquad L=h+a+b.
\]

If that progression contains a power of two, the glued graph has a dyadic cycle. This requires a rich signature on **only one side** of the cut; the other side can have a singleton linkage spectrum.

A particularly simple case is `g=2`, `L` even, and `L+\sum d_i >= 2^{\lceil \log_2 L\rceil}`: the progression reaches the next power of two without a parity obstruction.

**Arithmetic obstruction.** No amount of progression length alone suffices if its residue class excludes every power of two. For example, `L=6`, `g=3`, and arbitrarily many increments equal to `3` produce all multiples of three in an expanding interval, and never a dyadic length. A graph-theoretic theorem needs both flexibility and *modular alignment*. This purely arithmetic example is not asserted to arise in a minimum-degree-three graph.

**Important caveats.** Connectivity by itself does not yet supply the bypasses, their mutual compatibility, a complete weight sequence, or the required modular alignment. These are the missing structural claims. The proof is an elementary subset-sum lemma; novelty would have to come from proving a robust graph-theoretic source of such independent switches.

## Theorem 3: rooted switching polynomials (no completeness assumption)

For a cycle `C` of length `L` equipped with genuinely independent bypasses of *signed* increments `d_1,...,d_t` (positive or negative), form the Laurent polynomial

\[
F_C(z)=z^L\prod_{i=1}^{t}(1+z^{d_i}).
\]

The coefficient of `z^m` is exactly the number of bypass selections in this switching cube whose resulting simple cycle has length `m`. In particular, if the coefficient at a power of two is positive, there is a dyadic cycle. **Proof:** expand the product; every monomial corresponds to a subset of switches, and independence guarantees that its combination remains one simple cycle. The exponent is precisely its edge count. QED.

The same product handles **root avoidance**. A root in the interior of a replaced base arc requires that switch to be selected (replace `1+z^{d_i}` by `z^{d_i}`); a root in a bypass interior requires that switch to be omitted (replace its factor by `1`). If a root lies on a base segment that can never be removed, or is a switch endpoint, the rooted polynomial is zero. Otherwise, the resulting polynomial counts exactly the root-avoiding cycles in this switching family. The conditions assume disjoint switch supports as above; an arbitrary collection of overlapping bypasses need not factor.

This is a factored version of the Boolean-semiring boundary signature from pass X, with nonnegative integer coefficients. It captures *signed, irregular* subsets without requiring their lengths to form an arithmetic progression. The complete-sequence theorem is a special, easy-to-check sufficient condition.

**Quantifier warning:** one dyadic coefficient proves the existence of a cycle; failure to find a coefficient in one chosen switching cube says nothing about all other cycles in the graph.

## The need for two ears: an exact Petersen certificate

Use the standard NetworkX Petersen labeling. The base six-cycle is

`C = (0,1,2,3,8,5,0)`.

Two external bypass paths replace disjoint subpaths of the base:

* `0-1` is replaced by `0-4-9-6-1` (increment `+3`).
* `2-3-8-5` is replaced by `2-7-5` (increment `-1`).

The four length choices are **6, 9, 5, 8**. The final cycle is

`(0,4,9,6,1,2,7,5,0)`,

which has length 8 and avoids the root vertex 3. Neither single change produces a dyadic cycle. These signed increments are **not** a complete positive sequence, so the general complete-sequence criterion is only sufficient, not necessary. The exact subset-sum mechanism is more general.

This certifies a specific two-ear repair configuration *in a genuine cyclically four-edge-connected cubic graph*. The finite example does not prove the universal two-ear conjecture.

The rooted switching polynomial for root `3` is exactly `z^5+z^8`: the second bypass must be used to eliminate vertex `3`, while the first remains optional.

**Falsification check for a stronger but tempting induction lemma.** The included independent Petersen scan traverses every simple cycle, both orientations and all rotations, then checks every strictly independent pair of external bypasses with vertex-disjoint base-arc supports and disjoint bypass interiors. None has positive absolute increments satisfying the normalized complete-sequence condition. Thus **the requirement that such a complete pair always exist is already false in a cyclically four-edge-connected cubic graph** (within this precisely defined strict ear model). This does not rule out overlapping, nested, or dependent switches; the signed pair above is itself enough to force 8. The more promising object is the *root-conditioned polynomial support*, with completeness only as one sufficient route to a nonzero dyadic coefficient.



## A width-based hypothesis is provably too weak

Start with a 10-cycle and attach two independent external bypasses replacing disjoint arcs of lengths `2,2` with lengths `4,10`. Their increments are `2,8`. Individual local cycles have lengths `6` and `12`. The resulting graph's complete cycle-length set, independently enumerated, is

`{6,10,12,18,20}`.

The attainable large-cycle interval spans 16, but **no** cycle has power-of-two length. The graph has vertices of degree two; this is a counterexample to unconditional endpoint-width reasoning, **not** to the Erdős–Gyárfás conjecture or to a high-connectivity expansion statement.

By contrast, three disjoint `2->4` bypasses attached to a 10-cycle yield lengths `10,12,14,16`, while the local cycles still have nondyadic length 6. Their combination forces the 16-cycle.

## Exactly what remains open

A plausible next theorem would assert that every root-critical cyclically four-edge-connected cubic graph admits some **boundary-compatible rooted switching family whose factored polynomial has a positive dyadic coefficient**; or else an explicitly characterized obstruction whose edge bridges necessarily repair the defect by a different mechanism. Requiring a complete arithmetic progression is demonstrably too strong in the strict external-ear model.

That statement is deliberately **not** claimed here. It may be false. A credible research program would:

1. Test quantitative switch-packing bounds against known sparse-cycle 24- and 78-vertex constructions, looking for sharp counterexamples.
2. Seek an ear-exchange lemma that turns cyclic four-edge-connectivity into two or more compatible bypasses, and then a separate *length*-control lemma. The first does not imply the second.
3. Use the exact boundary signature from pass X to glue the resulting switch-supported progressions across 3- and 4-edge cuts.

This is more targeted than asking for arbitrary spectrum density: it identifies a concrete **mechanism** whose absence a hypothetical counterexample would have to enforce throughout its connected structure.

## Reproducibility

Run `python -m pytest -q tracks/2026-11-halving/scripts/test_spectral_switching.py` in the patched repository. The tests independently construct the graphs, enumerate simple cycles, check terminal path spectra, validate reconstructed switch cycles, and exercise the integer lemmas against explicit subset-sum enumeration. All assertions are finite; the preceding proofs establish the general theorems.

## Literature for context

* Li, Pan, Shi (2026), *A note on two cycles of consecutive even lengths in graphs*, Discrete Mathematics 349:3: established classical Bondy–Vince two-close-cycle result discussed in abstract, https://doi.org/10.1016/j.disc.2025.114820.
* Bai, Grzesik, Li, Prorok (2026), *Cycle lengths in graphs of given minimum degree*, JCTB 180:111–150, https://doi.org/10.1016/j.jctb.2026.06.003.
* Garcia (2026), *Small graphs without power-of-two cycles*, https://arxiv.org/abs/2609.04686.
