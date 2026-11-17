# Partial triangle expansion: exact constraints and a small complete census

**2026-11-16 — Research continuation of PR #2**

**Status:** The cycle-length formula and reductions below have a hand proof and were tested by separate algorithms; they are **not formally verified**. The census is **computationally verified, conditional on the published completeness of the cubic-graph counts**. No claim of mathematical novelty is made. This work does **not** prove the Erdős–Gyárfás conjecture.

## Relation to prior work

This is a special case and implementation of Garcia's *window lemma* (Section 3 of [arXiv:2609.04686](https://arxiv.org/html/2609.04686)), extended here to a **vertex-subset constraint solver** and a reproducible census on the complete cubic bases of orders 8 and 10. It also complements the truncation observations already made in `extremal24_findings.md` in PR #2. We did not have programmatic access to the merged repository source in this session; the attached files are **additions only** to avoid modifying existing work.

## Exact simultaneous-triangle-expansion formula [PROVED_IN_MARKDOWN]

Let `B` be a finite simple cubic graph and `S ⊆ V(B)`. Build `T_S(B)` by replacing every vertex of `S` with a triangle whose three vertices are attached one-to-one to its former neighbors; leave vertices outside `S` unchanged. The resulting graph is still simple and cubic, with `|V(T_S(B))| = |V(B)| + 2|S|`.

For a simple cycle `C` of `B`, write `L=|C|` and `s=|C ∩ S|`. Then its lifts to `T_S(B)` have **exactly** the possible lengths

```
L+s, L+s+1, ..., L+2*s.
```

Every simple cycle of `T_S(B)` is either an internal triangle at some expanded vertex or a lift of one original simple cycle. Consequently,

```
CycleLengths(T_S(B)) = ({3} if S nonempty else empty)
  union ⋃_{C simple cycle in B} [|C|+|C∩S|, |C|+2|C∩S|] ∩ integers.
```

**Proof.** Any simple cycle passing through an expanded triangle uses exactly two of the triangle's three external edges: the number of external edges used must be even, and it cannot be four or more. It traverses either the direct internal edge (length 1) or the two-edge internal route (length 2), exactly once. Contract the expanded triangles. The projected route is a simple cycle `C` of `B` (a repeated base vertex would require revisiting one of the triangle's three vertices). Conversely, for a base cycle, the direct or long internal route can be selected independently at each expanded vertex, so every integer between the two extremes is attained. A simple cycle using no external edges must be an internal triangle. QED.

### Constraint reduction [PROVED_IN_MARKDOWN]

For each base cycle `C`, define `s_C = |C ∩ S|`. To avoid forbidden cycle lengths `F` (e.g. `{4,8,16}`), it is **necessary and sufficient** that:

```
for every simple base cycle C:
    F ∩ [|C|+s_C, |C|+2*s_C] = empty.
```

All internal triangles have length three and are harmless for power-of-two avoidance. These are pure cardinality constraints on the 0/1 selection vector of `S`. In particular, forbidding 4- and 8-cycles yields:

| Base cycle length | Permitted expanded vertices on this cycle |
|---|---|
| 3 | 0 or 2 |
| 4 | **exactly 1** |
| 5 | 0, 1, 4 or 5 |
| 6 | 0, 3, 4, 5 or 6 |
| 7 | 0, 2, 3, 4, 5, 6 or 7 |

The C4 condition is an **exact-one hitting-set constraint** and can be encoded in SAT/PB/ILP. No candidate expanded graph needs to be built until these constraints pass.

## Complete small-base census [COMPUTATIONALLY VERIFIED]

The bundled fixture `scripts/cubic_catalog_n8_n10.json` contains 5 pairwise nonisomorphic connected cubic graphs of order 8 and 19 of order 10, meeting the published counts in Brinkmann–Goedgebeur–Van Cleemput's survey [Table 1](https://caagt.ugent.be/jgoedgeb/paper-cubic_graphs_survey.pdf). Completeness of this finite fixture follows from these published counts *if those counts are correct*; the fixture was constructed via seeded sampling and pairwise isomorphism tests. All `2^n` expansion subsets per base were checked using the exact constraints, and every surviving expansion was independently checked with a DFS cycle oracle for 4, 8 and 16.

| Cubic base order | Base isomorphism classes | Expanded order | Subsets avoiding 4, 8 | Resulting isomorphism classes | Classes planar |
|---|---:|---:|---:|---:|---:|
| 8 | 5 | all | 0 | 0 | 0 |
| 10 | 19 | 24 | 2 | 1 | 1 |
| 10 | 19 | 26 | 9 | 2 | 0 |
| 10 | 19 | 28 | 10 | 1 | 0 |
| 10 | 19 | 30 | 1 | 1 | 0 |

Each of the 22 successful labeled choices on order-10 bases **does contain a 16-cycle**, as both the exact formula and independent DFS confirm. The two order-24 constructions are isomorphic. Since the published 24-vertex census has four such graphs, exactly one planar, the unique planar output agrees with the Markström graph's defining properties. This is a **reconstruction of a known extremal**, not a new counterexample.

### Short certificate for a 24-vertex witness

Connected cubic base graph (10 vertices), encoded as graph6:

```
IAiAjQCKG
```

Equivalently, edges (with original 0–9 labels):

```
(0,4) (0,5) (0,8) (1,3) (1,6) (1,7) (2,4) (2,7)
(2,9) (3,6) (3,9) (4,7) (5,6) (5,8) (8,9)
```

Expand the seven vertices `S={1,2,3,4,5,8,9}`. Output: 24 vertices, cubic, connected, planar, no cycle of length 4 or 8, but at least one cycle of length 16. A second choice `S={0,2,3,6,7,8,9}` gives an isomorphic output.

This construction is enough to reproduce the class; the script also prints a graph6 encoding of the expanded graph.

## Reproduction

Python 3 with `networkx` is required; `pytest` is optional for the test command. From the repository root:

```bash
python -m pytest -q tracks/2026-11-halving/scripts/test_partial_triangle_expansion.py
python tracks/2026-11-halving/scripts/census_small_bases.py
python tracks/2026-11-halving/scripts/partial_triangle_expansion.py --base petersen --forbid 4 8 --cross-check
```

The tests compare full predicted and enumerated cycle spectra on all subsets of small sample bases. The census compares constraint solutions against an independently implemented DFS cycle detector and groups outputs by graph isomorphism. **Do not substitute `make test`** while the unrelated existing test-collection issue documented in PR #2 remains unresolved.

## Use in further research

The valuable next step is to use these cardinality constraints as a front end to a larger **mixed-gadget or sequential vertex-replacement search**, where a precomputed path-length spectrum is attached to each port pair. In particular:

1. Compile each base cycle into a forbidden-sum table and dispatch it to a PB-SAT solver before constructing expanded graphs.
2. Generalize to triangle / H7 / H15 gadgets with attachment-aware path spectra, matching Garcia's full window calculus.
3. Track isomorphism only after a solution passes all cycle constraints; store base graph6 + gadget assignment as a compact, independently verifiable certificate.
4. Concentrate on order >48 or non-cubic structural obstructions if the goal is *new* progress beyond Ducoffe–Dumitru's 2026 verification frontier; do not mistake a recovered small extremal for an extension.

**Limitations:** `nx.simple_cycles` can take exponential time on large dense bases. This code intentionally targets small cubic bases and cannot certify the main conjecture. The census depends on the published complete counts of cubic bases; it is not a new independent graph-enumeration proof. Novelty of the specific classification was not systematically checked against all unpublished data.
