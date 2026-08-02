# S6 dependency tree and the leaf-R replacement boundary

This file freezes the exact logical state after T1--T5, R1/R2, T8R/T8P,
the S/P leaf classification, and the rigid-leaf dichotomy. `G` is a
lexicographically minimal Erdős--Gyárfás counterexample, if one exists.
Nothing here is proof-assistant formalized.

## 1. Complete dependency tree

```text
S6: G is 3-connected
|
+-- C0. G is not 2-connected
|   `-- S5 leaves exactly one case:
|       one degree-4 cut vertex, two equal-order/equal-size lobes.
|       FIRST UNPROVED: exclude or safely replace one lobe.
|
`-- Assume G is 2-connected and choose a 2-cut {x,y}
    |
    +-- T1/T2: every B_i+xy is 2-connected; every Lambda_i contains
    |           two lengths differing by 1 or 2.
    +-- T4: t is 2 or 3, giving exactly Type A/B/C below.
    |
    +-- Type A: three bridges, no xy, a_1=a_2=a_3=1
    |   +-- a self-sum is dyadic
    |   |   `-- its two paths overlap (proved); FIRST UNPROVED is the
    |   |       deliberately deferred T7 overlap implication.
    |   `-- the needed bridge is self-sum-clean
    |       +-- T3/T5 force balance/maximality.
    |       +-- SP-eligible leaf forms: finite root S forms; no P leaf.
    |       `-- rigid-forced and minimal/T8-compatible
    |           `-- remote leaf R; FIRST UNPROVED is LR* below.
    |
    +-- Type B: two bridges plus xy, a_1=a_2=1
    |   +-- dyadic self-sum: same deferred overlap gate.
    |   `-- self-sum-clean
    |       +-- T3/T5 force balance/maximality.
    |       +-- finite S leaves/no P leaf.
    |       `-- rigid-forced and minimal/T8-compatible: LR* gate.
    |
    `-- Type C: two bridges, no xy
        +-- q_i=3 when min(a_i,b_i)=1; q_i=2 otherwise.
        +-- dyadic self-sum: same deferred overlap gate.
        `-- self-sum-clean
            +-- T3 forces each clean bridge to evade its q_i-copy gluing;
            |   T5 has no Type-C version.
            +-- (a_i,b_i)=(1,1): finite S leaves are possible; no P leaf.
            `-- every other terminal profile is rigid-forced; extending the
                scoped rigid-leaf theorem and then LR* are both unproved.
```

This tree records a critical scope fact: **LR* is not currently sufficient to
prove S6.** The cut-vertex case, the expressly deferred self-sum-overlap gate,
and the extension from scoped minimal Type-A gadgets to every Type B/C bridge
occur earlier in the dependency tree. Claiming that every 2-cut has already
been reduced to LR would therefore be false.

## 2. Exact Type A/B/C table

Let `c_i=|V(B_i)|-2`, `e_i=|E(B_i)|`, and
`q_i=max(ceil(3/a_i),ceil(3/b_i))`. Every row also inherits:

- internal power-cycle cleanliness of each actual bridge;
- `(Lambda_i+Lambda_j) cap F = empty` for `i != j`;
- two admissible terminal-path lengths in every `Lambda_i` (T2).

| type | nontrivial bridges / `xy` | terminal profile | T3/T5 consequences | possible leaf types in `B_i+xy` | proved eliminations | first unproved implication |
|---|---|---|---|---|---|---|
| A | `t=3`, `xy` absent | after swapping poles, `a_1=a_2=a_3=1`; `d_G(x)=3`; all `q_i=3` | T3: a self-sum-clean `i` must have `(3c_i+2,3e_i) >=lex (n,m)`. T5: every clean `i` is lex-maximal among bridge signatures; if all three are clean, `(c_1,e_1)=(c_2,e_2)=(c_3,e_3)`. | if `b_i=1`, S-triangle at either terminal or S-quadrilateral through both; if `b_i>1`, only the x-triangle; P leaf impossible; otherwise R | `t>=4`; `xy` present; remote/larger S leaves; all P leaves; Type-A bridge orders <=11 (finite only) | dyadic overlapping self-sum, or LR* after the clean/minimal rigid gate |
| B | `t=2`, `xy` present | after swap, `a_1=a_2=1`; `d_G(x)=3`; all `q_i=3`; additionally `(Lambda_i+{1}) cap F=empty` | T3 as above. T5: a clean bridge is lex-maximal; if both are clean, their `(c,e)` signatures are equal. | same per-bridge S/P/R list as Type A | all other bridge counts/profiles; remote/larger S leaves; all P leaves | dyadic overlapping self-sum, or LR* after the clean/minimal rigid gate |
| C | `t=2`, `xy` absent | `a_1+a_2>=3`, `b_1+b_2>=3`; no bridge has both terminal degrees >=3; `q_i=3` iff a terminal degree is 1, otherwise `q_i=2` | T3: clean `i` must have `(q_i c_i+2,q_i e_i) >=lex (n,m)`. If both have `q=2` and are clean, the full evasion equalities force equal `(c,e)`. No T5 statement is proved. | `(1,1)` is SP-eligible with the three finite S forms; exactly one unit terminal permits only its S-triangle; no unit terminal permits no S leaf; P leaf impossible; otherwise R | `q=1`; all P leaves; every S leaf outside the listed degree-2-terminal forms | Type-C replacement/balance implication; then LR* for a rigid leaf |

The S-leaf entries follow from one common argument: every internal vertex on
the real path of a leaf S-skeleton has degree two in the closure, while the
only possible degree-two closure vertices are terminals whose bridge degree is
one. This extends the already proved Type-A wording without changing its
proof. The no-leaf-P proof is type-independent for a simple reduced SPQR tree.

## 3. Exact replacement principle (proved) and LR* existence target (open)

Let a connected actual leaf pertinent graph `K` meet the rest `O` of `G`
exactly in its parent poles `a,b`. Define `Lambda_ab(K)` as its simple `a-b`
path-length spectrum. The following **replacement principle is proved
directly**.

If there is a connected two-terminal `K'` such that:

1. gluing `K'` to `O` is simple;
2. every internal vertex of `K'` has degree at least three;
3. `d_K'(a)=d_K(a)` and `d_K'(b)=d_K(b)` (the safe exact form of terminal
   degree preservation);
4. `K'` has no internal power-of-two cycle;
5. `Lambda_ab(K')` is a subset of `Lambda_ab(K)`;
6. `K'` has fewer internal vertices than `K`, or the same number and fewer
   edges;

then replacing `K` by `K'` gives a lexicographically smaller counterexample.
Indeed internal cycles in `O` and `K'` are safe. Every cycle using both sides
is one `a-b` path from each side; spectrum inclusion replaces its `K'` length
by an already occurring `K` length, so it cannot create a new forbidden
cycle. Exact pole degrees and the internal degree condition preserve minimum
degree three. This contradicts minimality of `G`.

The genuinely open statement is therefore:

> **LR*.** Every leaf-R pertinent graph satisfying the inherited conditions
> below either has an internal C4/C8, or admits a `K'` satisfying conditions
> 1--6.

For a **genuine original leaf R-node**, every skeleton element except the
parent edge is real. Thus the actual pertinent graph is exactly `K=R-ab`;
the expansion represented by the parent edge belongs to `O`. Exactly
inherited from a minimal-counterexample occurrence:

- `K` is the pertinent graph of a leaf R-node in the reduced SPQR tree of a
  simple host;
- its pole-edge closure is 2-connected and the R-skeleton is 3-connected;
- every actual internal cycle of `K` is power-cycle-free;
- every real edge is incident with a vertex cubic in `G` (global B3; this
  agrees with T8R only in the scoped minimal Type-A-gadget setting);
- the outside meets `K` only at `a,b`, so terminal-spectrum inclusion is the
  correct cross-cycle compatibility condition.

Not inherited automatically:

- self-sum cleanliness of the containing bridge;
- minimality of `K` among two-terminal realizations;
- a T8-style deletion certificate for a whole virtual expansion;
- applicability of the scoped rigid-leaf dichotomy to all Type B/C cases.

These missing hypotheses are why the informal LR wording cannot simply be
assumed.

An R-node newly exposed as a core leaf only after suppressing a terminal-local
S-leaf is not automatically such an occurrence: relative to its remaining
core neighbor, its pertinent side contains the suppressed S expansion and can
also contain the artificial closure edge `xy`. Applying the replacement
principle to that orientation would therefore be invalid. In a multi-node
core there is another core leaf away from the suppressed root side, and that
node is a genuine original R-leaf. If the core is a single R-node, it was
already an original leaf adjacent to the S-root and its pertinent side is
obtained by deleting that parent virtual edge, not by converting it.

## 4. Existing 75,745 leaf-R records: exact witness patterns

`verifier/leaf_r_patterns.py` streams the preserved E23 and E24 artifacts in
their common order. It performs no graph generation and no SPQR
recomputation. A pattern is the dihedral cyclic word of:

- parent-pole (`p`) versus internal (`i`) witness vertices;
- bridge degree exactly 3 (`3`) versus higher (`+`);
- real R-edge (`R`) versus a converted suppressed virtual element (`V`).

Parent poles are interchangeable. Under this exact equivalence relation,
**42 patterns are necessary and sufficient to cover all 75,745 records**:
each is a nonempty disjoint equivalence class, so no smaller exact-pattern
cover exists. Representatives and counts for all 42 are in
`manifests/leaf_r_patterns_manifest.json`.

| local witness property | records |
|---|---:|
| real R-edges alone contain a shortest C4/C8 | 75,137 |
| genuine original remote R-leaf; real-edge C4/C8-positive | 72,927 |
| root-side R exposed after terminal-S suppression | 2,818 |
| exposed root-side orientation is real-edge-clean; contracted witness uses the suppressed-S element | 608 |
| witness contains neither parent pole | 4,313 |
| witness contains exactly one parent pole | 61,773 |
| witness contains both poles, hence is two terminal paths | 9,659 |
| unique C8-only leaf | 1 |

The 608 residual records form **15 exact patterns and seven coarse profiles**
(562 rigid-forced records and 46 SP-eligible records). Of them, 576 witnesses
contain both parent poles and split into two terminal paths; 28 contain one
pole; four contain neither. The two empirical configurations are therefore:

1. **R-real-cycle:** a C4/C8 using only real R-edges (75,137 records), a direct
   local forbidden cycle;
2. **R-root-side-S:** the real R-edge subgraph is C4/C8-clean and one
   suppressed terminal-local S element completes a contracted C4 (608
   records).

The second configuration is a warning, not an LR counterexample or the LR
bottleneck. Its R-node became a leaf only after suppression, and expanding the
S element can change the contracted length four to a non-dyadic length; that
S-side expansion can also contain the artificial closure edge. The 72,927
genuine original remote R-leaf records all fall in the first configuration.

## 5. Smallest abstract search and exact bottleneck

`verifier/leaf_r_replacement_search.py` exhausts every edge-rooted connected
minimum-degree-three skeleton through order nine—a superset of realizable
3-connected R-skeletons. Across 87,004 skeletons and 1,802,018 choices of
parent edge, only ten deletions are C4-free and all ten contain a C8. Thus no
unexpanded clean `K=R-ab` exists through order nine; LR* alternative 1 always
holds there. The replacement alternative and spectrum inclusion are therefore
not exercised by this range.

The exact unresolved leaf configuration is:

> A genuine original remote leaf R-skeleton of arbitrary order, with parent
> edge `ab`, for which `K=R-ab` is C4/C8-clean and satisfies the inherited
> cubic-incidence, pole-degree, and internal power-cycle conditions. Prove that
> its exact terminal spectrum and pole degrees admit a strict replacement
> satisfying LR* conditions 1--6, or exhibit a concrete graph for which none
> exists.

No such `K` occurs in the 72,927 genuine archived leaves or in the abstract
edge-rooted search through skeleton order nine. This is the precise first
unseen LR configuration, but **not yet the sole S6 bottleneck** because the
earlier gates displayed in §1 remain open. No proof of S6 or LR* is claimed.
