# Priority audit: does `Pi0` remain the lowest-order unresolved Type-B tuple?

**Status.** This file is a hand-written logical audit reusing existing
proofs and existing computer-assisted finite certificates. It performs no
new computation and generates no new candidate graphs. It reaches a
**PROVED_IN_MARKDOWN** conclusion (Section 4) that changes the project's
priority order. No proof-assistant formalization exists.

## 0. Why this audit is necessary

`type_b_one_slack_resolution.md` proved B20 and raised the bound for
`Pi0=(2,2,4,4,1,1)` from 36 to 40. But `Pi0` is rank 1 of an explicit,
frozen 20-tuple family (`type_b_realizability.md` Section 2). Raising one
tuple's bound does not automatically mean it is still the smallest: other
tuples in the same family had lower or equal *original* bounds and have
never been touched by the B19/one-slack/B20 machinery. This file checks
every tuple with a bound at or below 40 and determines the true current
minimum.

## 1. The tuple family, recovered exactly

From `type_b_realizability.md` Section 1:

\[
 \Pi=(\rho,s,t,u,\delta,\varepsilon), \qquad
 \rho,s\ge2,\quad \delta,\varepsilon\in\{1,2\},\quad t,u>\max\{\rho,s,3\}.
\]

With `ell=2^t+1`, `m=2^u+1`:

\[
 S_1(\Pi)=\{2,\ell,\ell+\delta\}, \qquad
 S_2(\Pi)=\{2^\rho,2^s+1,m,m+\varepsilon\}.
\]

`S1` is `B1`'s forced terminal path-length set; `S2` is `B2`'s. Order bounds
(Section 3 of `type_b_realizability.md`):

\[
 |V(B_1)|\ge\ell+\delta+1, \qquad
 |V(B_2)|\ge\max\{m+\varepsilon+1,\,2^\rho+2^s\}.
\]

For `t=u=4` (`ell=m=17`), the constraint `t,u>max{rho,s,3}` forces
`rho,s in {2,3}` exactly — 4 choices — times `delta,epsilon in {1,2}` — 4
choices — giving exactly the 16 tuples ranked 1-16 in
`type_b_realizability.md`'s frozen table. Rank 17 jumps to `t=5`
(`ell=33`), giving bound 52. **No tuple outside ranks 1-16 has a bound at
or below 40.** This audit therefore covers all of them; nothing is left
out by scope-limiting to "the first twenty."

## 2. What the completed proofs actually use

Re-reading `type_b_b19.md`'s dependency-audit table line by line: every row
cites either "local bridge hypothesis," "ambient minimum degree
three"/"power-cycle-free," or a specific edge-count/degree-sequence
certificate. **`rho` and `s` do not appear anywhere in that table, in its
proof, in `type_b_one_slack.md`, or in `type_b_one_slack_resolution.md`.**
The one fact from the tuple that B19/one-slack/B20 actually use is stated
explicitly in the table's second row: *"18 belongs to the frozen forced
spectrum in both bridge roles."* That is exactly the condition `delta=1`
(for `B1`, giving `ell+delta=18`) or `epsilon=1` (for `B2`, giving
`m+epsilon=18`) — nothing about `rho,s` is ever invoked, because `B1`'s
spectrum `S1` never contains `rho,s` at all, and the degree/edge-count
argument for `B2` only uses `B2`'s longest required length, never the
other three members of `S2`.

**Consequence (immediate corollary, newly identified by this audit, not
previously stated in the repository).** For *any* bridge role `B` whose
longest required path has length exactly 18 (equivalently: whichever of
`delta=1` or `epsilon=1` holds), the entire chain — B19 (order 19
impossible), the one-slack reduction (order 20 reduces to a 19-vertex
remainder with a distinguished 18-vertex path), Family I/Family II
elimination, and B20 (order 20 impossible) — applies verbatim, giving
`|V(B)|>=21` for that role. This holds regardless of `rho,s,` and
regardless of what the *other* bridge's role requires. The reused
certificates (101,546-graph 26-edge run, 570-graph 27-edge extremal
census, 86,047-graph Family I run, the 54-candidate Family II run) are
themselves pure statements about graphs with given vertex/edge counts and
degree sequences — they never reference `rho,s` either, so no
recomputation is needed to reuse them.

For a role with `delta=2` (or `epsilon=2`), the longest required length is
19, not 18. This is a **genuinely different geometric reduction**: it
would require its own zero-slack (order-20, "E38"-style) elimination
parallel to `type_b_equality_order.md`'s E36, followed by its own
one-slack (order-21) analysis parallel to `type_b_one_slack.md`/B20 — none
of which exists in this repository. **Nothing currently proved reaches
these roles.**

## 3. Complete audit table

`orig` = the frozen bound from `type_b_realizability.md`. `B1
touched`/`B2 touched` = whether that specific bridge role's longest
required length is 18 (i.e. `delta=1` or `epsilon=1` respectively), the
exact condition under which the existing B19+B20 chain applies per
Section 2 above. `new` = the resulting current bound after applying the
chain to every touched role (untouched roles keep their original bound).

| rank | `(rho,s,t,u;delta,eps)` | `S1` | `S2` | orig `(n1,n2;nG)` | B1 touched | B2 touched | new `(n1,n2;nG)` |
|---:|---|---|---|---|:---:|:---:|---|
| 1 | `(2,2,4,4;1,1)` | `2,17,18` | `4,5,17,18` | `(19,19;36)` | yes | yes | `(21,21;40)` |
| 2 | `(2,3,4,4;1,1)` | `2,17,18` | `4,9,17,18` | `(19,19;36)` | yes | yes | `(21,21;40)` |
| 3 | `(3,2,4,4;1,1)` | `2,17,18` | `5,8,17,18` | `(19,19;36)` | yes | yes | `(21,21;40)` |
| 4 | `(3,3,4,4;1,1)` | `2,17,18` | `8,9,17,18` | `(19,19;36)` | yes | yes | `(21,21;40)` |
| 5 | `(2,2,4,4;1,2)` | `2,17,18` | `4,5,17,19` | `(19,20;37)` | yes | **no** | `(21,20;39)` |
| 6 | `(2,2,4,4;2,1)` | `2,17,19` | `4,5,17,18` | `(20,19;37)` | **no** | yes | `(20,21;39)` |
| **7** | `(2,2,4,4;2,2)` | `2,17,19` | `4,5,17,19` | `(20,20;38)` | **no** | **no** | **`(20,20;38)`** |
| 8 | `(2,3,4,4;1,2)` | `2,17,18` | `4,9,17,19` | `(19,20;37)` | yes | **no** | `(21,20;39)` |
| 9 | `(2,3,4,4;2,1)` | `2,17,19` | `4,9,17,18` | `(20,19;37)` | **no** | yes | `(20,21;39)` |
| 10 | `(3,2,4,4;1,2)` | `2,17,18` | `5,8,17,19` | `(19,20;37)` | yes | **no** | `(21,20;39)` |
| 11 | `(3,2,4,4;2,1)` | `2,17,19` | `5,8,17,18` | `(20,19;37)` | **no** | yes | `(20,21;39)` |
| **12** | `(2,3,4,4;2,2)` | `2,17,19` | `4,9,17,19` | `(20,20;38)` | **no** | **no** | **`(20,20;38)`** |
| **13** | `(3,2,4,4;2,2)` | `2,17,19` | `5,8,17,19` | `(20,20;38)` | **no** | **no** | **`(20,20;38)`** |
| 14 | `(3,3,4,4;1,2)` | `2,17,18` | `8,9,17,19` | `(19,20;37)` | yes | **no** | `(21,20;39)` |
| 15 | `(3,3,4,4;2,1)` | `2,17,19` | `8,9,17,18` | `(20,19;37)` | **no** | yes | `(20,21;39)` |
| **16** | `(3,3,4,4;2,2)` | `2,17,19` | `8,9,17,19` | `(20,20;38)` | **no** | **no** | **`(20,20;38)`** |

All arithmetic reproduced by direct computation (script embedded in this
audit's manifest); no manual transcription errors.

## 4. Required priority conclusion

**Option 3 applies exactly: other tuples occur below order 40.**

- Ranks 7, 12, 13, 16 (all `delta=epsilon=2`) sit at their **original,
  completely untouched** bound of **38**. Neither bridge role has been
  analyzed by any proof in this repository, because both roles need the
  length-19-path/order-20-zero-slack reduction that does not yet exist.
- Ranks 5, 6, 8, 9, 10, 11, 14, 15 (mixed `delta,epsilon`) improve from
  their original bound of 37 to **39** by direct, immediate reuse of the
  existing chain on whichever single role has `delta=1` or `epsilon=1` —
  but the *other* role remains completely unresolved at its own
  zero-slack order-20 minimum, so the pair bound is 39, not 40.
- Only ranks 1-4 (`Pi0` and its `rho,s`-siblings) reach the full proved
  bound of 40.

The strict minimum current bound across every tuple with `orig<=40` is
**38**, achieved by ranks 7, 12, 13, 16. `Pi0` (rank 1) is not first; it is
not even tied for first. Four tuples strictly precede it.

Per the task's own stopping rule ("If another tuple can beat order 40,
stop the two-slack `Pi0` work and attack that tuple first"), **the
two-slack, 21-vertex `Pi0` bridge investigation is not started in this
session.**

## 5. What is explicitly claimed and what is not

- **Claimed:** ranks 2, 3, 4 share `Pi0`'s exact bound of 40, as an
  immediate corollary of the fact (verified by direct re-reading of every
  dependency in `type_b_b19.md`, `type_b_one_slack.md`, and
  `type_b_one_slack_resolution.md`) that none of those proofs ever
  reference `rho` or `s`. This corollary is newly identified by this
  audit; it was not previously stated anywhere in the repository, and it
  reuses existing certificates rather than requiring new ones (those
  certificates are themselves `rho,s`-independent graph facts).
- **Claimed:** ranks 5, 6, 8, 9, 10, 11, 14, 15 improve from 37 to 39 by
  the same corollary applied to only their `delta=1`-or-`epsilon=1` role.
- **Claimed:** ranks 7, 12, 13, 16 remain at their original bound of 38,
  fully unresolved, and are the current strict minimum among all
  `orig<=40` tuples.
- **Not claimed:** any elimination of ranks 5-16. Their remaining
  unresolved roles (the `delta=2`/`epsilon=2` roles) require a fresh
  zero-slack (E38-style) reduction and then a fresh one-slack (order-21)
  reduction that do not exist yet.
- **Not claimed:** that the corollary in Section 2/5 has been
  independently re-verified by rerunning any computation specific to
  ranks 2-4. It rests on a documented, checkable re-reading of the
  existing proofs' stated hypotheses (Section 2), not on new execution.
- **Recommended next step (not started in this session):** a zero-slack,
  order-38, `(delta,epsilon)=(2,2)` elimination for ranks 7, 12, 13, 16 —
  the direct analogue of `type_b_equality_order.md`'s E36, but for a
  20-vertex bridge with a required length-19 Hamiltonian path — is now the
  correct highest-priority Type-B target, ahead of any two-slack `Pi0`
  work.

## 6. Superseded by `type_b_delta2_zero_slack.md`

The recommended next step in Section 5 has since been completed: B20D2
(no eligible 20-vertex Type-B bridge role with frozen admissible gap 2)
is proved in `type_b_delta2_zero_slack.md`. Combined with B19+B20, every
bridge role of every one of the 16 tuples audited here (ranks 1-16, the
only ones with original bound `<=40`) now has order `>=21`, so **all 16
tuples reach full-graph order `>=40`** — the priority question this file
raised is resolved: there is no longer a tuple below 40 to prioritize.
