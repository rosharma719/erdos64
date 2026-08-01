# Audit: the claimed "linear defect growth" theorem (n <= 15q-17)

## Status

[PARTIAL AUDIT — arithmetic and overlap confirmed; the genuinely new core
lemma is NOT independently verified here]

An external report (not in this repo's git history; cites branch
`codex/dyadic-passage-leap`, which does not exist in any local or remote
ref of this repository — checked via `git fetch origin` + `git branch -a`
+ `git log --all`, zero matches) claims, for a lexicographically minimal
Erdős–Gyárfás counterexample `G` with `n=|V(G)|`, `q=2n-2-m`:

```
n <= 15q - 17,   equivalently   q >= ceil((n+17)/15).
```

## Part 1: sections 1-2 of the report are NOT new — they exactly reconstruct
this repo's own `h<=q` result (already audited, see `defect_q_ge_a_audit.md`)

The report's "hub graph" construction (`A` = high-degree vertices, `B1` =
cubic vertices with exactly 1 cubic neighbour, replace each `B1`-vertex by
an edge between its 2 high-degree neighbours, giving a simple auxiliary
graph `F` on `A`) is **the same construction**, under different names, as
this repo's derived leaf graph `L(G)` from `defect.md`'s leaf-compression
Part I: `A`=`H`, `B1`=`C1` (both defined identically: the "3rd-neighbour"
count matches — `B1`'s "1 cubic neighbour" means 2 high-degree neighbours,
exactly `defect.md`'s `C1={v: d_F(v)=1}` meaning 2 `H`-neighbours), `F`=`L(G)`.

Checked directly:
- Their identity **`b1-b3 = 4a-2q-4`** (their eq. 1) is algebraically
  identical to `defect.md`'s **`c1 = c3+4h-2q-4`** (I.1) rearranged.
- Their **`b1 <= 2a-3`** (their eq. 3, from 2-degeneracy of `F`) is
  identical to `defect.md`'s **`c1 <= 2h-3`** (I.2/L4).
- Their derived **`a<=q`** (their eq. 4) is identical to `defect.md`'s
  **`h<=q`** — already proved in this repo and already audited in
  `defect_q_ge_a_audit.md` this session.

This is a **strong positive signal**: whoever/whatever produced this
report either has access to the same correct underlying mathematics, or
independently rediscovered it — either way, the parts of the report that
overlap with already-verified content check out exactly, with no
discrepancy.

## Part 2: the final arithmetic chain is self-consistent, checked by hand

Independently re-derived (not just trusted) the chain from the report's
own stated intermediate lemmas (1), (3), (7) down to the final bound:

- From (7) `b2 <= 10a-15+b1+3b3` and `b=b1+b2+b3`:
  `b <= 2b1+4b3+10a-15`.
- From (1), `b1 = b3+4a-2q-4`, so `2b1 = 2b3+8a-4q-8`, giving
  `b <= 6b3+18a-4q-23`.
- From (1) and (3) (`b1<=2a-3`): `b3 = b1-4a+2q+4 <= (2a-3)-4a+2q+4 =
  2q-2a+1`.
- Substituting: `b <= 6(2q-2a+1)+18a-4q-23 = 6a+8q-17`.
- `n=a+b <= 7a+8q-17` — **matches the report's stated intermediate bound
  exactly.**
- Using `a<=q` (confirmed in Part 1): `n <= 7q+8q-17 = 15q-17` — **matches
  the report's final claim exactly.**

So *given* the report's lemmas (1), (3), (7) as stated, the final bound
follows correctly by pure algebra — I found no arithmetic gap in this
chain.

## Part 3: what is NOT verified — the actual new content (lemma 7)

Everything checked above **assumes lemma (7)** (`b2 <= 10a-15+b1+3b3`),
which is the report's genuinely new contribution: the "five-layer passage"
argument bounding `B2` (degree-3 vertices with exactly one cubic
neighbour, i.e. two high-degree neighbours forming a "colour") via an
overlap-graph 5-colouring and per-colour 2-degeneracy bound, plus a
separate "chain"-counting argument (their section 4, `2P<=b1+3b3`).
**This lemma is not reconstructed, tested, or verified here.** It is
structurally plausible (it follows the same minimality-based
2-degenerate-auxiliary-graph pattern that correctly produced `h<=q`
elsewhere in this repo), and matches this project's own existing habit of
building larger 2-degenerate auxiliary graphs from suppressed degree-3
chains (`defect.md`, `contraction*.md` family), but:
- The precise definitions of "passage", "chain", "colour", and the overlap
  graph's exact structure are not spelled out in the report summary in
  enough detail to mechanically re-implement with confidence.
- Unlike `L1`/`L2` in `defect.md` (mechanically validated on 1,443
  synthetic C4-free instances before their minimality consequence was
  drawn), no such synthetic/mechanical cross-check of this new
  construction is reported or available here.
- The source branch/commit (`codex/dyadic-passage-leap`,
  `3d96e5f7303af7ff1d7dd825123d272e050aad61`) is not accessible from this
  repo, so the actual proof note, code, and "18 passed" tests referenced
  cannot be inspected directly.

## Verdict

**Do not cite `n<=15q-17` as established in this repo.** What's confirmed:
the report's foundational machinery (sections 1-2) exactly matches
already-proved content here, and the arithmetic combining all claimed
lemmas is internally consistent. What's unconfirmed: the one genuinely new
lemma (7) that the whole result depends on. This is a **plausible,
partially-corroborated claim, not a verified theorem** — the same
standard this project applies to every external report.

## Note on scope, if lemma (7) holds

Even if fully verified, the report itself notes the important limitation:
a cubic minimal counterexample has `q=n/2-2`, which trivially satisfies
`n<=15q-17` (`n <= 15(n/2-2)-17 = 7.5n-47`, true for all `n>=7`ish) — so
this bound, even if true, does **not** constrain the cubic case at all
(exactly the branch this project's order-30/32 computational work is
attacking). Its value would be in ruling out large, sparse, low-defect
*non-cubic* counterexamples — a different, complementary front to the
cubic-triangle-quotient and separator-theorem work already in this repo.
