# Sublinear expanders and the Erdős–Gyárfás conjecture: a working brief

Date: 2026-11-16. Tags: [SRC: x] = read in source x; [INF] = my inference, not checked against a source.
Source keys: LM = Liu–Montgomery; LET = Letzter survey; MON = Montgomery survey; SV = Sudakov–Verstraëte; FK = Friedman–Krivelevich; DD = Ducoffe–Dumitru; GAR = Garcia; HJYY = Hou–Jin–Yang–Yang; REPO = project files.

## Summary (5 lines)

1. Liu–Montgomery do not aim at powers of two: they prove every even length in a window [polylog n, n/polylog n] occurs in a bipartite sublinear expander, and that window is multiplicatively long, so it contains a power of two.
2. Exact lengths come from "adjusters": chains of short cycles, each offering two routes differing by 2, joined by short paths that the expander supplies even after deleting used vertices.
3. Large degree is consumed mainly by robust small-set expansion (a vertex must keep about d/2 neighbours after deletions); no explicit constant exists, and the stated parameters force it above roughly 10^35.
4. At minimum degree 3 the method fails locally, not globally; moreover a minimal counterexample has no proper subgraph of minimum degree 3, so "pass to an expander subgraph" always creates degree-2 vertices, and 3-subdivisions show degree-2 vertices are fatal.
5. Most promising: Hamiltonian cubic graphs via chord switching and subset sums, and 3-connected linear expanders via Friedman–Krivelevich plus O(1/α) adjusters. Nothing here suggests the conjecture is close to solved.

## 1. How Liu–Montgomery force a power-of-two length

**Expander definition.** A graph is an (ε1, k)-expander if every vertex set X with k/2 ≤ |X| ≤ n/2 has |N(X)| ≥ ε(|X|)·|X|, where ε(x) = ε1 / log²(15x/k) [SRC: LM Def. 2.1; LET Def. 2.2]. The rate decays with |X|, and sets below k/2 get no guarantee [SRC: LET, MON]. For constant-size sets the bound only says "at least one neighbour" [SRC: MON].

**Passing to an expander.** Komlós–Szemerédi: every graph G has an expander subgraph H with d(H) ≥ d(G)/2 and δ(H) ≥ d(H)/2 [SRC: LM Thm 2.2]; the loss in average degree can be made a factor 1−δ [SRC: LET Rem. 2.4; MON Thm 3.2]. The proof repeatedly deletes low-degree vertices and non-expanding sets [SRC: MON]. Taking a bipartite subgraph costs another factor 2, so average degree 8d yields a bipartite (ε1, ε2·d)-expander with minimum degree d [SRC: LM Cor. 2.5]. H may be far smaller than G [SRC: MON].

**Core theorem.** In a bipartite n-vertex (ε1, ε2 d)-expander H with δ(H) ≥ d and no 2-subdivided clique TK^(2)_{d/2}, any two vertices x, y are joined by a path of every length ℓ in [log^7 n, n/log^12 n] of the right parity [SRC: LM Thm 2.7]. Apply it to an edge xy to get every even cycle length in that range. If H does contain TK^(2)_{d/2}, every even length from 6 to about d appears directly [SRC: LM].

**Adjusters.** A simple adjuster is a cycle C of length 2ℓ with two vertices v1, v2 at distance ℓ−1 on C, so C gives v1–v2 paths of lengths ℓ−1 and ℓ+1, plus two disjoint "ends" F1, F2: connected sets of size D = polylog n grown around v1 and v2 with radius O(log³ n) [SRC: LM §2.4, Def. 4.1]. The ends exist so that later paths can attach to the adjuster even after many vertices are forbidden. Chaining r simple adjusters by short paths gives a (D, m, r)-adjuster: a set A of at most 10mr vertices containing v1–v2 paths of lengths ℓ0, ℓ0+2, …, ℓ0+2r [SRC: LM Def. 4.1, Lemma 4.7]. Here m = Θ(log³ n) is the expander's connection length.

**Building one adjuster.** Take a shortest cycle C; minimum degree gives |C| ≤ 2 log n / log(d−1), and bipartiteness makes it even [SRC: LM Lemma 4.2]. The hard part is doing this while avoiding a forbidden set U: they build many well-separated adjusters and show one must still expand in G−U, using TK^(2)-freeness to bound how many vertices send many edges into U [SRC: LM Lemma 4.3].

**Tuning.** Build an adjuster with r ≈ 22m. Connect x and y to its two ends by disjoint paths, avoiding A, of total length within 22m below the target. The deficit is even by the parity hypothesis, equals 2i with i ≤ 11m, and the adjuster supplies exactly that [SRC: LM Lemma 4.8].

**Why this beats additive windows.** [INF] Classical degree-d results give about d consecutive lengths starting at an uncontrolled point L, a window [L, L+d] with ratio near 1. LM's window has both ends tied to the same parameter n = |H|: lower end polylog n (the diameter cost), upper end n/polylog n. Its ratio tends to infinity, so any sequence with σ_{i+1} ≤ exp(σ_i^{1/10}) must hit it [SRC: LM Cor. 1.3]. Multiplicative sparsity is therefore not the obstacle at high degree; faster-growing sequences are genuinely avoidable [SRC: LM; SV §4]. For powers of two one only needs all even lengths in some [L, 2L].

## 2. Where large average degree is consumed

1. **Reduction to a bipartite expander with large minimum degree**: factor 8 [SRC: LM Cor. 2.5].
2. **Expansion threshold k = ε2·d.** Minimum degree d puts every neighbourhood above the threshold at once, so single vertices expand [SRC: LM Lemmas 3.7, 3.11; MON].
3. **Robustness.** Bounds like δ(G) − |forbidden| ≥ d/2 are used repeatedly to grow ends of size up to log^{5k} n around a vertex while avoiding earlier structure [SRC: LM Lemmas 3.7, 3.11, 4.3]. This is the step with no degree-3 analogue [INF].
4. **Dense/sparse dichotomy.** Vertices of degree ≥ 200mD are set aside; TK^(2)_{d/2}-freeness limits them [SRC: LM Lemma 4.3, Prop. 3.16].
5. **Short cycle.** Length ≤ 2 log n/log(d−1); this survives at d = 3 [SRC: LM for the bound; INF for the remark].
6. **Asymptotic slack.** n ≥ d ≥ d0 is needed for many polylog inequalities [SRC: LM].

**Is d explicit?** No. LM give only "d0 large"; the surveys give no value; Garcia calls the constant "uncomputed" [SRC: LM, LET, MON, GAR]. I found no paper estimating or improving it. [INF] Lower bounds from the stated parameters alone, natural logs: the interval [log^8 ℓ, ℓ] with ℓ = d/(10 log^12 d) contains a power of two only once d is around e^82 ≈ 10^35.7. Lemma 3.2 asks for sets of size m^{400k} with m ≥ 16 log³ n; if k = 10 there (I did not trace this), n must exceed about exp(1.5×10^5). So the true d0 is astronomically large. The older bound is different in kind: graphs with no power-of-two cycle have average degree exp(O(log* n)), with explicit constants in the general formula [SRC: SV Thm 1.3, Cor. 1.4].

LM remark the exponent 1/10 is not optimised and the number of adjusters might drop from about m to O(log log n) [SRC: LM]. Montgomery states that minimum degree 3 would need "very substantial new ideas" [SRC: MON Q5.1].

## 3. What survives at minimum degree 3

**Survives.** Short cycles (length ≤ 2 log₂ n); the two-route idea, which needs no degree (any even cycle is an adjuster with step 2, any odd cycle with step 1) [INF]; long-range connection between large sets in an expander [SRC: LM Lemma 2.3].

**Fails.**
- *Robust local expansion.* Deleting three vertices isolates a cubic vertex; a path through v uses two of its three edges. Ends F1, F2 cannot be grown while avoiding prior structure [INF].
- *No expander subgraph of minimum degree 3 exists.* In a minimal counterexample every proper subgraph is 2-degenerate (deleting a cubic vertex leaves a 2-degenerate graph [SRC: DD Thm 3.3]; a proper subgraph with δ ≥ 3 would be a smaller counterexample). So either G itself expands, or the Komlós–Szemerédi subgraph H has degree-2 vertices and is a subdivision of a kernel with uncontrolled path lengths [INF]. KS only guarantees δ(H) ≥ d(H)/2, i.e. δ(H) ≥ 2 here [INF].
- *Minimality gives no expansion.* 2-degeneracy of G[U] gives e(U, V∖U) ≥ 6 − |U|, useless beyond |U| = 6 [INF].

**Obstructions.**
- *3-subdivisions.* Subdivide every edge of any expander twice: all cycle lengths are multiples of 3, never a power of two, yet the kernel has any degree and expansion you like. Any argument that uses only "expander with δ ≥ 2 plus good kernel" is false [INF]. Compare DD Thm 3.8: 2^j-subdivisions are exactly the harmless ones.
- *Expansion alone is no easier than the full conjecture.* [INF, sketch only] If a counterexample G0 on c vertices exists, take a 3-subdivided expander and hang a copy of G0 by a bridge on every subdivision vertex. The result has δ ≥ 3, cycles only inside copies of G0 or of length divisible by 3, and vertex expansion Ω(1/c). So "every α-expander with δ ≥ 3 has a power-of-two cycle, for every α > 0" is equivalent to the conjecture. A useful expander theorem must fix α, or assume 3-connectivity or minimality (a minimal counterexample is bridgeless).
- *Additive error in linear expanders.* α-expanders have a cycle of length in [ℓ, ℓ+A] for all ℓ in [a1 log n, a2 n], with A = O(1/α) optimal in α [SRC: FK Thm 1]. So exact lengths are not automatic even with linear expansion.
- *Low powers are avoidable.* Cubic graphs avoiding 4, 8, 16 exist on 78 vertices and avoiding 4–32 on 450; f(k) ≤ 15·n3(2^{k−2}+1) [SRC: GAR, an AI-assisted preprint, unverified by me]. [INF] So an N-vertex cubic graph can avoid all powers of two up to order log N: any proof must find cycles of length at least about log n, the regime where expander methods start.
- *Degree-3-critical graphs.* Arbitrarily large graphs with 2n−2 edges and no proper induced δ ≥ 3 subgraph miss cycle length 23 (Narins–Pokrovskiy–Szabó) [SRC: REPO literature.md L20, itself access-limited]. "All lengths in a window" fails for that class, though the example is not δ ≥ 3 in the EG sense.

## 4. Reductions from low to high degree

- **Nothing in the literature.** Neither survey nor LM gives a low-to-high-degree reduction preserving cycle lengths [SRC: LM, LET, MON by absence].
- **Topological route blocked by counting.** [INF] A branch vertex of a subdivision has degree at most its degree in G. With ≥ 2n/3 cubic vertices and ≤ 2n−2 edges [SRC: DD], every kernel has average degree below 4. Balanced clique subdivisions need average degree ≥ c·k² in general (tight) and ≥ c·k in C4-free graphs [SRC: LET Thm 5.6, Wang; HJYY Thm 1.3]; these say nothing at degree < 4 beyond K4.
- **Balanced K4.** [INF] A balanced subdivision of K4 with paths of length ℓ has cycle lengths 3ℓ and 4ℓ, so ℓ = 2^j gives a power-of-two cycle outright. Dirac's theorem gives a K4-subdivision at δ ≥ 3 (from memory), but with no length control.
- **DD Thm 3.8 uses only minimality**: the kernel K would be a smaller counterexample [SRC: DD]. It gives no positive handle unless one can force equal power-of-two path lengths. [INF] The condition cannot be relaxed much: a length function whose sum on every cycle C is 2^j·|C| must be constant 2^j on any theta, hence on 3-connected kernels.
- **Minors.** [INF] Contracting radius-r balls in a cubic expander raises degree to about 2^r, but a cycle of length L in the minor lifts to lengths anywhere in [L, (2r+1)L]. In high girth the balls are trees, transit routes are unique, and no flexibility is gained. A weighted LM theorem is false in general (weights all 3) and trivial by pigeonhole when all weights are powers of two.
- **Poles.** DD ask whether their one-pole equivalence extends to k vertices of degree ≤ 2 [SRC: DD §4.1]. This is the form in which expander extraction would meet the one-pole theory: an extracted piece is a "many-pole" graph [INF].

## 5. Sub-problems, ranked by tractability

**P1. Decoration equivalence (calibration; days).**
*Statement.* Prove: for every α > 0, EG holds iff every α-expander with δ ≥ 3 has a power-of-two cycle. Then decide whether the same holds within 3-connected graphs.
*Why.* Fixes which hypothesis an expander proof must use; if a 3-connected decoration exists, expansion is useless.
*Tool.* Expansion under bounded-size blob replacement.
*Failure.* The 3-connected part: any 2- or 3-attached gadget creates new cycles through it.

**P2. Hamiltonian cubic graphs by chord switching.**
*Statement.* Every C4-free cubic graph with a Hamilton cycle Z (n ≥ n0) has a power-of-two cycle. Intermediate: for chords with pairwise disjoint arcs of lengths a_1..a_r, the cycle lengths n − Σ_{i∈S}(a_i − 1) all occur; show some choice of Z and chord family makes these sums hit a power of two.
*Why.* A natural special case I believe open (not verified). It is the degree-3 form of the adjuster chain: every vertex of Z carries an ear for free, but shifts are not ±2.
*Tool.* LM's adjuster chaining; subset-sum interval theorems; rotation of Z.
*Failure.* Chords pairwise crossing (Möbius-like); shifts all ≥ girth and in one residue class, so sums form a progression that misses the target.

**P3. 3-connected linear expanders with fixed α.**
*Statement.* For each α > 0 there is n0 such that every 3-connected α-expander with δ ≥ 3 on n ≥ n0 vertices has a cycle of length 2^k.
*Why.* Settles the "generic" case (random cubic graphs); only O(1/α) adjusters are needed to remove FK's additive error.
*Tool.* FK Theorem 1 in a rooted, set-avoiding form; LM Lemma 4.8 assembly.
*Failure.* FK's construction may not allow prescribed endpoints; P1 shows 3-connectivity must be used essentially.

**P4. Robust expansion for most vertices at degree 3.**
*Statement.* In an n-vertex α-expander (or sublinear expander) with δ ≥ 3, for every W with |W| ≤ w, all but |W|·polylog(n) vertices v have |B^r_{G−W}(v)| ≥ polylog n for r = O(log log n).
*Why.* Replaces the degree-consuming step 3 of Section 2 by an "almost all vertices" statement; a building block for P3.
*Tool.* LM's robust-gadget argument (§2.6): failing sets are small and can be grouped.
*Failure.* The exceptional set may contain exactly the vertices the construction is forced to use.

**P5. k-pole generalisation.**
*Statement.* Determine the largest k such that "at most k vertices of degree ≤ 2, at least one of degree ≥ 3" still forces a power-of-two cycle, conditionally on EG; or find η > 0 allowing ηn/log² n such vertices in an expander.
*Why.* It is what Komlós–Szemerédi extraction produces: boundary sizes sum as Σ 1/i², which converges [INF].
*Tool.* KS extraction with defect counting; DD doubling.
*Failure.* The 3-subdivision obstruction shows placement of degree-2 vertices matters, not only their number; k = 2 may already fail.

## 6. Reading list

1. Liu–Montgomery, arXiv 2010.15802: the mechanism; read §2.4–2.6 and §4.
2. Montgomery, arXiv 2607.26049: shortest account of adjusters; states EG as Question 5.1.
3. Letzter, arXiv 2401.10865: catalogue of expander definitions and extraction lemmas.
4. Sudakov–Verstraëte, arXiv 0707.2117: exp(O(log* n)) bound with explicit constants; girth-based small-set expansion.
5. Friedman–Krivelevich, arXiv 1912.11011: cycle lengths in linear expanders with no degree hypothesis; the additive-error barrier.
6. Ducoffe–Dumitru, arXiv 2609.28594: structure of a minimal counterexample; one-pole equivalence; Thm 3.8.
7. Hou–Jin–Yang–Yang, arXiv 2407.01625: adjusters and balanced subdivisions in C4-free graphs.
8. Martinsson–Steiner, arXiv 2204.09107: residues of cycle lengths in linear expanders (abstract only read).

## Caveats

- LM's concluding remarks, if any, were not in the text I received; the final assembly in Lemma 4.8 was read, but Lemma 4.3's proof only in outline.
- Two extractions of LM disagreed on ε2 (1/100 or 1/10); I treat it as a small fixed constant.
- I did not read Verstraëte's survey "Extremal problems for cycles in graphs" (no accessible copy found by search).
- The repo's 2n−6 edge bound was not used; everything above needs only 2n−2.
- Everything tagged [INF], especially the decoration equivalence and the numerical thresholds, needs checking before reuse.

## Sources

Read (via fetch, content summarised by the fetch tool rather than seen verbatim):
- https://ar5iv.labs.arxiv.org/html/2010.15802 (all three parts)
- https://arxiv.org/pdf/2401.10865 and https://arxiv.org/abs/2401.10865 (first 100k of 109k characters)
- https://arxiv.org/pdf/2607.26049 and https://arxiv.org/abs/2607.26049
- https://arxiv.org/pdf/2609.28594 and https://arxiv.org/abs/2609.28594
- https://ar5iv.arxiv.org/html/0707.2117
- https://arxiv.org/abs/1912.11011
- https://arxiv.org/abs/2204.09107v1
- https://arxiv.org/pdf/2609.04686
- https://arxiv.org/html/2407.01625v1 (first 100k characters)
- https://arxiv.org/abs/2609.26401 (Milojević–Montgomery–Pokrovskiy–Sudakov; first 100k characters)
- https://arxiv.org/html/2605.22232 (nested cycles; background only)
- https://www.emergentmind.com/papers/2608.20190 (metadata only)
- Repo files: proof.md (O30-5), literature.md (L19, L20), one_pole.md (§0, O1)
