# Pass XII status map (to integrate into the branch's central status map)

| Topic | Status | Evidence / boundary |
|---|---|---|
| Triangle-built clean poles | **PROVED** | `tower_theorem.md`: all-order induction; clean types I, T, S, H15; identity is virtual |
| `K4` substitutions with uniform H7 | **PROVED** | Same 35-case interval argument; no extra clean outputs |
| Hamiltonian port-span for any triangle-built pole | **PROVED** | Induction through all three children |
| Complete path interval for arbitrary triangle-built poles | **PROVED (false in general)** | Five-vertex unclean example path lengths `{1,3,4}` |
| Complete interval for clean triangle-built poles | **PROVED** | Simultaneous induction in tower theorem |
| Cyclic-three-edge-cut reduction if cap is 3-edge-connected | **PROVED** | `decomposition_lemma.md`; root-preserving cut contractions |
| Full arbitrary-cap decomposition; WRP ⇒ T | **OPEN** | Bridge/one-pole and 2-cut/two-pole cases remain |
| WRP prime-base cycle window property | **OPEN** | Precise statement in `decomposition_lemma.md` |
| Dual-checker tower and `K4` finite profiles | **COMPUTED** | Matching Python and C streams, exit codes and hashes in manifest |
| Dual-checker earlier cubic-fixture deletions through pole order 11 | **COMPUTED** (fixture-dependent) | Matching Python/C streams; no new generator completeness claim |
| Complete two-pole enumeration at orders 4 and 6 | **COMPUTED** | NetworkX atlas vs C labeled edge-subset generator |
| 3-pole `geng` census orders 13–23 | **OPEN** | No `geng` or target branch files accessible |
| 2-pole `geng` census orders 8–22 | **OPEN** | Not run |
| Conjecture T | **OPEN** | Tower theorem proves only a subfamily |
| Erdős–Gyárfás for all cubic graphs assuming T | **CONDITIONAL** | Spanning-tree-leaf deletion and existing small-order verification |

The central branch README and plan cannot be edited or committed from this package-only workspace. Include the status updates and the companion `plan.md` entry in the *same actual Git commit* on the target branch before submitting or merging.
