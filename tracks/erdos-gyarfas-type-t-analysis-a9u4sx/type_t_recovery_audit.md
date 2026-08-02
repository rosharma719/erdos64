# Type-T interrupted-session recovery and R2/S2 audit

**Status.** Hand-written proof, independently reproduced by finite symbolic
incidence accounting and a NetworkX local realization.  This is not
proof-assistant formal verification.  No literature-novelty claim is made.

## 1. Forensic state

The first checkout inspected was clean but on the wrong branch,
`codex/global-core-z3-lifts` at `a5af13de03d216b3e823eb06803198ffef29c6da`.
The expected branch existed as the remote-tracking ref and was checked out by
creating the missing local tracking branch; no reset, rebase, file discard, or
force operation was used.

The authoritative state before this audit was:

| item | recovered value |
|---|---|
| branch | `claude/erdos-gyarfas-handoff-l6tqlo` |
| HEAD | `d00fdac45cf85913f637c119d7a8a989aec0a8ee` |
| upstream HEAD | `d00fdac45cf85913f637c119d7a8a989aec0a8ee` |
| worktree | clean; no modified, staged, or untracked files |
| interrupted work committed? | no identifiable interrupted R2/S2 work; `d00fdac` is an earlier reconciliation/citation audit |
| commits after `1363d21` | only `d00fdac Reconcile and audit concurrent Type T work` |
| `ae64585` ancestor of HEAD | yes |
| `1363d21` ancestor of HEAD | yes |

Because both index and worktree diffs were empty, there was no interrupted diff
to save in `recovery/interrupted_work.patch` or
`recovery/interrupted_staged.patch`.  `/tmp/test_degree_forcing.py` did not
exist.  No recent `/tmp` file contained the interrupted work.  The only
repository-related scratch file found outside the 12-hour window,
`/tmp/erdos-audit.diff`, belongs to a different C++ intersecting-family
repository and contains no Type-T evidence.  The exact scratch claim and its
code are therefore not recoverable; only the committed candidate and the
visible activity description can be audited.

## 2. Authoritative dependency graph

The committed proof chain used here is:

```text
minimal counterexample: delta(G)>=3 and no C4/C8/...; M1; S5
  |
  +-- two_cut.md T1/T2 and bridge-spectrum identity
  |     +-- a 2-cut bridge has two admissible terminal paths
  |     `-- distinct bridges have power-free cross-sums
  |
  +-- contraction_saturation.md VII.2
  |     `-- each cubic Type-T vertex x has Theta_x with
  |         poles X_x,x', branches 2, 2^rho_x-1, 2^s_x
  |
  +-- contraction_central_bridge.md CB1
  |     `-- the bridge carrying xY_x has at least two attachments
  |
  +-- contraction_block_cut_tree.md MA1/MA2
  |     `-- A (admissible pair), P (shared port), or S (S5 leaf)
  |
  +-- central_bridge_templates.md
  |     `-- normalized A/P/S arithmetic
  |
  +-- central_bridge_triangle.md II-IV
  |     +-- T2/T3 and distinct external neighbours
  |     `-- if att(B_x)={x,X_x}, a shortest path has length 2;
  |         separately, some admissible pair has difference 1 or 2
  |
  +-- central_bridge_triangle_s5.md VI-IX
  |     `-- double-S/mixed-S and A/P pair matrix
  |
  +-- central_bridge_triangle_final.md X
  |     `-- identical or one-common triangle-anchored terminal pairs
  |
  `-- central_bridge_triangle_addendum.md
        +-- double-S leaves coincide literally
        `-- length 3/4 detours are conditionally excluded, but T2
            never supplied either detour
```

The audit separates two issues: a claimed length-3/4 path would force a
`C_4`, but the committed proof never validly obtained either path from T2.
T2's admissible pair need not contain the shortest terminal path.

## 3. Exact recovery of the R2/S2 notation

The labels in this section are path labels from
`central_bridge_triangle_final.md`, not `two_cut.md` section 21's unrelated
SPQR lemma `R2`, and not `lemmas.md`'s unrelated theorem `S2`.

Fix two distinct cubic vertices `x,y` of a Type-T triangle
`T={x,y,z_0}`.  In the one-common-terminal row

\[
X_x=X_y=z_0,\qquad Y_x=y,\qquad Y_y=x.
\]

For `x`, the canonical theta `Theta_x` has poles `{z_0,x'}` and branches

- `z_0-x-x'`, length `2`;
- an `x'`-`z_0` path of length `2^{rho_x}-1`;
- an `x'`-`z_0` path of length `2^{s_x}`.

Its central bridge `B_x` contains the triangle edge `xy`, has the pinned
gateway/attachment pair `{x,z_0}` in the audited A case, and contains:

- `R_1=x-y-z_0`, length `2`;
- `R_2`, a purported second simple `x`-`z_0` path, committed first as length
  `3` or `4`, then pinned by `1363d21` to length `4`. Its existence was not
  proved: T2 supplied an unspecified admissible pair, not a mate for `R_1`.

Symmetrically `Theta_y` has poles `{z_0,y'}`, `B_y` has attachments
`{y,z_0}`, `S_1=y-x-z_0`, and `S_2` was the second length-4
`y`-`z_0` path.  Lemma NE gives `x'!=y'`.  The selected
triangle-contraction pair and its common outside arc `Q` are independent of
this local A/A row and are not used in the correction.

The committed conditional candidate concatenated `R_2`, reverse `S_2`, and
the edge `xy`, assigning length

\[
1+ell_x'+ell_y'=1+4+4=9.
\]

Before the addendum, a mixed `3,4` choice made the same formula equal `8`.
Neither formula describes a simple cycle: every `R_2` starts with `xy` and
every `S_2` starts with `yx`, so `x`, `y`, and the edge `xy` are repeated.
With otherwise-disjoint tails, the edge symmetric difference plus `xy` is a
`C_7`, not a `C_9`; this observation alone is not the elimination.

## 4. Conditional anchored-detour lemma and the upstream inference failure

**Lemma (length-3 and length-4 anchored detours are impossible) [PROVED].**
Let `T={x,X,Y}` be a triangle in an `F`-clean graph, and let `B` be a central
bridge with `att(B)={x,X}` such that `xY` is the only edge of `x` in `B`.
If a second simple `x`-`X` path in `B` has length `3` or `4`, then `G`
contains a `C_4`.

*Proof.*  The short path has length `2`; hence the second path `P` has length
`3` or `4`.  Because `xY` is the only `B`-edge at `x`, `P` begins with
`xY`.

- If `|P|=3`, `P` plus the triangle edge `xX` is a simple cycle of length
  `4`.
- If `|P|=4`, delete the first edge `xY` from `P`.  The remaining suffix is
  a simple `Y`-`X` path of length `3`; it is internally disjoint from the
  triangle edge `YX`, so their union is a simple cycle of length `4`.

Both contradict `F`-cleanness. Therefore neither purported `R_2` nor `S_2`
exists with the committed length. QED.

This does **not** eliminate the exact-two-attachment anchored A branch. The
cited theorem says only that the spectrum contains two values differing by 1
or 2. From the independent fact `2 in Lambda_x`, the committed proof
incorrectly concluded that those values were `2` and `3` or `4`. A spectrum
such as `{2,7,9}` satisfies the actual conclusion using `7,9`.

The independent checker gives a concrete regression: subdivide an edge of the
Heawood graph, attach terminal `x` to the subdivision vertex `Y`, and take the
other endpoint as `X`. The closure `B+xX` is 2-connected, all internal
vertices have degree at least 3, and `B` is `C_4`-free. Its complete terminal
path-length set is `{2,7,9,11,13,15}` and its admissible pairs are
`(7,9),(9,11),(11,13),(13,15)`—none includes `2`. The fixture contains a
`C_8`, so it is not an F-clean Type-T survivor; it refutes the theorem
inference under the theorem hypotheses plus the locally used C4-freeness.

## 5. Degree-forcing audit

The visible activity's degree-forcing idea can be reconstructed only after
the path definitions are recovered.  In the one-common-terminal row, cubicity
gives

\[
N(x)={y,z_0,x'},\qquad N(y)={x,z_0,y'}.
\]

If the impossible length-4 paths are nevertheless written symbolically, their
only possible first two steps are

\[
R_2=x-y-y'-r-z_0,\qquad
S_2=y-x-x'-s-z_0.
\]

Thus cubic degree forces the already-existing external edges `yy'` and
`xx'`; it does not force a new edge.  The scope is universal because it uses
the full degree-three neighbourhoods of `x,y`, not degrees measured in a
partial gadget.  The intermediate vertices `r,s` need not be distinct from
each other, and central-bridge component sharing can add incidences at them;
none of this affects the two individual cycles

\[
y-y'-r-z_0-y,\qquad x-x'-s-z_0-x.
\]

Each is already a simple `C_4` by simplicity of its own path. Outside edges
cannot repair the contradiction. This refutes the committed length-4
candidate, not the broader exact-two-attachment A branch with unspecified
larger admissible paths. S5's degree-four cut vertex is irrelevant.

The lost script, if it existed, could at most have checked one constructed
gadget.  Such a gadget would not prove the forcing statement.  The independent
checker added by this audit instead derives the forced incidence from the
symbolic cubic neighbourhood and separately realizes the complete local
two-theta incidence in NetworkX.

## 6. Cycle audit and independent computation

`verifier/type_t_r2_s2_audit.py` performs two checks:

1. **Symbolic incidence enumeration.**  It exhausts `ell'=3,4`, constructs
   the corresponding forced `C_4` in each case, accounts for cubic-neighbour
   forcing in the joint R2/S2 row, rejects the length-9 object for repeated
   `x,y`, and computes the length-7 symmetric-difference cycle in the
   otherwise-disjoint case.
2. **Independent NetworkX realization.**  It constructs both canonical local
   thetas with branch lengths `{2,7,8}`, a T3 triangle with cubic `x,y`,
   distinct external neighbours, exact bridge attachments `{x,z_0}` and
   `{y,z_0}`, and the forced R2/S2 paths.  NetworkX independently enumerates
   both forced `C_4`s.
3. **T2-inference regression.** A subdivided Heawood bridge independently
   verifies closure 2-connectivity, internal minimum degree 3, C4-freeness,
   the full terminal spectrum `{2,7,9,11,13,15}`, and the fact that every
   length-difference-2 admissible pair avoids the isolated shortest path `2`.

The joint R2/S2 NetworkX fixture satisfies the complete local incidence
hypotheses but, necessarily, not the final `F`-clean hypothesis: the
conditional lemma proves no such `F`-clean realization exists. It is a
negative fixture exposing the contradiction, not evidence for a valid minimal
counterexample. The separate Heawood fixture is `C_4`-free and satisfies the
local two-cut theorem hypotheses, but contains a `C_8`; its sole purpose is to
refute the inference that the theorem's admissible pair must contain the
shortest path.

The audit is new relative to the workspace. Repository search found the
R2/S2 candidate and the partial length-3 exclusion, but neither the forced
triangle-edge closure for length 4 nor the invalid use of T2. The previous
`central_bridge_triangle.py` fixture actually contained this `C_4` but did not
test it and incorrectly reported the path as support.

## 7. Residual Type-T table after the correction

The following is the honest residual classification.  `T2` has one cubic
pair; `T3` has three cubic pairs and eight joint choices of
`(X_a,X_b,X_c)`.  Lemma NE keeps all cubic vertices' external neighbours
distinct.  For every cubic `x`, `Theta_x` has branch spectrum
`{2,2^{rho_x}-1,2^{s_x}}` and `Y_x` is the unused triangle mate.

| surviving family | T2/T3 and selected pair | gateways / sharing | path and route data | S5 data | remaining condition |
|---|---|---|---|---|---|
| theta-chord case IV.1(ii) | either; `Y_x` lies on `Theta_x` | chord `xY_x`, attachments `{x,Y_x}` | no committed A/P/S reduction for the joint triangle analysis | none | exact placement of `Y_x` on the near-power/power branch and resulting route arithmetic |
| exact-two-attachment anchored A | either; `att(B_x)={x,X_x}` | gateways `{x,X_x}`; every bridge path starts `xY_x` | spectrum contains `2` and an admissible pair `ell,ell+delta`, `delta in {1,2}`, `ell>=5`; guaranteed cycles have offsets `0,1,2^rho,2^s+1`; an infinite safe family survives | none | control mutual path overlap or prove a full-F rooted replacement; T1/T2 and C4/C8-freeness do not anchor the pair |
| multi-attachment A | either; at least one cubic `x` has `|att(B_x)|>=3`; admissible terminals are not forced to `{x,X_x}` | sharing must be defined relative to the separate deletions `G-V(Theta_x)` and `G-V(Theta_y)` | lengths `ell,ell+delta`, `delta in {1,2}`; same-branch theta routes: 3; different-branch: 4 (6 with pole edge); all paired sums must avoid powers of two | none unless an independent S leaf coexists | terminal locations, path overlap, and component/block/port sharing; no pinned `{2,4}` claim survives |
| P | either; requires further attachments beyond the triangle-forced pair | two attachments share one internal port; different P bridges may share only a gateway, a port, a block, or a deletion-relative component | length-2 port path; every corresponding theta route must avoid `2^m-2` | none | locate the extra attachments/port and resolve cross-bridge overlap |
| single or mixed S | either | cut vertex `z`, possibly touched by the other bridge | the non-S path data are unchanged unless they detour into the leaf lobe | `d(z)=4`, two incidences per lobe, equal lobe order/size; a detour can reuse the same incidence | internal spectrum of the common leaf and whether a mixed bridge actually enters it; the committed `z in T` degenerate case also remains open |
| double S | T2 or any T3 pair | both analyses name the same `z`; for `z notin T`, both name the literal same attachment-free component `L` | no new theta-route equality is forced | same `z`, `d(z)=4`, same two lobes, same leaf `L`; the triangle and both thetas lie in the opposite lobe | incidence sharing at `z` and the internal cycle spectrum of `L`; no degree contradiction is yet proved |

The former pinned **`{2,4}` exact-two-attachment row** is removed, not the
entire anchored A branch. Anchored `(A,A)` and `(A,P)` remain residual only
with unspecified larger admissible pairs; the committed R2/S2 joint analysis
cannot be applied to them.

Consequently the committed claim that only two residual issues remained was
too broad. The specific R2/S2 candidate is refuted, but genuine survivors still
include deletion-relative component sharing, extra-attachment P geometry,
multi-attachment A terminal/overlap geometry, mixed-S leaf detours, the
double-S incidence problem, the `z in T` S5 case, and the theta-chord case.

### Priority residual audits

**Double S.** In the generic `z notin T` case, both analyses identify the same
cut vertex `z`, the same two lobes, and the same attachment-free component
`L`. S5 gives `d(z)=4`, with two incidences into `L` and two into the lobe
containing `T` and both thetas. This count does not force a fifth edge: the two
central analyses may use the two triangle-side incidences separately, as in
`verifier/central_bridge_triangle_addendum.py`, or may share one incidence.
Sharing only reduces the number of required incidences. Thus one S5 leaf can
serve both cubic vertices at the locally required degree; no degree-forcing
contradiction is proved. The internal spectrum of `L`, the precise entry-path
overlap, and the degenerate `z in T` case remain open.

**Component sharing.** A bridge `B_x` is computed after deleting
`V(Theta_x)`, while `B_y` is computed after deleting `V(Theta_y)`. Therefore
the following are inequivalent and must remain separately labelled: equality
of the deletion-relative components; one shared vertex; one shared internal
block; one shared port; containment of the other vertex's external neighbour;
common gateway only; and membership in the same ambient component with
different attachment sets. The four `(X_x,X_y)` rows settle only the local
gateway incidences: rows 1--3 realize disjoint/touching-at-an-attachment
possibilities, and row 4 is the only row in which full component equality is
locally possible. An internal shared block requires a cut vertex of the joint
external union; a shared port requires the P template; and interlacing
attachments require an ambient block with crossing 2-cuts. None is forced by
the triangle or by the recovered R2/S2 incidence. No complete minimal-joint
enumeration survived in scratch state, so these are retained as topology
conditions rather than promoted to new lemmas.

## 8. Validation record

Baseline, before proof changes:

- `make check`: exit 0; 89 Python files parsed; **83 passed**, 0 failed,
  0 skipped; four native checkers built.
- nauty: `geng` installed at `/opt/homebrew/bin/geng`.
- all seven committed Type-T dependency verifiers exited 0.  Script and
  stdout hashes matched their manifests except
  `central_bridge_triangle_final.py`'s stdout hash: its use of unordered sets
  made row output nondeterministic even though the assertions passed.  This
  audit makes that enumeration deterministic.
- The committed `central_bridge_triangle.py` run also exited 0, but its
  length-4 fixture contained the missed `C_4`; passing reflected incomplete
  assertions, not a valid `F`-clean example.

Post-change commands, hashes, and exact results are recorded in
`manifests/type_t_r2_s2_audit_manifest.json` and the refreshed affected
manifests.  Computation is a finite cross-check of the hand proof, not an
exhaustive graph census or proof-assistant verification.

Final validation used `make check` and
`PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/<name>.py` for each of
the 15 contraction/Type-T verifiers from `contraction_lift` through the new
`type_t_r2_s2_audit`.  Results: **83 passed, 0 failed, 0 skipped**; 90 Python
files parsed; **15/15 verifier processes passed**.  Thirteen stdout hashes
matched their manifests exactly. Two unchanged historical scripts passed all
assertions but retain pre-existing hash-seed-dependent stdout ordering:

- `neighborhood_lift.py`: the manifest hash appears at `PYTHONHASHSEED=2`;
  seeds `1,3,99` produce two other hashes;
- `leaf_block_arithmetic.py`: the manifest hash appears at
  `PYTHONHASHSEED=99`; seeds `1,2,3` produce three other hashes.

Neither script nor manifest was modified by this audit. The default final run
produced hashes
`9090e259486242985ab5789e6a102db47d60792251b8c2b5271eaba28143fac8` and
`65c2cb2645b955cf6893f97ca7538b828cda7e15fed80f18f687f353898054a3`,
respectively. All three refreshed verifiers and the new verifier matched their
refreshed stdout hashes exactly; the corrected final-triangle verifier also
reproduced one hash under `PYTHONHASHSEED=1,2,3,99`.

Current SHA-256 inventory (verifier / corresponding manifest):

| verifier | script SHA-256 | manifest SHA-256 |
|---|---|---|
| `theta_saturation.py` | `c2ff4582f0340b812b639499dda20b2f878fcfd9d9a15d16a7eb90bb92dd8133` | `2e62fa025db5524778156401a5ad5adf62ca49468e145902bc26d04076022e89` |
| `central_bridge.py` | `1a08aace7430ec4addd8081e29c347f07cb036912f03de4e650721ebfac0ed30` | `4696425539d19ec2a7e9b3b4fce67daef434602e821420361fa6f2cb3c8854dd` |
| `block_cut_tree.py` | `3085780496339ba472fd1128ece01c7b71155703eadbd47eccc073416fe4d062` | `d19334fcb84abf361d2684d9dd30d3cf8f398411bf5b7583b83aa2b97d43c3c8` |
| `central_bridge_triangle.py` | `fdd4f03e54e36c4da4997dd87614c57b57350e200736968737cec594825b2079` | `9d570bfdf67917f8a941696e4906520ba51a4f7e68a800b92a92e0bbdcc073c1` |
| `central_bridge_triangle_s5.py` | `cd9e3e2bece61c72f5b987e07299175ef8b961322a7d96f367fe9263ca9553c6` | `c56040eaadf474ab73c064a406d1d96b37fa3581121bd5c16cd5783f7451797f` |
| `central_bridge_triangle_final.py` | `7dcb0dd32ad04fb3d9210b84684474a8d8e26208d0dccef6a3ed16be86f8a8c9` | `d260ea291f15b2469c56d08ab1a6e3b46fd2b9f5a4c71e0119695df1310d2764` |
| `central_bridge_triangle_addendum.py` | `067bd55468df00204891a959c96bd06e9eea8e1953a3cca1bbbf85af378df13a` | `29432027310264f9a64c4c74df84dfe9bdb7490ff72e3e093c36386afee8bda0` |
| `type_t_r2_s2_audit.py` | `304bda8ecde09e76091a4057c4a2f8d70acd580f60034b0069a69ee52d752536` | `faf204212515baaaf6115d9dbaaec134ead503ed3fb532dcb021933daa65b60d` |

**Stopping condition: the interrupted claim refuted by an explicit valid configuration.**
