# Erdős–Gyárfás: 28-vertex rooted-cubic audit (preparatory packet)

**Created:** 2026-11-16 (US Eastern). **Status:** Exact verifier implemented and tested; *the complete order-28 graph dataset has not been obtained*. This packet does **not** establish a 28-vertex rooted classification.

## Research question

Markström (2004), *Extremal graphs for some problems on cycles in graphs*, reports 251 connected cubic graphs of order 28 having neither a C4 nor a C8. The ordinary conjecture is verified at this order, but that does not decide the stronger rooted assertion:

> Does every cyclically four-edge-connected cubic graph G of order 28, with no C4 or C8, have a C16 avoiding each of its vertices?

For these graphs, rooted failure means exactly that at least one vertex belongs to every C16. This is what the supplied exact code checks. The test is significant only if the graph6 input is a **complete, correctly sourced and deduplicated 251-graph census**. A file merely containing 251 rows is insufficient evidence of completeness.

## Exact checker

```
python verify_g6.py complete_28_C4_C8_free.g6 \
    --expect-count 251 --strict --output order28_results.json
```

Input format: one **graph6** representation of a simple graph per line. The command requires a 28-vertex connected cubic graph, checks absence of C4 and C8, tests 3-vertex-connectivity and every possible nontrivial 3-edge cut, and checks dyadic cycles avoiding every root. In this strict regime, the only possible dyadic length is 16.

The C16 oracle is **exact**: a simple C16 exists if and only if there are two internally vertex-disjoint length-eight paths with the same endpoints. It enumerates all length-eight paths from each start vertex, groups them by endpoint, and tests pairwise intersection of vertex bitmasks. Thus a negative answer is an exhaustive search, not a Monte Carlo result. For every C16 query in this script an independently written bounded-depth DFS search is also run by default. Positive answers are saved as explicit cycles and checked edge-by-edge.

A graph is marked prime only when it is 3-vertex-connected and has no cyclic three-edge cut. All triples of edges are tested. Triangle-containing graphs are immediately excluded from prime status because their three incident external edges form a nontrivial cyclic three-edge cut in a connected cubic graph of order at least six.

**Warning:** If a root is certified only via C4 or C8, the output appropriately records that shorter cycle, rather than incorrectly declaring it critical because it lacks a C16. The 28-vertex strict input excludes those cases.

## Checks actually completed

| Input | Count | C4/C8-free | Prime and C4/C8-free | Root-critical graphs | Interpretation |
|---|---:|---:|---:|---:|---|
| Prior audit controls | 6 | 4 | 0 | 1 (K4) | Petersen is rooted-robust via C8; four 24-vertex near-misses are rooted-robust via C16 |
| Coxeter graph (28 vertices) | 1 | 0 | 0 | 0 | Prime graph has C8; excluded from target family |
| Random-regular oracle comparisons | 64 rooted C16 queries | N/A | N/A | N/A | MITM and independent exhaustive DFS agreed in every tested query |

The four 24-vertex near-miss graphs are sourced from the previous `Rooted_Conjecture_Audit/controls.g6`. Their status as the complete order-24 family was reported in earlier work and in published sources; this packet **does not independently re-enumerate all cubic graphs on 24 vertices**.

### Separate small negative experiment

Starting from the four 24-vertex near-misses, all **96** single vertex-to-triangle expansions (four graphs × 24 vertices) were tested. No expansion remains both C4-free and C8-free. Breakdown: 12 acquire only C4; 36 acquire only C8; 48 acquire both. This is exact for the supplied four starting graphs, but it does not classify 26-vertex graphs, and no 28-vertex graph is thereby obtained. It cautions against assuming all extremal graphs arise by naive triangle expansion.

Run `python triangle_expansion_controls.py` to reproduce.

## Why this calculation matters and what it cannot settle

The full 28-vertex ordinary search has already been completed and reported in the literature. The extra question here is whether the stronger **root-avoiding** property holds for the prime subset. A verified root-critical example would falsify the specific rooted conjecture pursued in earlier research passes, while leaving the original Erdős–Gyárfás conjecture untouched. A verified negative census would only settle rootedness for this small order.

A complete order-28 scan from scratch is costly: a standard generation paper reports 40,497,138,011 connected cubic graphs on 28 vertices, of which 656,783,890 have girth at least five. The present packet does not claim to generate that space. Prefer obtaining Markström's exact 251 graph6 objects, or reproducing them with a certified forbidden-cycle generator using independent count/isomorphism checks.

## Recommended external sources

- K. Markström, *Extremal graphs for some problems on cycles in graphs* (2004), public PDF: https://citeseerx.ist.psu.edu/document?doi=27733b5bbe1c33ff70addf950e622f0330c1938e&repid=rep1&type=pdf
- G. Brinkmann, J. Goedgebeur, B. McKay, *Generation of Cubic graphs* (2011): https://dmtcs.episciences.org/articles/551/download
- R. J. Kingan, S. R. Kingan, *On cyclically 4-connected cubic graphs* (2024): https://doi.org/10.1080/09728600.2024.2333397
- Later independent exploration of order 24 and 26: https://github.com/oaustegard/experiments/blob/main/erdos-gyarfas/note.html

## Reproduce this packet

```
python test_oracles.py
python verify_g6.py controls.g6 --output control_results.json
python verify_g6.py coxeter.g6 --output coxeter_results.json
python triangle_expansion_controls.py
```

Requires Python 3 and `networkx`. Results were run locally with NetworkX 3.6.1.

## Next decision gate

1. Obtain the actual 251-item order-28 census with provenance, or regenerate via a trusted compiled generator (not a random sample).
2. Run the exact root test and export each minimal positive cycle-cover certificate and negative exhaustive evidence.
3. If no prime graph survives the C4/C8 filter, record that **as a bounded structural result only after the dataset is certified**.
4. If some prime graphs survive, prioritize rooted failure search on them and only then reassess the proof architecture.
5. If no complete dataset can be obtained economically, stop expanding this census and shift to a broader literature-backed problem with a genuine forcing mechanism.
