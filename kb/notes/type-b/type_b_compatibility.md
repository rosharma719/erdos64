# Global Type-B compatibility

**Status.** Hand-written graph-theoretic and arithmetic proofs, with an
independent finite verifier for the cycle bookkeeping, finite arithmetic
regressions, and the Balaban diagnostic. This is not proof-assistant formal
verification, an all-orders graph census, or a claim that the surviving
spectrum templates are realized by bridges in a counterexample. No
literature-novelty claim is made.

Throughout, `G` is the 2-connected lexicographically minimum
Erdos--Gyarfás counterexample assumed in `two_cut.md`,

\[
  \mathcal F=\{4,8,16,\ldots\},
\]

and `\{x,y\}` is a Type-B 2-cut. Its nontrivial bridges are `B_1,B_2`,
and `xy` is the separate trivial bridge. Put

\[
 a_i=d_{B_i}(x),\qquad b_i=d_{B_i}(y),\qquad
 c_i=|V(B_i)|-2,\qquad e_i=|E(B_i)|,
\]

and let `\Lambda_i` be the set of lengths of simple `x`--`y` paths in
`B_i`.

## 1. Exact inherited theorem package

After interchanging `x,y` once if necessary, T4 gives exactly

\[
 a_1=a_2=1,\qquad d_G(x)=a_1+a_2+1=3,
\]

whereas

\[
 d_G(y)=b_1+b_2+1\ge3
\]

need not equal three. The edge `xy` is not an edge of either nontrivial
bridge. T1 says each closure `J_i:=B_i+xy` is 2-connected. T2 gives a pair
of lengths differing by one or two in each `\Lambda_i`. Finally,

\[
 q_i=\max\{\lceil3/a_i\rceil,\lceil3/b_i\rceil\}=3
\]

for both bridges.

The exact dependency table is:

| claim | hypotheses | `B_1` | `B_2` | pair only | cleanliness needed |
|---|---|:---:|:---:|:---:|---|
| T1 closure is 2-connected | `G` 2-connected; actual 2-cut bridge | yes | yes | no | no |
| T2 admissible pair | T1; every nonterminal has degree at least 3 | yes | yes | no | no |
| T4 Type-B profile | minimality; two bridges and `xy` | yes | yes | yes | `G` is internally `\mathcal F`-clean |
| edge-plus compatibility | global cycle identity and `xy` | yes | yes | yes | inherited from `G` |
| cross compatibility | global cycle identity | yes | yes | yes | inherited from `G` |
| T3 self-forcing | the three-copy graph is lexicographically smaller | separately | separately | no | the conclusion is self-sum dirtiness |
| T5 replacement forcing | `(c_i,e_i)<_{lex}(c_j,e_j)` | either orientation | either orientation | yes | no cleanliness premise; the conclusion is dirtiness of `B_i` |
| T5 maximality corollary | T5 and self-sum cleanliness of `B_i` | conditional | conditional | comparison | yes, for the bridge asserted maximal |
| equal signatures | both bridges self-sum-clean | yes | yes | yes | yes, for both |
| T9B paired replacement below | full Type-B outside context and spectrum inclusion | either | either | yes | internal and full paired cleanliness |

In particular, T3 proves only

\[
 (3c_i+2,3e_i)<_{\rm lex}(|V(G)|,|E(G)|)
 \Longrightarrow
 (\Lambda_i+\Lambda_i)\cap\mathcal F\ne\varnothing.
\]

It says nothing in an order/edge tie or when the copy graph is larger. T5
proves

\[
 (c_i,e_i)<_{\rm lex}(c_j,e_j)
 \Longrightarrow
 (\Lambda_i+\Lambda_i)\cap\mathcal F\ne\varnothing.
\]

Thus a self-sum-clean bridge is signature-maximal. If both are
self-sum-clean, both are maximal and `(c_1,e_1)=(c_2,e_2)`. In the dirty
case T5's implication has already reached its conclusion; it supplies no
signature equality. T8, T8R, T8P, and the rigid-leaf dichotomy retain their
minimal self-sum-clean Type-A scope and are not used here.

## 2. Complete cycle decomposition

**Type-B cycle decomposition [PROVED].** Every simple cycle `C` using this
cut is in exactly one of the following support categories:

1. `C\subseteq B_1`;
2. `C\subseteq B_2`;
3. `C=xy\cup P_1`, where `P_1` is a simple `x`--`y` path in `B_1`;
4. `C=xy\cup P_2`, where `P_2` is a simple `x`--`y` path in `B_2`;
5. `C=P_1\cup P_2`, where `P_i` is a simple `x`--`y` path in `B_i`.

Indeed, a simple cycle visits each of `x,y` at most once. Distinct bridge
interiors have no edge or vertex between them. A cycle that enters a bridge
interior and later changes support must therefore reach the other terminal;
it splits into exactly two `x`--`y` arcs. The two arcs are either the terminal
edge and one nontrivial-bridge path, or paths in the two different
nontrivial bridges. A cycle never changing support is in category 1 or 2.
These support sets are mutually exclusive, which proves uniqueness of the
category. Different path choices may of course have the same numerical
length; no uniqueness of a length representation is claimed.

Conversely, the unions in categories 3--5 are simple cycles. In category 5
this uses the defining fact that distinct cut bridges meet only at `x,y`.
Hence the complete cross-cut arithmetic is

\[
 (\Lambda_1+\{1\})\cap\mathcal F=\varnothing,
 \qquad
 (\Lambda_2+\{1\})\cap\mathcal F=\varnothing,
\]

\[
 (\Lambda_1+\Lambda_2)\cap\mathcal F=\varnothing,
\]

together with internal `\mathcal F`-cleanliness of each bridge. There is no
condition `\Lambda_i+\Lambda_i` in the actual Type-B graph: that sumset is
introduced only by T3/T5 copy constructions.

## 3. Exact mapping of the triangle-anchored configuration

Use `central_bridge_triangle.md` IV with `y=X_x`. The terminal edge is the
triangle edge `xy`. The two nontrivial cut bridges are not two independently
chosen central bridges:

- `B_1=K` is the central bridge containing `xY` and `Yy`. Its unique edge at
  `x` is `xY`. It contains the isolated path `x-Y-y` of length two, and every
  `x`--`y` path in `B_1` begins with `xY`.
- `B_2` is the component through the external neighbour `x'`. Its unique
  edge at `x` is `xx'`. The canonical theta supplies paths of lengths
  `2^rho` and `2^s+1`. Since `x'y` is excluded by Lemma NA and `xx'` is the
  only `B_2` edge at `x`, no length-two path is forced in `B_2` (indeed this
  geometry has none).
- The edge `xy` belongs to neither `B_i`; it is used only in categories 3
  and 4 of the full graph decomposition.

Applying T2 separately, choose canonical pairs

\[
 \ell,\ell+\delta\in\Lambda_1,
 \qquad m,m+\varepsilon\in\Lambda_2,
 \qquad \delta,\varepsilon\in\{1,2\}.
\]

The guaranteed spectrum cores are therefore

\[
 S_1(\ell,\delta)=\{2,\ell,\ell+\delta\}\subseteq\Lambda_1,
\]

\[
 S_2(m,\varepsilon,\rho,s)
 =\{2^\rho,2^s+1,m,m+\varepsilon\}\subseteq\Lambda_2.
\]

They are asymmetric. Only paths in `B_1` use `xY`; every path in `B_2`
instead uses `xx'`. The values `0,1,2^rho,2^s+1` in
`type_t_exact_two_a.md` are **cycle-closing offsets for the `B_1` pair**,
not four extra lengths in `\Lambda_1`. In particular `\ell+1` is a cycle
length from `xy`, not a terminal path length that may be inserted into a
later cross sum.

The complete lengths forced by these cores are:

| source | guaranteed lengths |
|---|---|
| internal to `B_1` via the `Yy` suffix closure | `ell`, `ell+delta` |
| internal to `B_2` from the two distinct theta branches | `2^rho+2^s-1` |
| `xy+S_1` | `3`, `ell+1`, `ell+delta+1` |
| `xy+S_2` | `2^rho+1`, `2^s+2`, `m+1`, `m+epsilon+1` |
| `2+S_2` | `2^rho+2`, `2^s+3`, `m+2`, `m+epsilon+2` |
| `{ell,ell+delta}+{2^rho,2^s+1}` | `ell+2^rho`, `ell+delta+2^rho`, `ell+2^s+1`, `ell+delta+2^s+1` |
| the two T2 pairs across the cut | `ell+m`, `ell+m+epsilon`, `ell+delta+m`, `ell+delta+m+epsilon` |

The table is a guaranteed subset, not the full cycle spectrum: additional
terminal paths in either bridge create additional edge-plus and cross sums,
and all internal bridge cycles must still be clean.

For a different cubic triangle vertex, its `B_z` is defined after deleting a
different theta. Such central objects can share gateways, vertices, blocks,
or even a deletion-relative component as catalogued in
`central_bridge_triangle.md` V. They are not the two bridges above unless an
explicit identification proves it. By contrast, the two actual bridges of
the fixed cut `\{x,y\}` are internally vertex-disjoint and share exactly the
terminals. Their gateway vertices are distinct as well: `Y` lies in the
triangle while `x'` lies outside it. Only the latter bridge-disjointness fact
licenses every sum in
`\Lambda_1+\Lambda_2` as a simple cycle.

## 4. Paired-spectrum arithmetic

The four canonical pair sums have offset patterns

| `(delta,epsilon)` | offsets from `ell+m` |
|---|---|
| `(1,1)` | `0,1,1,2` |
| `(1,2)` | `0,1,2,3` |
| `(2,1)` | `0,1,2,3` |
| `(2,2)` | `0,2,2,4` |

Four nearby integers can therefore all avoid powers of two; the short
interval alone is not contradictory.

For completeness, assume only `t,u>=1` and write

\[
 A_q=2^t+2^u+2+q,\qquad 0\le q\le4.
\]

Up to interchanging `t,u`, the complete power-of-two exceptions are

\[
 q=0:(t,u)=(2,1),\qquad
 q=2:(t,u)=(1,1),(3,2),\qquad
 q=4:(t,u)=(3,1),
\]

and there are none for `q=1,3`. The odd cases are immediate. For even `q`,
factor the lowest power of two: outside the displayed boundary exponents the
remaining quotient is odd and greater than one, or the number visibly has
two distinct binary digits. Thus this list is exact, not a bounded-search
inference. In the triangle-anchored family below `t,u>=4`, so none of the
exceptions can occur.

**Infinite compatible forced-core family [PROVED].** Fix `rho,s>=2`, choose
arbitrary `delta,epsilon in {1,2}`, and let

\[
 \ell=2^t+1,\qquad m=2^u+1,
 \qquad t,u>\max\{\rho,s,3\}.
\]

Then every guaranteed length in the table in section 3 avoids
`\mathcal F`.

*Proof.* The two displayed `B_1` internal lengths are `2^t+1` and
`2^t+1+delta`, hence odd or strictly between consecutive powers. The known
`B_2` internal cycle `2^rho+2^s-1` is odd and greater than one. Values of the
form `2^v+q`, `1<=q<=5`, lie strictly between
consecutive powers once `v>=4`. Sums `2^t+2^rho+r` and
`2^t+2^s+r`, for the displayed residual offsets, are either odd, have
2-adic valuation one or two with quotient greater than one, or (in the
boundary `s=2` case) visibly have two distinct nonzero binary digits.
The same applies with `t` replaced by `u`.

For the four pair sums put

\[
 A=2^t+2^u+2.
\]

Every needed value is `A+q` for `q in {0,1,2,3,4}`. The odd cases
`q=1,3` are not in `\mathcal F`. For `q=0`, the 2-adic valuation is one.
For `q=2`, both exponents are at least four, so the valuation is two and
the quotient is greater than one. For `q=4`, the valuation is one. These
statements remain true when `t=u` (combine the equal powers first). Thus no
displayed sum is a power of two. `\square`

This is an exact infinite family for the **forced cores** `S_1,S_2`. It is
not a pair of realized full spectra: supersets `\Lambda_i` can add a
forbidden cross sum, and internal cleanliness is independent. Consequently
paired arithmetic alone cannot eliminate Type B.

## 5. T9B — Type-B paired replacement and criticality

Order the two bridge signatures once and choose a Type-B occurrence
lexicographically minimally by

\[
 (|V(B_1)|+|V(B_2)|,|E(B_1)|+|E(B_2)|,
   (c_1,e_1),(c_2,e_2))
\]

inside the fixed minimal counterexample. The following statement actually
uses the stronger global minimality of `G`; the extra choice makes the
paired scope explicit but is not smuggled in as Type-A gadget minimality.

**T9B(a), paired replacement [PROVED].** Fix `i` and let `j!=i`. Suppose a
simple two-terminal graph `B_i'`, on fresh internal vertices and with no
edge `xy`, satisfies:

1. `B_i'+xy` is 2-connected;
2. every nonterminal vertex of `B_i'` has degree at least three;
3. `B_i'` has no internal cycle whose length is in `\mathcal F`;
4. `\Lambda(B_i')\subseteq\Lambda_i`;
5. `B_i'` has fewer internal vertices than `B_i`, or the same number and
   fewer edges.

Then no such `B_i'` exists. In particular, the prompt's stronger demand that
the terminal degree contributions be exactly equal is sufficient but not
necessary.

*Proof.* Replace `B_i` by `B_i'`, retaining `B_j` and `xy`. A 2-connected
closure has degree at least two at each terminal, so after removing `xy`,
`B_i'` contributes at least one edge at each terminal. The retained bridge
and terminal edge already contribute two at each terminal. Hence the new
graph has minimum degree at least three. Its internal cycles are clean by
hypothesis and inheritance. Its edge-plus lengths are a subset of
`\Lambda_i+\{1\}`, and its cross lengths are a subset of
`\Lambda_i+\Lambda_j`; section 2 proves there are no other new cycles.
Thus the replacement is an `\mathcal F`-clean graph of smaller order, or of
equal order and smaller size, contradicting the defining minimality of `G`.
The argument is symmetric in the two bridges. `\square`

**T9B(b), deletion form [PROVED].** For every `e in E(B_i)`, at least one
of the following holds:

1. an internal vertex has degree below three in `B_i-e`; or
2. `J_i-e=(B_i-e)+xy` is not 2-connected.

Deleting `e` only removes internal cycles and terminal paths. If neither
failure occurred, `B_i-e` would satisfy T9B(a): 2-connectivity of its
closure itself guarantees positive terminal contributions. Notice that the
unique edge at `x` automatically falls under alternative 2, since deleting
it leaves `x` with degree one in the closure.

There is also a stronger full-graph statement, already implicit in M1 but
worth spelling out in the Type-B coordinates:

> Every edge of either `B_i` meets `x`, an internal vertex of bridge degree
> three, or `y` when `d_G(y)=3`.

Indeed, if both endpoints of any edge had full graph degree at least four,
deleting it would preserve minimum degree three and could only delete cycles,
contradicting the edge-minimality of `G`. Internal vertices have the same
degree in their bridge and in `G`; `d_G(x)=3`; and

\[
 d_G(y)=3\quad\Longleftrightarrow\quad b_1=b_2=1.
\]

This full-graph version shows that failure of closure connectivity is not an
independent protection for an edge whose endpoints are both non-tight: such
an edge is already ruled out by global edge minimality.

## 6. SPQR consequences and their exact limit

For each closure `J_i=B_i+xy`, `x` has closure degree two, every internal
vertex has degree at least three, and `y` has closure degree `b_i+1`.
Therefore the type-independent S/P arguments already proved in
`two_cut.md` give:

- if `b_i=1`, both terminals have closure degree two and `J_i` is
  SP-eligible;
- if `b_i>=2`, `x` is the unique closure-degree-two vertex and `J_i` is
  rigid-forced;
- a leaf S-node is only an `x`-triangle, a `y`-triangle when `b_i=1`, or
  an `x,y` quadrilateral when `b_i=1`;
- no leaf P-node occurs in a simple reduced, Q-suppressed SPQR tree.

Combining R1/R2 with T9B(b) gives the sharper Type-B-specific real-edge
rule:

> Every real `B_i` edge in an R- or P-skeleton meets an internal
> degree-three vertex.

R1/R2 exclude the closure-connectivity alternative. A real R/P edge cannot
be the unique edge at `x`, nor (when `b_i=1`) the unique edge at `y`, because
its deletion would leave a degree-one vertex in `J_i`, contradicting the
proved 2-connectivity of `J_i-e`. If `b_i>1`, incidence with `y` does not
protect the edge either; its other endpoint must be an internal cubic
vertex. Separately, for arbitrary bridge edges the full-graph rule in
section 5 allows `y` as a tight endpoint only when `b_1=b_2=1`. This is the
terminal audit missing from a direct reuse of T8R/T8P.

These conclusions do not give a finite SPQR family. In particular, the
Type-A rigid-leaf dichotomy used self-sum cleanliness to exclude an exposed
P leaf via a length-two self-sum; Type B supplies only cross cleanliness, so
that proof cannot be imported. Arbitrarily many R-nodes covered by internal
degree-three vertices are not excluded. A paired rooted census is therefore
not structurally justified at this stage: finite absence would not prove the
needed all-orders statement.

## 7. Internal cleanliness and the Balaban diagnostic

T9B does not prove that the first admissible pair begins below 16, that a
long pair forces `C_16`, or that a long pair has a smaller replacement. Those
remain candidate strengthenings, not consequences of criticality alone.

The Balaban-derived bridge from `type_t_exact_two_a.md` makes the boundary
sharp. Its rooted paths through length 14 have lengths `2,11,13`; the verifier
records explicit representatives of the latter two.
A deterministic `C_16` witness is

```text
0-69-28-27-8-7-6-5-4-3-32-31-22-23-62-61-0.
```

It avoids the gateway vertices `x,Y`, so it lies wholly in the 3-connected
Balaban rigid core (the original 70-vertex host is independently checked to
have vertex connectivity three). It nevertheless intersects the recorded
length-11 path in five edges and the recorded length-13 path in nine edges.
Thus the failure is not a detached decorative cycle, but neither overlap
count implies a general theorem.

The fixture violates no T9B incidence condition: apart from the terminal
`x`, every edge has an internal cubic endpoint. Deleting any edge of the
displayed cycle therefore violates an internal degree constraint. No smaller
spectrum-safe replacement is known. Its precise failure remains the internal
`C_16`, so it is a diagnostic near-miss and not a paired obstruction.

## 8. Result

The whole-cut formulation proves T9B and corrects the Type-B SPQR scope, but
it does not eliminate Type B. Both canonical admissible pairs, the terminal
edge, and all triangle-forced gateway routes coexist in the infinite
forced-core family of section 4. Extra paths, internal power-cleanliness, and
realizability by paired-critical bridges are the irreducible missing data.

**one exact irreducible paired-spectrum family**
