# Erdős–Gyárfás rooted audit: correction and current status (2026-11-17)

## Corrected classifier
The prior `verify_g6.py` computed `prime = connected3 and tri==0 and cut is None`, and only called `cyclic_three_edge_cut` when triangle-free. This is not the standard definition of cyclically 4-edge-connected: K4 is 3-connected, has no cyclic 3-edge cut, and is cyclically 4-edge-connected under the standard definition, despite its triangles. The extra triangle-free filter must be a separately named research restriction. The supplied corrected script removes this filter and always checks 3-edge cuts in 3-connected graphs.

Reproduction: `cd EG28_Rooted_Audit && python test_oracles.py && python verify_g6.py controls.g6 --output corrected_controls.json && python triangle_expansion_controls.py`.

Corrected control output: Petersen (10 vertices) is cyclically 4-edge-connected and rooted-robust; K4 is cyclically 4-edge-connected and every root is critical; four 24-vertex C4/C8-free controls are not cyclically 4-edge-connected and are rooted-robust. The corrected controls give prime-root-critical = 1, not 0. For the intended 28-vertex C4/C8-free class the triangle filter is expected to agree with cyclic edge connectivity, because a triangle has a cyclic external 3-edge cut in connected cubic graphs of order at least 6, but this must be stated as a lemma with its hypotheses.

## Census provenance
No complete, verified 251-record order-28 graph6 dataset was available locally, and runtime DNS could not reach raw.githubusercontent.com. The published count 251 is sourced, but there is no order-28 exhaustive rooted classification in this packet.

## Literature caution
The `oaustegard/experiments` research note states Markström's old computation reached n<=52, while `chriss1245/erdos-gyarfas-cubic-frontier` claims a newer n<=40 bound. This is an apparent priority/baseline inconsistency requiring the original Markström source or archived logs before accepting the 52 assertion. Do not claim 40 is a new best bound without resolving it.

## Further direction
Seek a sourced order-28 dataset and independent canonical checks. Alternatively test rooted assertions with explicit small graph exclusions (K4 already falsifies the unrestricted cyclically-4-edge-connected version). Distinguish the stronger `triangle-free and cyclically four-edge-connected` hypothesis from standard cyclic connectivity.
