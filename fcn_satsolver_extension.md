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

PLACEHOLDER_RESULT_SUMMARY

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

PLACEHOLDER_BRUTEFORCE

Also checked: the cycle enumerator agrees exactly with `networkx.simple_cycles`
(count and content) on 300 random graphs at lengths 3,4,5,6,8; and symmetry
breaking never changes a verdict (every case re-run with it off).

### 3.2 Replaying the already-proven ground truth

PLACEHOLDER_GROUNDTRUTH

## 4. Prospective results

PLACEHOLDER_SWEEP

## 5. Honest limitations

PLACEHOLDER_LIMITS

## 6. Reproducing

```sh
# brute-force cross-validation incl. positive controls (slow at n=9)
python verifier/test_fcn_sat_existence.py --quick

# replay F9..F12 and FC-5..FC-15
python verifier/fcn_sat_existence.py validate --both-modes

# prospective sweep
python verifier/fcn_sat_existence.py sweep --dx 2 --from 16 --to 21 --time-limit 21600
```
