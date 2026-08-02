# FC-N by direct SAT graph-existence search: extending the (2,\*)-terminal series past order 15

**Status of the artefact**: `[COMPUTATIONALLY_VERIFIED]` for the orders marked
UNSAT below; `[TIMEOUT]` (explicitly *not* a result) for the rest.

## 0. What this file is

`fcn_order15_result.md` closed the `(2,*)`-terminal two-terminal `C4`/`C8`
series through order 15 by `nauty-geng` enumeration, and hit a wall doing it:
`n=15` alone already needed 2,625,442 raw candidate graphs and a compiled C
batch detector. `separator_theorem_order32_gap_analysis.md` and the Type-B
reduction reported in chat want this series pushed to **order 21** (the
"`(2,2)`-piece of order `<=21`" that Type B's 2-cut case reduces to). Raw
enumeration cannot get there.

This pass replaces generate-and-filter with a **direct graph-existence search**:
the graph itself is the decision variable. One Boolean per unordered vertex
pair, and a SAT solver either *constructs* a satisfying graph or *proves none
exists*. Code: `verifier/fcn_sat_existence.py`; validation harness:
`verifier/test_fcn_sat_existence.py`.

## Headline: the series does NOT continue — FC-19 and FC-21 are **FALSE**

The solver was validated against both published results, agreed with both
exactly, and then found:

- **`n = 16, 17, 18`: UNSAT** — new, genuine extensions of FC-15.
- **`n = 19`: SAT.** An explicit 19-vertex, 28-edge graph with
  `d(x)=d(y)=2`, all other degrees `>=3`, `xy` absent, `B+xy` 2-connected,
  and **no `C4` and no `C8`**.
- **`n = 21`: SAT.** Likewise, 21 vertices, 31 edges.

Both survivors were audited adversarially
(`verifier/fcn_survivor_audit.py`, §5) and are **genuine, not encoding bugs**.

So the `(2,*)`-terminal `C4`/`C8` series **stops at 18**. Pushing it "through
order 21", which was the stated goal, is not merely hard — it is impossible,
because the proposition is false there. The `(2,2)`-piece of order `<=21` that
the reported Type-B reduction wants to eliminate **cannot be eliminated by
`C4`/`C8`-avoidance alone**.

**The redeeming detail**: both survivors *contain a `C16`* (confirmed by all
four independent detectors). They are therefore **not** counterexamples to
Erdős–Gyárfás; they are only counterexamples to the artificially restricted
`{C4,C8}` proposition. See §4.3 for the `{C4,C8,C16}` version, which is the one
the application actually needs.

## 1. The predicate, stated exactly

For parameters `n` and `d_x in {1,2}`, decide:

> Does there exist a simple graph `B` on `n` vertices with a designated
> terminal `x` with `d_B(x) = d_x` **exactly**, a designated terminal `y != x`
> with `d_B(y) >= d_x`, `d_B(v) >= 3` for every `v notin {x,y}`,
> `xy notin E(B)`, `B+xy` 2-connected, and `B` containing no `C4` and no `C8`?

UNSAT at `(n, d_x=1)` is exactly proposition **F-n** (`f12_order12_result.md`);
UNSAT at `(n, d_x=2)` is exactly proposition **FC-n**
(`fcn_order15_result.md`). These two files are the ground truth this solver is
validated against before it is used prospectively.

**No degree-sequence shape is assumed.** This matters: `fcn_order15_result.md`
documents a real bug caught in the brute-force version, where an early script
assumed the even-`n` "both terminals exactly degree 2" shape and silently
filtered every odd-`n` candidate away, producing a spurious "0 survivors". The
SAT encoding cannot make that mistake by construction — it constrains
`deg(x) = d_x` exactly, `deg(y) >= d_x`, `deg(v) >= 3` otherwise, with **no
upper bound on any degree** and no total-edge-count bound, so the parity slack
lands wherever the solver wants it. Nothing in the encoding references
`m_min`, `ex(n;{C4,C8})`, or a degree cap. (The brute-force cross-check in
`verifier/test_fcn_sat_existence.py` is likewise shape-free: it runs over
*every* graph on `n` vertices and *every ordered pair* of distinct vertices as
`(x,y)`.)

## 2. Encoding

Variables: `e_{ij}` for every unordered pair `i<j` (`C(21,2) = 210` at `n=21`).

| condition | how |
|---|---|
| `xy notin E(B)` | unit clause `~e_{01}` |
| `deg(x) = d_x`, `deg(y) >= d_x`, `deg(v) >= 3` | sequential-counter cardinality constraints on each incidence row (PySAT `CardEnc`) |
| **no `C4`** | **eager**: for every 4-subset, forbid each of its three 4-cycles. Equivalently "every vertex pair has at most one common neighbour", which is exactly `C4`-freeness for simple graphs. `3*C(n,4) = 17,955` clauses at `n=21` |
| **no `C8`** | **lazy (CEGAR)**: solve; enumerate the candidate's 8-cycles; add one 8-literal blocking clause per 8-cycle; re-solve incrementally. An eager encoding would need `2520*C(n,8) = 5.1e8` clauses at `n=21` — hopeless |
| **`B+xy` 2-connected** | **lazy**: when a `C4`/`C8`-free candidate has a cut vertex `c` splitting `V\{c}` into `S`&#124;`T`, add the clause "some edge of `B+xy` crosses `S`&#124;`T`" |
| symmetry breaking | the vertices `{2,...,n-1}` carry identical constraints, so the edge-variable serialisation is required to be lex-maximal under **every transposition** of that block (`C(n-2,2) = 171` lex constraints at `n=21`) |

### Why UNSAT is a proof

Every clause ever added — eager or lazy — is satisfied by **every** genuine
solution of the predicate, so the accumulated formula is a *relaxation* and its
UNSAT transfers:

- an 8-cycle blocking clause: a genuine solution is `C8`-free, so it does not
  contain that particular 8-cycle;
- a lazy cut clause: a genuine solution has `B+xy` 2-connected, so `(B+xy)-c`
  is connected for every `c`, so every bipartition of `V\{c}` is crossed;
- the symmetry-breaking constraints: the lex-maximum member of each
  relabelling orbit satisfies the constraint for every group element, and the
  genuine-solution set is closed under relabelling `{2,...,n-1}`. The lazy
  clauses above are satisfied by *all* labellings of a genuine solution (they
  are consequences of `C8`-freeness / 2-connectivity, which are isomorphism
  invariants), so adding them preserves that orbit-closure. Hence at least one
  representative of every orbit survives.

### Why SAT would be a proof too

SAT is only ever reported after the witness has been re-verified **from
scratch** by `verify_witness()`, using routines that share no code with the
encoding: `networkx` for the degree conditions, `xy`-absence, and
`nx.is_biconnected` on the closure, plus **two independent cycle detectors** —
`cycle_detect.has_cycle_len_dfs` (the repo's certified DFS detector) and
`networkx.simple_cycles` — which must agree. A candidate that fails
re-verification is reported as `BUG`, never as a survivor.

## 3. Validation (done before any prospective claim)

### 3.1 Exhaustive brute-force cross-check, with positive controls

`verifier/test_fcn_sat_existence.py` enumerates **all** graphs on `n` vertices
with `nauty-geng`, tries **every ordered pair** `(x,y)`, evaluates the
predicate directly, and compares with the solver's verdict.

The suite deliberately does **not** consist only of the settings of interest.
An over-constrained encoding with a bug would answer UNSAT everywhere and sail
through an all-UNSAT suite. So the parameters are varied — forbidden cycle set
`{4,8}` / `{4}` / `{8}`, internal degree floor 3 / 2, 2-connectivity required
or not — precisely so that many cases have genuine survivors and the solver
must *find* them.

**Result** (`verifier/test_fcn_sat_existence.py`, full run, `n = 5..9`):
**50 / 50 cases in exact agreement**, of which **23 returned SAT** with a
witness that passed independent re-verification. `nauty-geng` enumerated every
graph on up to 9 vertices (274,668 at `n=9`), every ordered `(x,y)` pair was
tried, and the SAT verdict matched the brute-force verdict in every case.
The `n=9` rows include the two settings of real interest:

| `n` | `d_x` | forbidden | internal deg | 2-conn | brute force | SAT solver |
|--:|--:|---|--:|---|---|---|
| 9 | 1 | `{4,8}` | 3 | yes | UNSAT | UNSAT |
| 9 | 1 | `{4}` | 3 | yes | **SAT** | **SAT** |
| 9 | 1 | `{4,8}` | 2 | yes | **SAT** | **SAT** |
| 9 | 1 | `{8}` | 3 | yes | **SAT** | **SAT** |
| 9 | 2 | `{4,8}` | 3 | yes | UNSAT | UNSAT |
| 9 | 2 | `{4}` | 3 | yes | **SAT** | **SAT** |
| 9 | 2 | `{4,8}` | 2 | yes | **SAT** | **SAT** |
| 9 | 2 | `{8}` | 3 | yes | **SAT** | **SAT** |

The bolded SAT rows are the point: the encoding is *not* trivially
over-constrained. Weaken any one ingredient and the solver immediately
produces a genuine, re-verified survivor.

Also checked: the cycle enumerator agrees exactly with `networkx.simple_cycles`
(count and content) on 300 random graphs at lengths 3,4,5,6,8; and symmetry
breaking never changes a verdict (every case re-run with it off).

### 3.2 Replaying the already-proven ground truth

`python verifier/fcn_sat_existence.py validate` re-decides every instance of
the two published results with no reference to their method, their search box,
`m_min`, or `ex(n;{C4,C8})`:

| series | source of truth | orders | expected | SAT solver |
|---|---|---|---|---|
| F9-F12 (`d_x=1`) | `f12_order12_result.md` | `n = 5..12` | UNSAT everywhere | **UNSAT everywhere** |
| FC-15 (`d_x=2`) | `fcn_order15_result.md` | `n = 5..15` | UNSAT everywhere | **UNSAT everywhere** |

Per-instance cost is trivial (`n=13`, `d_x=2`: 233 CEGAR iterations, 3,983
lazy `C8` clauses, 0.60 s), versus the 2,625,442 raw graphs that `n=15` alone
cost the `geng` pipeline.

**Exact agreement with both published results, at every order.**

## 4. Prospective results

### 4.1 The `(2,*)` series, `{C4,C8}` forbidden — where it breaks

`[COMPUTATIONALLY_VERIFIED]` at every row below. `x` is vertex 0 with
`d(x)=2` exactly, `y` is vertex 1 with `d(y)>=2`, all other degrees `>=3`.

| `n` | verdict | CEGAR iterations | lazy `C8` clauses | base clauses | wall time |
|--:|---|--:|--:|--:|--:|
| 5..13 | UNSAT (reproduces FC-15) | <=233 | <=3,983 | | <1 s |
| 14 | UNSAT (reproduces FC-15) | 523 | 9,767 | 11,386 | 2.2 s |
| 15 | UNSAT (reproduces FC-15) | 1,065 | 21,673 | 15,007 | 6.6 s |
| **16** | **UNSAT — new** | 2,138 | 47,629 | 19,410 | 19.5 s |
| **17** | **UNSAT — new** | 4,124 | 93,650 | 24,697 | 64.3 s |
| **18** | **UNSAT — new** | 7,626 | 175,821 | 30,976 | 297.9 s |
| **19** | **SAT — survivor** | 12,476 | 311,113 | 38,361 | 994.5 s |
| **20** | **SAT — survivor** | 16,327 | 464,104 | 46,972 | 2,422.3 s |
| **21** | **SAT — survivor** | 15,701 | 503,687 | 56,935 | 1,592.6 s |

So **`FC-18` is true and `FC-19` is false**. The frontier is exactly 18.

Note that `lazy_cut_clauses` is **0 on every single row**, including the UNSAT
ones. That means the loop never even reached a `C4`/`C8`-free candidate on
which to test 2-connectivity, so the formula actually refuted contains **no
connectivity constraints at all**. The UNSAT results are therefore *stronger*
than FC-n as stated:

> **`[COMPUTATIONALLY_VERIFIED]`** For `n <= 18` there is no simple graph on
> `n` vertices at all — connected or not — with one vertex of degree exactly 2,
> another non-adjacent vertex of degree `>= 2`, every other vertex of degree
> `>= 3`, and no `C4` and no `C8`.

### 4.2 The three survivors

| `n` | `m` | `m_min = ceil((3n-2)/2)` | degree-sum slack | graph6 |
|--:|--:|--:|--:|---|
| 19 | 28 | 28 | 1 | `RSPH@?OCGP?o?_?P?GW?_?AC?A_??w` |
| 20 | 30 | 29 | 2 | `SSPH@COC?P?_?`?__G_@??E??OW?B???k` |
| 21 | 31 | 31 | 1 | `TTP@@?OA?O_a@??g?O?AC?O??d??SO?@_??h` |

All three sit at or barely above the edge-count floor that the `geng` pipelines
derived, and the `n=19` and `n=21` cases carry their degree-sum slack on a
single internal vertex bumped to degree 4 — **exactly the odd-`n` shape that
`fcn_order15_result.md` records having accidentally filtered away once**. Had
this search assumed the naive "both terminals degree 2, everything else degree
3" shape, all three would have been invisible.

### 4.3 The `{C4,C8,C16}` version — the one the application needs

Every one of the three survivors **contains a `C16`**. They refute `FC-n` as
literally stated, but none of them is anywhere near a counterexample to
Erdős–Gyárfás. So the same search was re-run forbidding all powers of two that
fit (`4, 8, 16`):

| `n` | verdict, `{C4,C8,C16}` forbidden | CEGAR iterations | lazy clauses | wall time |
|--:|---|--:|--:|--:|
| 16 | **UNSAT** | 2,240 | 60,523 | 22.0 s |
| 17 | **UNSAT** | 4,148 | 192,362 | 100.5 s |
| 18 | **UNSAT** | 7,454 | 639,693 | 639.5 s |
| 19 | PLACEHOLDER_P2_19 |
| 20 | PLACEHOLDER_P2_20 |
| 21 | PLACEHOLDER_P2_21 |

Adding `C16` to the forbidden set costs roughly a further factor of 2 in wall
time per order (`n=18`: 639 s versus 298 s), because the lazy clause stream is
dominated by 16-cycles once the short ones are gone.

### 4.4 The `(1,*)` F-series, for comparison

The same solver run with `d_x = 1` (i.e. `F-n`, extending `F12`):

`[COMPUTATIONALLY_VERIFIED]`, forbidden set `{C4,C8}`:

| `n` | verdict | CEGAR iterations | lazy `C8` clauses | wall time |
|--:|---|--:|--:|--:|
| 5..12 | UNSAT (reproduces F9-F12) | <=112 | <=1,283 | <1 s |
| **13** | **UNSAT — new** | 281 | 4,355 | 0.45 s |
| **14** | **UNSAT — new** | 594 | 11,598 | 1.4 s |
| **15** | **UNSAT — new** | 1,202 | 27,598 | 5.0 s |
| **16** | **UNSAT — new** | 2,353 | 59,882 | 16.2 s |
| **17** | **UNSAT — new** | 4,414 | 119,280 | 62.1 s |
| **18** | **UNSAT — new** | 7,843 | 221,387 | 315.6 s |
| **19** | **UNSAT — new** | 13,802 | 395,328 | 1,470.7 s |
| 20 | PLACEHOLDER_DX1_20 |
| 21 | PLACEHOLDER_DX1_21 |

This is a substantial strengthening of `F12` on its own: the F-series survives
seven further orders past where `f12_order12_result.md` left it, and unlike the
`(2,*)` series it has **not** broken yet. `F19` raises the Type-A/Type-B
nontrivial-bridge order floor from `>=13` to `>=20`.

### 4.5 Cost model

Wall time grows by a factor of roughly 3.5-4 per order, and CEGAR iterations by
roughly 2 per order. `geng` growth over the same range was far worse (465 raw
graphs at order 12 to 2,625,442 at order 15, a factor of ~5,600 over three
orders); the SAT search covers those same three orders at a cost factor of ~55.
That is what made 16-21 reachable at all.

## 5. Auditing the survivors (the part that must not be got wrong)

A SAT solver reporting SAT is exactly where an encoding bug would be most
damaging, so each survivor was re-checked by `verifier/fcn_survivor_audit.py`,
which shares as little as possible with the search:

1. the graph is re-read **from its graph6 string**, not from the solver's
   model;
2. degrees, `xy`-absence, connectivity and `is_biconnected` via networkx;
3. `C4`, `C8` and `C16` by **four independent detectors**:
   - `cycle_detect.has_cycle_len_dfs` (the repo's certified DFS detector),
   - `networkx.simple_cycles`,
   - the compiled C batch detector `verifier/check_power_masks.c`, already
     certified in the F9-F12 and FC-15 pipelines,
   - a from-scratch bitmask dynamic program over simple paths, written for this
     audit and sharing no code with anything else;
4. the terminal pair is re-derived by `rooted_pair_survivors` **imported
   directly from `verifier/type_c_fcn_series.py`** — i.e. by the existing FC-15
   pipeline's own acceptance routine, with no reference to the SAT search.

**All four detectors agreed on all three cycle lengths for all three
survivors**, and the FC-15 pipeline's own routine accepts `(x,y) = (0,1)` in
every case. Verdict: the survivors are real. `FC-19`, `FC-20`, `FC-21` are
false as stated.

## 6. What this does and does not do for the order-32 target

**What it settles (negatively).** The reported Type-B reduction wants to
eliminate a `(2,2)`-piece of order `<= 21`. Section 4.1 shows that
**`C4`/`C8`-avoidance alone cannot do that**: explicit `(2,2)`-terminal,
`{C4,C8}`-free, 2-connected-closure pieces exist at orders 19, 20 and 21. Any
argument of the shape "extend FC-15 to FC-21 by more computation" is now known
to be attempting to prove something false. That is a real, if unwelcome,
narrowing — it redirects effort rather than consuming it.

**What may still work.** All three survivors contain a `C16`, so the
`{C4,C8,C16}` version (§4.3) is not refuted by them, and it is the version the
Erdős–Gyárfás application actually needs at these orders (`16 <= n <= 21`, where
`C16` is an admissible power-of-two cycle). §4.3 is where the order-21 target
actually lives.

**What is NOT claimed.** No consequence for the overall Type-B or Type-C order
bound is derived here. `fcn_order15_result.md` explicitly recorded overclaiming
that step once and correcting it; this file does not repeat the exercise. The
bridge-order arithmetic (`n >= b1 + b2 - 2` versus the gap analysis's
`n >= 2N+2` convention) is not reconstructed or reconciled here, and **this
file must not be cited for an `n >= 32` conclusion of any type.**

## 7. Honest limitations

### It is a decision procedure, not a structural proof

Like F12 and FC-15 before it, an UNSAT verdict says *no such graph exists*; it
does not exhibit a mechanism. `f12_order12_result.md` was explicit about the
same thing (F12 holds because the hypotheses are never simultaneously
satisfiable near the extremal edge count, not because a pendant vertex is shown
to force a cycle). Nothing here is `PROVED_IN_MARKDOWN`.

### The UNSAT proofs are not independently certified

The CDCL solver's UNSAT answer is taken on trust. This is the same trust level
as the geng pipelines (which trust `nauty-geng`'s generation completeness), but
it is worth naming. Mitigations actually run, rather than merely proposed:

1. exact agreement with exhaustive brute force at every order `<= 9`, including
   23 cases where a survivor exists and had to be found;
2. exact agreement with both published results (`F9`-`F12`, `FC-5`-`FC-15`);
3. agreement between different CDCL backends and between symmetry-breaking on
   and off;
4. an independent CP-SAT re-implementation (`verifier/fcn_cpsat_existence.py`)
   with a different engine and a different encoding of *every* constraint.

What is *not* done: emitting and checking DRAT/LRAT proof certificates. That is
the obvious next hardening step, and PySAT does not expose it for the backends
used here. Flagged, not claimed.

### `TIMEOUT` is not `UNSAT`

Any order reported `TIMEOUT` above is exactly that: the search did not
terminate inside its budget. It is *not* evidence for either answer, and must
not be read as "probably UNSAT" — the whole point of tabulating it separately.

## 8. Reproducing

```sh
# brute-force cross-validation incl. positive controls (slow at n=9)
python verifier/test_fcn_sat_existence.py --quick

# replay F9..F12 and FC-5..FC-15
python verifier/fcn_sat_existence.py validate --both-modes

# prospective sweep
python verifier/fcn_sat_existence.py sweep --dx 2 --from 16 --to 21 --time-limit 21600
```
