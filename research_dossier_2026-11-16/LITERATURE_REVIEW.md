# Literature review — Erdős–Gyárfás and the tools used in this dossier

**Compiled:** 17 November 2026. **Scope:**
- every external result this dossier relies on or positions itself against;
- with what was actually verified, and how;
- grouped by role in the program (see `program/` and `passes/`).

**Verification levels**

| Level | Meaning |
|---|---|
| **R** | Read: the relevant statement or proof was read in the full text during this work. |
| **A** | Abstract: the statement was checked against the arXiv abstract or journal page. |
| **S** | Secondary: known only through another paper's quotation; check the original before citing. |
| **D** | Dossier: inherited from the 16 November dossier; not re-verified here. |

## 1. Status of the conjecture

**Conjecture (Erdős–Gyárfás, 1995).** Every graph with minimum degree ≥ 3 contains a
cycle whose length is a power of two.

- **Status:** open as of November 2026. Erdős Problems #64.
- **Prize:** $100 for a proof, $50 for a counterexample, as recorded by the external
  campaign below.
- **Expert view:** Montgomery's 2026 survey (§1, item 1, row M1 below) states that a
  positive answer "would require very substantial new ideas". **R**

## 2. Minimal counterexamples and finite frontiers

| Ref | Result | Level |
|---|---|---|
| Ducoffe–Dumitru, *Towards a more structured search for Erdős–Gyárfás counter-examples*, arXiv:2609.28594 (Sep 2026) | Minimal counterexample is 2-edge-connected and almost biconnected; > 2/3 of vertices have degree 3; EG verified for all graphs ≤ 40, bipartite ≤ 66, cubic ≤ 48 vertices. | **A** |
| Carr, *Every minimal counterexample … is predominantly cubic*, arXiv:2605.22844 (May 2026) | Every regular minimal counterexample is cubic; every vertex is adjacent to a degree-3 vertex; ≥ 4/7 of vertices have degree 3. Builds on Markström's observation that degree-≥4 vertices form an independent set. | **A** |
| Tranquilli, *A 60-vertex lower bound for cubic bipartite counterexamples*, arXiv:2608.02675 (Aug 2026) | **Certified computation:** every cubic bipartite graph on ≤ 58 vertices has a C₄, C₈ or C₁₆. Not a result for all orders, although search snippets suggest otherwise. Uses Moore bound plus Levi-graph/configuration search. | **A** |
| Markström, *Extremal graphs for some problems on cycles in graphs*, Congr. Numer. (2004) | Cubic graphs with no C₄, C₈: exactly 4 on 24 and 23 on 26 vertices. All contain C₁₆. | **D**, counts independently reproduced by the external campaign |
| External campaign, `github.com/mcolsen/erdos-gyarfas` (MIT; final state Aug 2026; unrefereed) | No counterexample: general ≤ 35, cubic ≤ 48 (frontier ≥ 50), bipartite ≤ 56. Smallest {C₄,C₈,C₁₆}-free cubic graph bracketed in [50, 82]. Audit confirming Carr (sharpened to ≥ 2/3). "α-block equivalence": EG fails iff a 2-connected graph with ≤ 1 degree-2 vertex avoids all powers of two up to its order. Arc-transitive census ≤ 10,000 and vertex-transitive ≤ 1,280 swept. | **R** (reports and data read; graphs used in Pass XIV) |
| Zenodo record 23886386 (Nov 2026; single author, unreviewed) | Explicit cubic graph on 370 vertices with no C₄, C₈, C₁₆, C₃₂, so f(5) ≤ 370. Construction of order 26,550 avoiding up to C₆₄. | **A**; both graphs checked in Pass XIV for rooted robustness only |

**Our use.** The growth reformulation (`program/STRATEGY_2026-11-17.md` §2): EG holds iff
f(k) ≥ 2^(k+1) for every k. The smallest open band is k = 5, i.e. 41–63 vertices; for cubic
graphs, 50–62.

## 3. Classes for which EG is proved

| Ref | Class | Level |
|---|---|---|
| Heckman–Krakovski, EJC 20 (2013), doi:10.37236/3252 | 3-connected cubic planar graphs | **A** |
| Daniel–Shauger; arXiv:1109.5398 | claw-free graphs (incl. cubic claw-free) | **A** (title and abstract) |
| Gao–Shan, arXiv:2109.01277 | P₈-free graphs (cycle of length 4 or 8) | **A** |
| *The EG conjecture holds for P₁₀-free graphs*, Discrete Math. (2024), doi:10.1016/j.disc.2024.114175 | P₁₀-free graphs | **A** (title) |
| Hegde–Sandeep–Shashank, arXiv:2410.22842 | P₁₃-free graphs (computer-assisted) | **A** |
| arXiv:2508.19302 | diameter 2 (cycle of length 4 or 8) | **A** |
| Burkhart, arXiv:2611.05060 (Nov 2026) | Cayley graphs of odd order; Cayley graphs of nilpotent groups | **A** |
| Liu–Montgomery, *A solution to Erdős and Hajnal's odd cycle problem*, JAMS (2023), arXiv:2010.15802 | sufficiently large constant average degree ⇒ a cycle of power-of-two length; more generally many sparse sequences of lengths are unavoidable | **R** (as stated in Montgomery's survey §5) |

## 4. Cycle lengths in expanders — the backbone of Pillar A

| Ref | Result | Level |
|---|---|---|
| Friedman–Krivelevich, *Cycle lengths in expanding graphs*, Combinatorica 41 (2021), arXiv:1912.11011 | In an α-expander, for every ℓ ∈ [a₁ log n, a₂ n] there is a cycle of length in [ℓ, ℓ + A], A = O(1/α), and A's order is optimal. Ω(α³/log(1/α))·n distinct lengths. β-graphs contain every length in [b₁ log n, (1 − b₂)n]. Lemmas 2.1–2.7 and the full construction were read and used in Passes XV and XIX. | **R** |
| Martinsson–Steiner, *Cycle lengths modulo k in expanders*, arXiv:2204.09107 | For α > 1/(p − 1) (p the least prime factor of k), large α-expanders have all residues mod k. Sharp: for α < c/(p − 1), subdivided expanders (δ = 2) have all cycle lengths ≡ 0 mod p. **Open question (§4):** does every large 3-connected α-expander have all residues mod odd k, for every α? Proof read in full; the adjuster-chain and removal lemma (Lemma 3.1) are used in Passes XVI–XVIII. | **R** |
| Alon–Krivelevich, *Divisible subdivisions*, JGT 98 (2021); Mészáros–Steiner | Every large α-expander has a cycle of length ≡ 0 mod k (via K_f minors) | **S** (via Martinsson–Steiner) |
| Montgomery, *Recent progress in graph theory using expansion*, arXiv:2607.26049 (Jul 2026), §5 | Survey. Describes the Liu–Montgomery adjuster ("paths which enter and leave on almost-but-not-quite opposite sides of each adjusting cycle"); sublinear expanders without dense spots have all even lengths in [log⁷ n, n/log¹² n]; poses EG as Question 5.1. | **R** |
| Draganić–Montgomery–Munhá Correia–Pokrovskiy–Sudakov, *Hamiltonicity of expanders: optimal bounds and applications*, arXiv:2402.06603 | C-expanders are Hamiltonian | **A** |
| Draganić–Munhá Correia–Sudakov, *Chvátal–Erdős condition for pancyclicity*, J. Amer. Math. Res. (2024) | Pancyclicity via a path with attached triangles plus shortening/augmenting. The source of the triangle-adjuster idea (Pass XV). | **A** (abstract-level description) |
| arXiv:2503.07147 | nearly Hamilton cycles in sublinear expanders | **A** |
| Krivelevich, *Expanders — how to find them, and what to find in them* (survey) | robustness of expanders; subdivisions preserve expansion (Prop. 4.2) | **S** (via FK and MS) |

## 5. Cycle lengths under minimum degree and connectivity — local adjusters

| Ref | Result | Level |
|---|---|---|
| Fan, *Distribution of cycle lengths in graphs*, JCTB 84 (2002) 187–202, Cor. 3.1 | If H is 2-connected and all vertices except u, v have degree ≥ 3, there are u–v paths R₁, R₂ with \|R₁\| ≥ 2 and 1 ≤ \|R₂\| − \|R₁\| ≤ 2. **Central to Passes XVI–XX.** | **S** — quoted verbatim in Liu–Ma (arXiv:1508.07912, proof of Lemma 2.2). **Check against Fan's original before citing.** |
| Bondy–Vince, JGT 27 (1998) | Graphs with ≤ 2 vertices of degree < 3 (other than K₁, K₂) contain two cycles whose lengths differ by 1 or 2. 2-connected non-bipartite graphs of large minimum degree need not have consecutive lengths. | **S** |
| Liu–Ma, *Cycle lengths and minimum degree of graphs*, JCTB, arXiv:1508.07912 | Rooted 2-connected graphs with min degree ≥ k+1 have k x–y paths with the length condition (bipartite: consecutive even lengths). Used for rooted 2-connectivity and the bipartite Fan variant. | **R** (relevant sections) |
| Gao–Huo–Liu–Ma, *A unified proof of conjectures on cycle lengths in graphs*, IMRN (2022), arXiv:1904.08126 | Thomassen's and related conjectures: min degree k + 1 ⇒ cycles of all even residues mod k | **A** |
| Lyngsie–Merker, *Cycle lengths modulo k in large 3-connected cubic graphs*, Adv. Comb. 2021:3, arXiv:1904.05076 | Large 3-connected cubic graphs contain cycles of every residue mod odd k. **Fails for 2-connected cubic graphs** when 3 divides m and k, with k ≥ 12. Theta-necklace method. | **A** |
| Chen–Saito, JCTB (1994) | min degree ≥ 3 ⇒ a cycle of length divisible by 3 | **S** |
| Thomassen | cubic graphs of large girth contain all residues mod odd k | **S** (via MS) |

**Caution from Lyngsie–Merker.** Their 2-connected cubic examples show that residue
claims about 2-connected graphs need an extra hypothesis. In our program that hypothesis
is α-expansion. The conditional theorem of Passes XVIII–XX ("bounded-degree 2-connected
δ ≥ 3 *expanders* have all residues mod odd k") must be checked against their
construction. If their examples can be made expanding, our claim would be false.
**Action item.**

## 6. Structure of cubic graphs (dossier inputs)

| Ref | Result | Level |
|---|---|---|
| Kingan–Kingan, AKCE (2024), doi:10.1080/09728600.2024.2333397 | Generation of cyclically 4-connected cubic graphs by bridging | **D** |
| Nedela–Seifrtová–Škoviera, *Decycling cubic graphs*, Discrete Math. (2024), arXiv:2309.11606 | Coherent decycling partitions of cyclically 4-edge-connected cubic graphs | **D** (Pass XIII) |
| Bucić–Gishboliner–Sudakov, FoMS 10 (2022) | Hamiltonian graphs with δ ≥ 3 have n^(1−o(1)) cycle lengths | **D** |
| Garcia, *Small graphs without power-of-two cycles*, arXiv:2609.04686 | Finite constructions; every counterexample has ≥ 24 vertices | **A** (search summary) |
| Traldi, EJC (2011) | interlace polynomials (Pass XXV context) | **D** |

## 7. How our results sit against the literature

| Our item | Relation | Novelty status |
|---|---|---|
| Growth reformulation (EG ⟺ f(k) ≥ 2^(k+1)) | elementary; implicit in finite searches | likely folklore; useful framing |
| Rooted robustness fails for 3-connected cubic graphs at n = 16 (Pass XIV) | refines the dossier's rooted-prime programme | computational; new as far as we know |
| Rigid-pocket example (Pass XVI Prop. 1) | δ ≥ 3 variant of MS Prop. 1.4 | small but clarifying |
| Thm 1, Pass XVII: short (O(log n)) nonzero-residue cycle in 2-connected δ ≥ 3 expanders, any α | partial answer to MS §4 for *one* residue with a *length bound*; Fan gives existence without length | **appears new**; needs refereeing |
| Anchoring and nesting lemmas (Pass XVIII) | removes MS's α-threshold at the level of existence of good candidates | appears new |
| Π-gadget lemma (Pass XX) | position-free and modulus-free adjuster; a structural cousin of Liu–Montgomery adjusters and DMS triangles | appears new; elementary |
| Conditional expander theorem (Passes XVIII–XX) | would answer MS §4 for bounded degree, and give EG for 2-connected bounded-degree δ ≥ 3 expanders | conditional (G1′, robust linkage, M1 constants, subcase T); **check against Lyngsie–Merker's 2-connected examples** |

## 8. Gaps in this review

- **Not read in full:** Fan (2002), Lyngsie–Merker (2021), Liu–Montgomery (2023),
  Heckman–Krakovski (2013), Ducoffe–Dumitru (2026). The last two matter for positioning;
  the first three for correctness of Passes XVI–XX.
- **Erdős Problems #64:** the page and the erdosproblems forum were not re-checked this
  session. Forum posts may contain partial results (the external campaign notes a forum
  post of the ≥ 2/3 bound).
- **Not searched systematically:** non-English literature, and theses (e.g. the Utah
  State thesis that appeared in one search).
