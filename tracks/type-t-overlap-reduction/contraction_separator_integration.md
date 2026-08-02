# contraction_separator_integration.md — separators, admissible paths, and Type T integration

**Standing reminder, per project discipline.** Every proof below is a
hand-written Markdown argument, cross-checked computationally wherever
the claim is unconditional. Nothing here is proof-assistant formal
verification. Builds on `contraction_central_bridge.md` (CB1, the
endpoint-return normal form, the topological-K4 reduction) and cites
`two_cut.md`'s T1–T5 and `lemmas.md`'s S5 directly, without re-deriving
them.

## Part VI: the block-or-separator lemma inside `B_v` — CB3, refined

**The task's proposed CB3 is not quite the sharpest correct statement.**
Working through the cases carefully finds the *real* dichotomy is
sharper, with a genuinely new third case the original formulation did
not name. This is presented as **CB3′**, the strongest correct
replacement, per the task's own instruction to prefer this over forcing
an incorrect formulation.

### VI.1. `\{v,x\}` is a genuine 2-cut of `G` exactly when `\operatorname{att}(B_v)=\{v,x\}` [PROVED]

If `\operatorname{att}(B_v)=\{v,x\}` exactly, `B_v`'s component `C`'s
only edges leave to `\Theta}` (landing only on `v,x`, by hypothesis) or
stay inside `C` (definition of "component of `G-V(\Theta)`"; no edge
reaches a *different* component of `G-V(\Theta)` directly,
`contraction_central_bridge.md` V.1). So `G-\{v,x\}` disconnects `C`
from everything else (`\Theta\setminus\{v,x\}` and every other bridge)
— **`\{v,x\}` is a genuine 2-cut, and `B_v` (`=C` plus its edges to
`v,x`) is literally one of `two_cut.md`'s "nontrivial `xy`-bridges" at
that cut**, with `x,y` relabelled `v,x` here.

### VI.2. CB3′ — the two genuine failure modes [PROVED]

**A useful bonus fact, reused below:** `v` itself can never be `G`'s
S5-exceptional cut vertex (`v` is cubic, `\deg_G(v)=3`, while S5 forces
every cut vertex to have degree exactly 4).

**CB3′.** *Exactly one of the following holds:*

1. **`\operatorname{att}(B_v)=\{v,x\}` exactly, and neither `x` nor any
   internal vertex of `B_v` is `G`'s (at most one, by S5) cut vertex.**
   Then `K(v,x):=B_v` qualifies as a genuine `two_cut.md`-bridge at the
   2-cut `\{v,x\}`, and **T1** (`B_v+vx` is 2-connected) and **T2**
   (`\Lambda(B_v)` contains 2 admissible `v`-`x` path lengths, differing
   by 1 or 2, citing Gao–Huo–Liu–Ma) apply **by direct citation, with no
   new proof needed** — both of CB3's required properties hold exactly.
   *Why the citation is valid without re-proving 2-connectivity of `G`
   itself:* T1/T2's own proofs need only "`G-x` connected" and "`G-z}`
   connected for internal `z\in C`" — and since `G` has at most one cut
   vertex (S5) and neither `x` nor any internal `B_v`-vertex is assumed
   to be it (this case's hypothesis), both facts hold regardless of
   whether `G` is fully 2-connected or has its one S5 exception
   *elsewhere* in the graph.
2. **A cut vertex covered by S5.** `\operatorname{att}(B_v)=\{v,x\}`
   exactly, but `x` or some internal `B_v`-vertex *is* `G`'s S5
   cut vertex. T1/T2's proofs break exactly where they cite "`G-x`
   connected"/"`G-z}` connected" — this is precisely the case S5 already
   classifies exhaustively (equal-order lobes, degree 4 at the cut
   vertex), no new theorem needed, but genuinely a distinct outcome from
   case 1, not folded into it.
3. **A genuinely new multi-attachment case, not covered by S5 or by
   Type A/B/C [the actual smallest obstruction to the task's original
   CB3].** `\operatorname{att}(B_v)` has **`\ge3`** elements. Restricting
   to any 2 of them as terminals `(v,x)` necessarily *excludes* the
   other attachment point(s) `y`; any internal `C`-vertex with an edge to
   an excluded `y` **loses that edge** in the 2-terminal picture — a
   genuine internal-degree loss, breaking T2's degree hypothesis
   *structurally*, not via a cut vertex or a 2-cut at all (`Type A/B/C`
   is inherently a **2-terminal** classification; a `\ge3`-attachment
   bridge is not a 2-cut bridge in that sense in the first place —
   citing Type A/B/C here would misapply it, exactly the caution the
   task's audit anticipated). **Resolving this case would require
   treating `B_v` as a genuine `\ge3`-terminal network, outside this
   project's existing 2-terminal machinery entirely** — recorded as the
   precise open extension, not attempted.

**Audit, as required.** *Articulations inside `B_v`*: covered by T1's
own proof (adding `vx` merges every piece, so no *internal* articulation
survives in case 1 — no separate block-cut-tree search is needed once
T1 applies). *Leaf blocks with no theta attachment*: irrelevant to
`K(v,x)+vx`'s 2-connectivity once T1 applies (T1 shows there are none
once `vx` is added). *Leaf blocks with one or several attachments*: this
is exactly what distinguishes case 1 (exactly `v,x`, both present) from
case 3 (extra attachments beyond `v,x`). *Attachment vertices with edges
into multiple blocks*: the source of case 3's degree loss. *Loss of
internal degree*: proved to occur exactly in case 3, and *only* there —
cases 1–2 preserve full internal degree (T2's citation is unconditional
on this point once `\operatorname{att}(B_v)=\{v,x\}` is fixed).

**Computational cross-check.** `verifier/separator_integration.py`'s
`check_cb3_cases` builds one explicit gadget per case (clean 2-attachment,
S5-cut-vertex-coincident, and 3-attachment) and confirms directly:
case 1's `B_v+vx` is 2-connected (via networkx) and every internal
vertex retains degree `\ge3`; case 3 exhibits the exact degree-loss
phenomenon at the vertex touching the third attachment point when
restricted to just two terminals.

## Part VII: admissible central paths

**Only in CB3′ case 1** does T2 apply, giving **two** `v`-`x` paths of
lengths `\ell` and `\ell'\in\{\ell+1,\ell+2\}` (T2's exact conclusion,
cited).

### VII.1. Paired topological-`K_4` systems

Both admissible paths, substituted into the interior-return construction
(`contraction_central_bridge.md` IV), give two topological-`K_4`
subdivisions sharing the **same** `p,q,x` and the same `M,N,d` — differing
*only* in the `vx` branch length (`\ell` vs `\ell'`). **The three
`M,N`-only formulas (`N+2`, `M+N`, `M+2`) are identical in both systems
and remain unconditionally safe** (Lemma E/F/parity, unchanged from
`contraction_central_bridge.md` IV.2). The four `\ell`-dependent
formulas each appear **twice**, once per system (`\ell` and `\ell'`),
giving up to 8 distinct symbolic conditions (fewer if some coincide
numerically) — genuinely more constraints, but not automatically
resolved by pure arithmetic (consistent with IV.2's own scope note).

**The genuinely new content: the union of the two central paths
themselves.** If the two admissible `v`-`x` paths `R,R'` (lengths
`\ell,\ell'`) are internally disjoint (a clean pair, in the sense of
`contraction_atoms.md`'s toolkit), their union is a simple cycle *not
using any theta branch at all*, of length `\ell+\ell'`:

- **`\ell'=\ell+1`:** `\ell+\ell'=2\ell+1`, **odd, hence never a power
  of two — unconditionally safe, regardless of `\ell`.**
- **`\ell'=\ell+2`:** `\ell+\ell'=2\ell+2=2(\ell+1)`, a power of two
  **iff `\ell+1` is itself a power of two, i.e. `\ell=2^j-1` for some
  `j`.** This is a genuine, nontrivial excluded family: **if the two
  admissible paths differ by 2 and are internally disjoint, `\ell`
  cannot be one less than a power of two** (`\ell\ne3,7,15,31,\dots`) —
  else `\ell+\ell'` is itself a forbidden cycle length, an immediate
  contradiction.

**If `R,R'` are *not* internally disjoint,** their symmetric difference
decomposes via `contraction_intersections.md`'s cell machinery instead
of the clean formula above — not re-derived here, but directly
applicable by citation.

**Computational cross-check.** `check_paired_k4_union` brute-forces
`2\ell+1` (always safe, confirmed over `\ell\in\{2,\dots,20\}`) and
`2\ell+2` (confirmed to hit a power of two exactly at
`\ell\in\{3,7,15,\dots\}` within the tested range, matching `2^j-1`
exactly) against direct power-of-two testing.

## Part VIII: cross-branch versus separator dichotomy

### VIII.1. The dichotomy, and a sharp `pq`-edge consequence [PROVED]

**Claim.** *If no `\Theta`-bridge has attachments on two different
branches, then removing `\{p,q\}` separates the interiors of the three
theta branches.* *Proof.* Each branch's interior vertices connect only
to: other vertices of the same branch, the poles `p,q`, or bridges
attached to *that same branch alone* (the hypothesis excludes cross-branch
attachments). So `G-\{p,q\}` leaves each branch's interior (plus its own
private bridges) as a self-contained piece, disjoint from the other two
branches. ∎ This makes `\{p,q\}` a genuine 2-cut with (up to) **three**
nontrivial bridges — `P_0` (the `v`-branch, together with `B_v` and any
other private bridges), `P_1`'s piece, `P_2`'s piece.

**Mapping to T4's exact classification [PROVED, direct citation].**
`P_0` alone (before attaching `B_v`) already has `a_0=b_0=1}` (its only
edge from `p` is `pv`, from `q` is `qv`) — matching the `a_i=1` pattern
T4 requires of *every* bridge in the `t=3` (**Type A**) case. **If
`pq\in E(G)` *and* the theta genuinely has 3 separate non-cross-branch
bridges, this is already excluded by T4's own proof**: T4 shows directly
that `t=3` nontrivial bridges together with an `xy` edge is impossible
(retaining any 2 bridges plus the edge already reaches degree 3 at both
terminals, contradicting minimality — `two_cut.md` §2c). **So: if
`pq\in E(G)`, some `\Theta`-bridge must be cross-branch** — a clean,
sharp, citation-based necessary condition, not merely "the separator
machinery applies."

**If `pq\notin E(G)`,** the no-cross-branch case is **exactly Type A**
(`t=3`, `xy\notin E(G)`, `a_1=a_2=a_3=1`, `q_1=q_2=q_3=3` — `two_cut.md`
§2c) — a case this project has *already* mapped exhaustively in
`s6_case_tree.md`: Type A's dependency chain is "a self-sum is dyadic →
its two paths overlap (proved) → **first unproved: the deliberately
deferred T7 overlap implication**," or, on the clean branch, "the needed
bridge is self-sum-clean → T3/T5 force balance/maximality → SP-eligible
leaf forms → rigid-forced and minimal → **first unproved: LR\*}**." This
is cited exactly, not merely gestured at.

**Central bridge `B_v` is cross-branch exactly when Part VI's `x` is
interior to `P_1` or `P_2`** (Part IV's interior-return case) — endpoint
return (`x=p` or `q`, Part III) keeps `B_v` attached only to `P_0`'s
poles, **not** cross-branch in this Part VIII sense (both its
attachments are still theta *poles*, not branch interiors) unless a
*further* attachment beyond `\{v,x{=}p\}` exists (case 3 of CB3′).

### VIII.2. Exact separator spectra [PROVED skeleton; full resolution open]

In the Type A outcome, the three terminal path-length spectra supplied
by the branches are (at minimum) `\{2\}` (`P_0` alone, before folding in
`B_v`'s own contribution — see below), `\{M\}=\{2^r-1\}`, `\{N\}=\{2^s\}`
(substituting the NPT lengths where applicable). **`P_0`'s *true* spectrum
`\Lambda_0` is not simply `\{2\}`** once `B_v` is accounted for: if
CB3′ case 1 holds, T2 supplies a *second* `v`-`x` path — but this only
enlarges `\Lambda_0` if `x=q` (an endpoint-return coincidence with `P_0`'s
*own* far pole) or if `B_v` itself, combined with `P_0`'s edges, creates
new `p`-`q` routes; in the generic interior-return case (`x` internal to
`P_1` or `P_2`), `B_v`'s paths do **not** directly enlarge `\Lambda_0}`
(they create the cross-branch topological-`K_4}` structure of Parts
IV/VII instead, a different kind of object than a simple `p`-`q}`
alternative route). **Fully determining `\Lambda_0}` in general, and
hence definitively placing this configuration into T3/T5's "dirty
self-sum," "already eliminated," or "deferred overlap" cases, requires
resolving exactly which of Parts III/IV/VII applies — this is not
completed as a single closed-form answer here**, honestly reported
rather than asserted. What *is* established: the mapping target
(Type A, `s6_case_tree.md`'s exact dependency chain) is named precisely,
not left as "the separator machinery applies."

## Part IX: Type T multi-vertex triangle interaction — setup only

`H` independent `\Rightarrow` every triangle has `\ge2` cubic vertices
(`contraction_atoms.md` VII.2 / `contraction_saturation.md` VII.3,
already noted, not re-derived). For each cubic triangle vertex `v_i`:
its own canonical theta, central bridge `B_{v_i}}`, second attachment,
and CB3′-case classification (endpoint return / interior return /
multi-attachment) are each individually well defined by Parts I–VI
above, **applied vertex-by-vertex**. **The joint analysis this task
identifies as highest-priority** — whether two different cubic
vertices' central bridges share a component, share a theta attachment,
cross each other, or induce the same or distinct topological-`K_4`
subdivisions sharing the triangle — **is not carried out in this
pass.** This requires combining `contraction_intersections.md`'s
non-clean intersection machinery with *two* independently-chosen
central bridges simultaneously, a genuinely new combination not reached
by any single-vertex analysis on record. Recorded here as the precise,
named next step, exactly matching this file's own instruction not to
reduce it to single-vertex arithmetic — no such reduction is claimed.

## Part X: limited computation

**No `q=4` census, no broad graph regeneration.** Computation in this
pass is limited to exactly what Part X of the task permits: verifying
CB3′'s three cases on explicit constructed gadgets; the paired-`K_4`
union arithmetic (`2\ell+1`, `2\ell+2`); and confirming (by direct
inspection of `manifests/`, not regeneration) that no existing project
artifact contains central-bridge or CB3′-relevant examples — the
existing `data/`/`manifests/` artifacts remain from the defect-three
phase (bounded-order exhaustive census for `q\le3}`), structurally
unrelated objects to the theta/bridge constructions introduced across
this and the preceding four contraction-phase files; no mining of them
was attempted or is claimed.

## Part XI: honest stopping-condition assessment

**None of outcomes 1, 2, 3, 4, 7, or 8 is reached.** Central
endpoint-return is not eliminated (Part III ends in a normal form, not a
contradiction). Central interior-return is not eliminated (Part IV/VII
end in a theorem table with open symbolic conditions, not a
contradiction). Not every canonical theta reduces to the `\{p,q\}`
separator case (VIII.1 shows this is *conditional* on no bridge being
cross-branch, and `B_v` itself is frequently cross-branch by
construction whenever the interior-return case applies). Not every
canonical theta reduces to *one* paired topological-`K_4}` configuration
(both endpoint-return and the CB3′ case-2/3 failure modes remain live
alternatives). Neither Type N nor Type T is eliminated.

**Closest matches, stated precisely rather than rounded up:**
- **A genuine instance of outcome 6** (one exact block-cut-tree
  obstruction): **CB3′'s case 3** (`|\operatorname{att}(B_v)|\ge3`) is
  exactly this — a precisely identified, smallest exact obstruction to
  the task's originally-proposed CB3, not covered by S5 or by the
  existing 2-terminal Type A/B/C machinery, requiring a genuinely new
  `\ge3}`-terminal treatment to resolve.
- **A partial instance of outcome 5** (irreducible bridge itinerary):
  `contraction_central_bridge.md` V.2's structural (non-canonical)
  two-excursion instance, still standing as the best available example,
  neither proved minimal nor excluded.
- **No instance of outcome 4**: the paired-`K_4}` systems of Part VII
  are *not* shown to be the single configuration every remaining case
  reduces to — they are one concrete family among several live cases
  (endpoint-return, CB3′ cases 2–3, the Type A separator outcome of
  Part VIII).

**Concrete named next steps, not a vague list:** (1) VIII.2's full
determination of `\Lambda_0}` (`P_0`'s true path-length spectrum once
`B_v}` is folded in), needed to place the Type A separator outcome
precisely into `s6_case_tree.md`'s "dirty self-sum / eliminated /
deferred" trichotomy; (2) CB3′'s case 3, the `\ge3`-terminal network
extension; (3) Part IX's joint two-central-bridge analysis at a shared
Type T triangle, identified (again) as the single highest-value
remaining target across this entire five-file contraction-phase
sequence.
