# central_bridge_triangle.md — Type T triangle: shared witnesses and paired central bridges

**Standing reminder, per project discipline.** Every proof below is a
hand-written Markdown argument, cross-checked computationally wherever
the claim is unconditional. Nothing here is proof-assistant formal
verification. Builds on `contraction_atoms.md` (triangle atom, Type N/T
dichotomy), `contraction_saturation.md` Part VII (Type T system),
`contraction_central_bridge.md` (CB1), `contraction_separator_integration.md`
(CB3′, Part VII), and `central_bridge_templates.md` (the frozen A/P/S
templates this file consumes by citation). Continues Parts I–XIII of the
current task; Part I is `central_bridge_templates.md`.

## Part II: Type T triangle setup — T2 vs T3, and external-neighbor distinctness

Let `T=\{a,b,c\}` span a triangle of `G`. By `M1` (`lemmas.md`), the
degree-`\ge4` vertices `H` form an independent set; since `T` is pairwise
adjacent, **at most one of `a,b,c` lies in `H`**. So exactly one of two
cases holds:

- **T2.** Exactly one of `a,b,c` is in `H` — say `\deg(c)\ge4`, `a,b`
  cubic.
- **T3.** None of `a,b,c` is in `H` — all three cubic.

**Every cubic triangle vertex has a well-defined external neighbour.**
Let `x\in T` be cubic, `\{p,q\}:=T\setminus\{x\}` its two triangle-mates.
`x` has exactly 3 edges; two go to `p,q` (triangle edges), so the third
goes to some vertex `x'`, automatically distinct from `p,q` (a simple
graph has no repeated edges) and hence `x'\notin T`. Call `x'` **`x`'s
external neighbour**.

**Lemma NA (no auxiliary adjacency) [cited, not re-derived].**
`contraction.md` III.1, applied to `x`'s own neighbour set `\{p,q,x'\}`
(with `pq` already an edge — the "exactly 1 internal edge" case there):
the proof shows directly that `xp,xq` are triangle edges and — quoted
exactly — *"`vc` has no common neighbour (`a,b` are the only candidates,
and — with exactly one internal edge `ab` — neither is adjacent to
`c`)"*. Substituting `v\to x,\ a,b\to p,q,\ c\to x'`: **neither `p` nor
`q` is adjacent to `x'`.** This is not new content — it is exactly what
III.1's own proof already established, restated in this file's notation
because Part IV below needs it explicitly.

### II.1. Lemma NE — no two cubic triangle vertices share an external neighbour [PROVED, new]

**Claim.** If `x,y\in T` are distinct cubic vertices, `z:=T\setminus\{x,y\}`
the third (cubic or not), then `x'\ne y'`.

**Proof.** Suppose `x'=y'=:w`. By the paragraph above, `w\notin T`, so
`w,x,y,z` are four distinct vertices. The following four edges all
exist: `xw` (`=xx'`), `wy` (`=yy'`, since `w=y'`), `yz` (triangle edge,
`y,z\in T`), `zx` (triangle edge, `z,x\in T`). These four edges, on the
four distinct vertices `x,w,y,z`, form the 4-cycle `x\text{-}w\text{-}
y\text{-}z\text{-}x}`. But `G` is `C_4`-free (`lemmas.md`: *"`G` a
counterexample `\Rightarrow` `G` has no 4-cycle"*). Contradiction. So
`x'\ne y'`. `\blacksquare`

**The proof never used `\deg(z)`** — it applies whether `z` is cubic or
in `H`, so it covers every pair in both T2 and T3 uniformly.

**Applying Lemma NE.**
- **T2**: the only cubic pair is `\{a,b\}`, giving `a'\ne b'`. (`c` has
  no single canonical "external neighbour" — it may have several,
  `\deg(c)-2\ge2` of them, none singled out by this lemma.)
- **T3**: all three pairs apply — `a'\ne b'`, `a'\ne c'`, `b'\ne c'`,
  using `z=c,b,a` respectively.

**Complete audit, as required.** `x'\notin T` is automatic (simple-graph
edge-distinctness, no proof needed beyond the neighbour count). The one
*nontrivial* possible equality — two cubic triangle vertices sharing an
external neighbour — is now eliminated in every case, T2 and T3 alike.
No other equality among `\{a',b',c'\}` (or between them and `T`) remains
to audit.

**Computational cross-check, implemented.**
`verifier/central_bridge_triangle.py` constructs the smallest gadget with
`a'=b'=w` forced and confirms by NetworkX cycle enumeration that the predicted
4-cycle is present, independently of the hand proof above.

## Part III: shared triangle-contraction witness

`T` is automatically a contractible atom (`contraction_atoms.md` III.1),
giving contracted vertex `t`, `\deg_{G/T}(t)=\sum_{v\in T}(\deg_G(v)-2)`:

- **T2**: `(3-2)+(3-2)+(\deg(c)-2) = \deg(c)\ge4`.
- **T3**: `1+1+1=3`.

**The triangle-pair lemma (III.2, cited).** For a power-of-two cycle `D`
of `G/T`, `|D|=2^k`, with forced-distinct attachment vertices `u,v\in T`
(the same forced-distinct-attachment step used throughout this
sequence): both `\boxed{2^k+1}` and `\boxed{2^k+2}` are realized in `G`,
**"using the identical outside arc `Q_{\text{out}}` and identical
attachment vertices `w_1,w_2`"** (quoted exactly) — call this common
outside arc **`Q`**. The **unused vertex** is `T\setminus\{u,v\}`, the
one triangle vertex carrying no attachment for this particular `D`.

### III.1. Symmetry orbits of the attachment pair, before any external/bridge data

**T2.** The three candidate pairs are `\{a,b\},\{a,c\},\{b,c\}`. The
labelling symmetry of the *bare* T2 setup (nothing yet known beyond "`a,b`
cubic, `c\in H`") is generated by the transposition `a\leftrightarrow b`
(order 2; `c` is fixed, being the unique non-cubic vertex, hence not
interchangeable with `a` or `b`). Orbits: `\{a,b\}` maps to itself
(fixed as a *set*, though the swap permutes which of `a,b` carries which
role) — **orbit of size 1**. `\{a,c\}\leftrightarrow\{b,c\}` — **orbit of
size 2**. **So `\{a,b\}` is not equivalent to `\{a,c\}`/`\{b,c\}`**,
exactly as the task requires.

**T3.** All three vertices are cubic, structurally interchangeable
before any external data is fixed: the full `S_3}` acts on `\{a,b,c\}`.
The three 2-subsets form a **single orbit of size 3** under `S_3`. **All
three pairs are equivalent** — exactly as the task requires.

**Symmetry-breaking convention, recorded once.** From Part IV onward,
external neighbours (`a',b',c'`) and bridge data are genuinely
asymmetric data layered on top of `T`; fixing a specific attachment pair
or a specific vertex's canonical witness is a choice (in the sense of
`contraction_atoms.md` V.1's definitional tie-breaking), made explicitly
where used, not a further case reduction.

**No further chord content.** `G[T]=K_3` supplies exactly the two simple
`u`-`v` paths already exhausted by III.2 (the direct edge, `r=1`, and the
through-the-third-vertex route, `r=2`) — there is nothing left to add
about chords specific to the attachment step.

## Part IV: per-vertex theta and central-bridge data — the three thetas are not independent

For cubic `x\in T` with mates `\{p,q\}=T\setminus\{x\}`: `x`, viewed as a
Type T vertex of `G` in its own right (`contraction_atoms.md` Part IV),
has **its own unique triangle exactly equal to `T`** (`pq` is the one
internal edge among `x`'s three neighbours) and unique nontriangle edge
`x`-`x'`. This is a direct instantiation — not an approximation — of
`contraction_saturation.md` Part VII's Type T system, with `v:=x`,
`\{a,b\}:=\{p,q\}`, `c:=x'` in that file's notation.

**Canonical `\Theta_x`** (`contraction_saturation.md` VII.2, cited):
poles `\{X_x,x'\}`, where `X_x\in\{p,q\}` is whichever mate the canonical
`xx'`-edge witness exits through (`contraction_atoms.md` V.1's
minimal-overlap definitional choice, applied to this edge); `P_0=X_x
\text{-}x\text{-}x'` (length 2, using triangle edge `xX_x` and external
edge `xx'`); `P_1`: the `xx'`-edge witness, `x'\to X_x`, length
`2^{\rho_x}-1`, avoiding `x`; `P_2`: the `N[x]`-witness `Q_{X_x,x'}`,
length `2^{s_x}`, avoiding `x`. Define `Y_x:=T\setminus\{x,X_x\}`, the
triangle-mate **not** used by `P_0`.

**Central bridge `B_x`** (`contraction_central_bridge.md` Part I): the
`\Theta_x`-bridge containing `x`'s third edge `e_x=x\text{-}Y_x`.

### IV.1. The triangle sits inside `\Theta_x` in exactly one of two ways [PROVED, new]

Since `Y_x,X_x\in T`, the triangle edge `Y_xX_x` exists in `G`.

- **(i) `Y_x\notin V(\Theta_x)`** (the generic case). `e_x` is not a
  chord; `B_x` is the component `C` of `G-V(\Theta_x)` containing `Y_x`.
  `C` has **two** boundary edges into `\Theta_x`, both visible directly
  from the triangle alone: `e_x=Y_x\text{-}x` (into the branch-internal
  vertex `x`) and the triangle edge `Y_x\text{-}X_x` (into the pole
  `X_x`). **Hence `\operatorname{att}(B_x)\supseteq\{x,X_x\}`,
  established directly from `T`'s own edges — sharper than CB1's generic
  `\ge2` bound**, which needs an S5/cut-vertex contradiction; here the
  second attachment point is pinned explicitly to a pole, no appeal to
  S5 required.
- **(ii) `Y_x\in V(\Theta_x)`** (`Y_x` lies on `P_1` or `P_2` — the
  triangle reconnects to its own near-power witness). Then `e_x` is a
  chord of `\Theta_x`; by CB1's chord case directly,
  `\operatorname{att}(B_x)=\{x,Y_x\}` exactly.

Both sub-cases give `|\operatorname{att}(B_x)|\ge2` with no separate
argument needed; (i) is the generic one used below.

### IV.2. MA2 output `\tau_x`, sharpened by the triangle structure [PROVED where stated]

Assume (i) and no further attachment (`\operatorname{att}(B_x)=\{x,X_x}`
exactly) — this is exactly **CB3′ case 1**
(`contraction_separator_integration.md` VI.2/VII), giving directly (T2,
Gao–Huo–Liu–Ma, cited): two simple `x`-`X_x` paths inside `B_x`, lengths
`\ell,\ell'`, `\ell'-\ell\in\{1,2\}`.

**Concrete sharpening, specific to this triangle setting [new].** `x`'s
*only* edge into `B_x` is `e_x=x\text{-}Y_x`; every `x`-`X_x` path inside
`B_x` therefore begins `x\text{-}Y_x\text{-}\cdots`. The path
`x\text{-}Y_x\text{-}X_x` (edge `e_x` then the triangle edge
`Y_xX_x`) has length exactly `2`, and no shorter `x`-`X_x` path inside
`B_x` can exist (any such path needs `\ge1` edge to leave `x` and `\ge1`
more to reach `X_x`, with equality realized by exactly this route).
**The shortest path length is `2` exactly**, but the original next inference
was invalid: T2 supplies *some* two paths whose lengths differ by 1 or 2; it
does not say that a globally shortest terminal path belongs to that pair.
Thus T2 does **not** license a second path of length `3` or `4` from the mere
existence of `x-Y_x-X_x`.

**Conditional anchored-detour lemma [PROVED, 2026-07-27 recovery].** Every
`x`-`X_x` path in `B_x` begins with the unique bridge edge
`xY_x`.  If the second path has length `3`, closing it with the triangle
edge `xX_x` gives a simple `C_4`.  If it has length `4`, delete its first
edge `xY_x`; the remaining simple `Y_x`-`X_x` suffix has length `3`, and
closing that suffix with the triangle edge `Y_xX_x` gives a simple `C_4`.
Thus lengths `3,4` are excluded from the anchored bridge spectrum.  This does
**not** eliminate the exact-two-attachment case: T2's admissible pair may
have larger lengths `L,L+\delta`, independently of the isolated length `2`.

**Full corrected anchored spectrum [PROVED, 2026-07-27 continuation].**
For any other bridge path `P=xY_x\cdots X_x` of length `L>2`, deleting the
forced prefix `xY_x` leaves a simple `Y_x`-`X_x` path of length `L-1` that
does not use `Y_xX_x`. Closing it with `Y_xX_x` gives a simple cycle of
length `L`; closing the full path with the separate triangle edge `xX_x`
gives a simple cycle of length `L+1`. The other nontrivial bridge at the
`\{x,X_x\}` cut, through `x'`, has route lengths `2^{\rho_x}` and
`2^{s_x}+1`. Therefore a T2 pair `\ell,\ell+\delta` guarantees exactly

\[
\begin{array}{c|cc}
&P_1&P_2\\ \hline
\text{suffix}+Y_xX_x&\ell&\ell+\delta\\
\text{full path}+xX_x&\ell+1&\ell+\delta+1\\
\text{near-power outside route}&\ell+2^{\rho_x}&\ell+\delta+2^{\rho_x}\\
\text{power outside route}&\ell+2^{s_x}+1&\ell+\delta+2^{s_x}+1.
\end{array}
\]

The two admissible paths need not be internally disjoint from each other, so
their union contributes no guaranteed cycle. The table has the explicit
infinite safe arithmetic family `\ell=2^t+1`,
`t>\max\{\rho_x,s_x,3\}`; hence it does not eliminate the case. The proof,
arithmetic classification, overlap audit, Heawood hypothesis table, and SPQR
scope are in `type_t_exact_two_a.md` and
`verifier/type_t_exact_two_a.py`. The subsequent whole-cut continuation
`type_b_compatibility.md` identifies this central bridge as one side of the
actual Type-B pair, maps the asymmetric spectrum of the component through
`x'`, and proves T9B without importing Type-A self-sum assumptions.

`verifier/type_t_r2_s2_audit.py` includes an explicit C4-free Heawood-based
bridge satisfying T2's degree and 2-connectivity hypotheses with terminal
path lengths `\{2,7,9,11,13,15\}`: the admissible pairs exist among the larger
lengths, while no length `3` or `4` path exists.  This is a direct regression
against the invalid inference, not an F-clean Type-T survivor: it has an
internal `C_8`, and its paths of lengths `7,15` close with `xX_x` to `C_8`
and `C_{16}`. The symbolic incidence and independent NetworkX checks are in
`verifier/type_t_r2_s2_audit.py`; the full recovery and scope audit is
`type_t_recovery_audit.md`.

**If `\operatorname{att}(B_x)` has a third point, the triangle reconnects
as the chord case IV.1(ii), or the 2-attachment
structure fails T2's 2-connectivity hypothesis internally** — CB3′ case
2 (S5) or case 3 (genuinely new `\ge3`-terminal network) applies instead,
exactly as catalogued in `central_bridge_templates.md`'s **S** output or
MA2's outcome 3. **Neither is ruled out by the triangle structure alone**
— this is not a gap introduced here, it is the same open item the prior
files already recorded, now confirmed to survive unchanged inside the
triangle setting.

### IV.3. The three thetas overlap — made precise, not assumed [PROVED]

If `X_x` happens to equal one of `x`'s triangle-mates that is **itself**
a cubic vertex under separate analysis (say `x=a`, `X_a=b`), then `B_a`'s
second attachment point is `b` itself — and `b`, in its own right, is
the branch-internal vertex of `\Theta_b`. **So `B_a`'s boundary touches
`\Theta_b`'s own branch point directly.** This is the precise, checkable
content behind the task's instruction not to treat `\Theta_a,\Theta_b,
\Theta_c` as independent: they do not merely happen to share the
ambient triangle `T` — one theta's bridge can attach exactly at the
vertex that anchors a different theta's own branch.

**Computational cross-check, corrected and implemented.**
`verifier/central_bridge_triangle.py` builds an explicit Type-T triangle
gadget, recomputes `\operatorname{att}(B_x)` by NetworkX component/boundary
calculation, and enumerates the terminal paths. The old fixture's length-4
path is now explicitly checked to contain the forced `C_4`; it is a negative
fixture, not an F-clean witness.

## Part V: central-bridge component sharing between two cubic triangle vertices

Fix two distinct cubic vertices `x,y\in T` (case (i) of IV.1 for both).
Each canonical witness independently selects `X_x\in T\setminus\{x\}`
and `X_y\in T\setminus\{y\}` — **4** combinations in T3 (`X_x\in\{y,z\}`,
`X_y\in\{x,z\}`, `z:=T\setminus\{x,y\}`); in T2 the same 4 combinations
occur with the role of `z` possibly played by the non-cubic vertex.

### V.1. The four `(X_x,X_y)` configurations [PROVED classification]

| `X_x` | `X_y` | `Y_x` | `Y_y` | `e_x` | `e_y` |
|---|---|---|---|---|---|
| `y` | `x` | `z` | `z` | `x\text{-}z` | `y\text{-}z` |
| `y` | `z` | `z` | `x` | `x\text{-}z` | `y\text{-}x` |
| `z` | `x` | `y` | `z` | `x\text{-}y` | `y\text{-}z` |
| `z` | `z` | `y` | `x` | `x\text{-}y` | `y\text{-}x` |

**The last row is the distinguished case: `e_x=e_y=xy`, literally the
same edge of `G`.** This happens exactly when *both* `x`'s and `y`'s
canonical witnesses exit through the *third* vertex `z` — not, as an
earlier informal pass at this problem mis-stated it, when they "point at
each other." Both attaching structures start from the identical edge
`xy`, so `B_x` and `B_y}`, restricted to their first step, coincide
exactly; whether they coincide *entirely* is Part V.2 below. The middle
two rows are mirror images of each other (swap `x\leftrightarrow y`); the
first row is the case where `e_x,e_y` are two different edges (`xz,yz`)
that nonetheless share the endpoint `z`.

### V.2. Resolving the task's 6 possibilities honestly

- **(1) Disjoint.** Realized in the first three rows of V.1 whenever the
  external components `C_x\ni Y_x`, `C_y\ni Y_y` (beyond the shared
  triangle vertex itself) have no further common vertex — genuinely
  possible, not excluded by anything proved so far.
- **(2) Same component.** Requires `C_x=C_y` as vertex sets — only
  possible in the last row (`e_x=e_y=xy`, so `Y_x=y,Y_y=x` are each
  other's start, and `B_x,B_y` both begin at the identical edge); whether
  the *rest* of the component coincides is external information this
  file does not have. **Realizable as a special case of row 4, not
  provable in general.**
- **(3) Distinct but meet at an attachment.** Realized whenever
  `X_x=y` or `X_y=x` (rows 1–3): the attachment vertex `X_x=y` is
  simultaneously `\Theta_y`'s own branch-internal vertex (Part IV.3) —
  `B_x` and `\Theta_y` meet at `y` even when `B_x\ne B_y` as sets.
- **(4) One contains the other's external neighbour.** E.g. `x'\in C_y}`
  — genuinely possible (nothing rules it out), and genuinely
  **independent of the `(X_x,X_y)` table above**, since `x'` sits outside
  `T` entirely; not resolved by the triangle structure alone.
- **(5) Share an internal block but not the full component.** Would
  require `C_x,C_y` to meet at a cut vertex of their union without being
  identical throughout — a block-cut-tree question about the *external*
  graph beyond `T`, genuinely open, not decidable from `T`'s local data.
- **(6) Attachment sets interlace.** Would require a *further*, larger
  ambient block containing both `\{x,X_x\}` and `\{y,X_y\}` as
  crossing 2-cuts — again a question about structure beyond what `T`
  and its two thetas pin down; open.

**Which are proved distinct.** (1)/(2)/(3) are pairwise distinct and
each concretely realized or ruled compatible by the `(X_x,X_y)` table
above — this is the part of the classification the triangle's own local
structure actually settles. **(4)/(5)/(6) are not shown distinct from
each other or from (1)–(3)** in general — they depend on external graph
structure this file has no handle on; recorded as open, not forced into
a false resolution.

**The key nuance, resolved as promised.** Sharing a vertex outside both
theta systems (e.g. `z` in row 1, or `y` itself in rows 2/3 as `X_x`)
does **not** force `B_x,B_y` to be the literal same connected component:
`B_x` is defined relative to `G-V(\Theta_x)`, `B_y` relative to
`G-V(\Theta_y)` — different ambient deletions in general — so a vertex
common to both boundary structures need not make the two *bridges*
identical as objects, only *adjacent* or *touching*. Row 4 of V.1 is the
only configuration this file can point to where full coincidence is even
possible, and even there it is not forced.

### V.3. Canonical joint encoding

Per the task's request, the joint state of a Type T triangle vertex pair
`(x,y)` is now fully encoded by the tuple
\[
\big(\text{T2 or T3};\ \{x,y\}\text{'s orbit label (III.1)};\ (X_x,X_y)
\text{ row of V.1};\ \tau_x,\tau_y\in\{A,P,S\};\ \text{V.2 sharing
type (1)–(6), if determined}\big).
\]
This is exhaustive at the level this file resolves it: T2/T3 (Part II),
orbit label (Part III), `(X_x,X_y)` row (V.1, always exactly one of the
4), `\tau_x,\tau_y` (Part IV.2, each independently A/P/S per
`central_bridge_templates.md`), and the V.2 sharing type **when it is
determined by local data** (rows 2–3 pin down (2)/(3) partially; row 1
and any of (4)–(6) require external information not fixed here).
