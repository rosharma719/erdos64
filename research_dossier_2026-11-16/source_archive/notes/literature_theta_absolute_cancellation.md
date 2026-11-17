# Pass XXIII — From modular theta necklaces to absolute length control

**Research status:** PUBLISHED (external theorems), PROVED (elementary transfer lemmas below), OPEN (graph-existence/scale conditions). Date: 2026-11-16.

This is an additive integration note for the research track. It does **not** claim a proof of the Erdős–Gyárfás conjecture, does not certify any graph census, and does not validate the earlier unreviewed research passes in aggregate. No shared solver is changed.

## 1. Literature dependencies

**PUBLISHED — Lyngsie–Merker (2021).** [Cycle lengths modulo k in large 3-connected cubic graphs](https://www.advancesincombinatorics.com/article/18971-cycle-lengths-modulo-k-in-large-3-connected-cubic-graphs), especially Definitions 2.2 and 2.6, Lemmas 2.3 and 2.7, Theorem 4.3, and Lemma 5.13 / Theorems 5.14–5.15. Their global proof extracts either theta necklaces or wiggly necklaces. For theta necklaces, the output is modular: when the modulus is odd, the authors use the relation among four local routes to cover all residues. For even moduli only a parity or mod-four class can follow. This **does not** locate an absolute power-of-two length.

**PUBLISHED — Choi–Chu–Kim–Park (2026).** [Existence of cycles of length divisible by 3 or 4](https://arxiv.org/abs/2605.02731), Theorem 1.7 and Section 4. A graph of order at least nine, minimum degree at least two, and at most three degree-two vertices has a cycle of length divisible by four. For a clean two- or three-pole at that order, this cycle cannot have length 4, 8, 16, ...; it must be a non-power-of-two multiple of four (at least 12). Their minimality and terminal-path residue bookkeeping are portable. Their planarity/face argument relies on excluding **all** cycles divisible by four, which cleanness does not imply.

**PUBLISHED — Di Braccio–Katsamaktsis–Ma–Malekshahian–Zhao (2026).** [Leaf-to-leaf paths and cycles in degree-critical graphs](https://doi.org/10.1007/s00493-026-00205-2) shows that many distinct lengths can coexist with strong arithmetic sparsity; the number of lengths alone is not a dyadic certificate.

**VERIFIED STATUS — Duran Ballester (2026).** The [original Zenodo working paper](https://zenodo.org/records/22019344) claimed a structural exhaustion proof. The [Erdős Problems claim record](https://erdosproblems.ai/wiki/problems/extremal_graph_theory/E0064/claims/2026_08_19_duran_ballester) records the author's subsequent reduction with six remaining outcomes, a defect in the odd-part modular inference, and the claim's withdrawn status. The full conjecture remains open. This work should not be used as a proved theorem.

## 2. Exact local route matrix in a theta necklace

**PUBLISHED (as data in Lyngsie–Merker Lemma 2.3).** For one theta(i) block, the four boundary-to-boundary routes have lengths

    a+b,  a+d,  c+b,  c+d-2i.

Set `B=a+b`, `X=c-a`, `Y=d-b`. The route matrix is

    R00 = B           R01 = B+Y
    R10 = B+X         R11 = B+X+Y-2i.

In particular, the discrete mixed second difference is **exactly**

    R00 + R11 - R01 - R10 = -2i.

This is stronger arithmetically than its reduction modulo any `k`, but one block alone need not provide an actual switch of length `2i`.

## 3. Two-block cancellation theorem

**PROVED (elementary deduction from the published route matrix).** Let two distinct theta(i) blocks `j` and `h` of the *same* theta necklace satisfy `Y_j=Y_h`. Their external connector paths are fixed, and all theta blocks are mutually disjoint, so the following combinations both extend to simple cycles:

- At block `j` use `R00`, and at block `h` use `R11`.
- At block `j` use `R01`, and at block `h` use `R10`.

The first combination has total local length

    B_j + (B_h + X_h + Y_h - 2i),

while the second has total local length

    (B_j + Y_j) + (B_h + X_h).

The second is longer by exactly `2i`, because `Y_j=Y_h`. **No equality of the X-increments is needed.** A symmetric argument works if `X_j=X_h` instead.

For unequal increments the same trade has signed difference `2i+Y_j-Y_h`. Thus nearby, rather than identical, increments may also provide useful small absolute switches. This latter observation is a formula, not a graph-existence theorem.

## 4. Absolute-progression corollary

**PROVED.** Suppose a theta(i) necklace has `N` disjoint theta blocks, and among their Y-increments there are only `R` distinct integer values. If the multiplicities are `n_1,...,n_R`, we can form

    m = sum_s floor(n_s/2) >= ceil((N-R)/2)

pairwise disjoint pairs of equal-Y blocks. Apply the two-block trade to each pair independently. There is a fixed baseline simple cycle of some length `L` such that **all** lengths

    L, L+2i, L+4i, ..., L+2im

occur as simple cycles in the necklace. The selected family has generating polynomial

    z^L (1+z^(2i))^m,

where positivity of a coefficient guarantees a cycle of the corresponding length. The polynomial is an encoding of an explicit independent family, not a substitute for showing those paths are compatible.

If `q` is the smallest power of two at least `max(L,4)`, the family contains a dyadic cycle whenever

    (a) L is divisible by 2i, and
    (b) q <= L + 2im.

For the values in the published structural theorem, `i=1` (step 2) or `i=2` (step 4), condition (a) is the appropriate parity/mod-four alignment. If the necklace avoids a prescribed edge or vertex, all these cycles do too. If the fixed scaffold meets the prescribed edge/root, avoidance does *not* follow.

**Limitation:** The theorem is conditional on *exact* repetition of one local increment and the presence of a suitable baseline. The published modular pigeonhole argument gives repetition modulo a fixed odd modulus, not exact equality of the increments. Nor does it guarantee that `2im` is comparable to `L` or that the baseline is aligned. These are the three genuinely new structural requirements.

## 5. A scale-coupling lemma for multiple windows

**PROVED (elementary).** Suppose some construction yields a family of simple cycles whose lengths include every integer in each of `[L_1,U_1],...,[L_t,U_t]`, with `L_j <= L_(j+1)` and `L_(j+1) <= U_j+1` for all adjacent windows. Then all lengths in `[L_1,max_j U_j]` are attained. If this interval contains a power of two, so does the graph. For step-two windows, the same holds if they have a common even parity class and `L_(j+1) <= U_j+2`.

This is a certificate-extraction lemma and contains no assertion that the required windows exist. In the theta-chain setting, the difficult question is whether the nested attachments create such overlapping windows **at a common scale**, not just in a common residue class.


## 6. A safe modular-to-exact audit (the Zenodo arithmetic lesson)

**PROVED (elementary number theory).** Let `g=2^s h` with `h` odd, and consider the residues of powers of two modulo `g`. These residues consist of the finitely many `2^k mod g` for `0<=k<s`, together with precisely those residues `r` satisfying

    r = 0 mod 2^s   and   r mod h belongs to <2> in (Z/hZ)^*.

Here `<2>` is the multiplicative subgroup generated by 2, and the statement for `h=1` uses the obvious trivial interpretation. Proof: for `k>=s` the first congruence is necessary, while `2^k mod h` cycles through `<2>`; every member of this cyclic subgroup is attained at arbitrarily large exponents. The Chinese remainder theorem then gives the characterization.

For `g=96=32*3`, the dyadic residues are exactly `{1,2,4,8,16,32,64}`. The interval of residues `{17,...,29}` intersects the power-of-two orbit **modulo the odd part** 3, but has no dyadic residue modulo 96. Therefore odd-part reachability alone is invalid.

**PROVED (elementary exact-lift lemma).** If every cycle length under consideration is in `[L,U]`, `Q` is a power of two in this interval, and a modulus `g` satisfies `g>U-L`, then the existence of an attained length congruent to `Q` modulo `g` implies an attained cycle of length exactly `Q`. Without a length-range restriction of this kind, *even a correct full-modulus residue match is not an exact-length proof*. In particular, Lyngsie–Merker's theorem for each fixed odd modulus does not give the desired exact lift merely by choosing `g` to grow with graph order; the size threshold in their theorem itself depends on `g`.

This corrects a possible failure mode in both the older modular-argument literature and our research notes. No claim is made that the recorded Zenodo defect is the only defect.

## 7. Revised primary research question

**OPEN — absolute cancellation or diversity theorem.** In the isolated-endblock theta-chain case of Lyngsie–Merker Section 5.3, prove a structural dichotomy with two outcomes:

1. **Low increment diversity:** enough blocks have equal (or nearby) X/Y differences that the two-block theorem produces a long even-aligned absolute progression with a dyadic target inside it; or
2. **High increment diversity:** varying the theta routes produces two or more *compatible* cycle windows, with controlled absolute positions, whose union crosses a dyadic boundary.

Any version must explicitly (i) quantify width relative to baseline, (ii) handle the parity/mod-four class, (iii) accommodate theta necklaces as well as wiggly necklaces (the published chain lemma may yield either), and (iv) preserve avoidance of the distinguished edge if the argument is intended for clean two-poles.

A serious attempt should first derive inequalities on X/Y increments from the order of attachment spans in Lemma 5.13. **Exact equality of these increments is not known to be forced by the paper.** If it is false in the relevant graph class, keep the pair-trade `2i+Y_j-Y_h` and study the resulting sumset instead.

## 8. Strategic priority and stopping rules

- **Primary:** Test and prove/falsify a quantitative *absolute increment diversity dichotomy* for a special theta-chain. This uses a genuine existing structural trichotomy and targets the missing scale control directly.
- **Secondary:** Use the Choi et al. mod-four cycle as an anchor only if it can be placed into the *same* switchable scaffold. An unrelated mod-four cycle does not solve alignment.
- **Fallback:** Analyze connecting-endblock and few-endblock cases after the isolated-chain mechanism is understood, because the Lyngsie–Merker global theorem cannot be upgraded by strengthening only one of its three branches.
- **Stop if:** The candidate hypothesis assumes that the switch budget already crosses a power of two, that equal increment values occur with linear multiplicity without a proof, or that arbitrary overlapping paths are independently switchable. These would simply repackage the original problem.

**Overall status:** The two-block exact cancellation and its quantitative pairing corollary are PROVED by direct route algebra. The absolute scale/alignment existence lemma is OPEN. Conjecture T, nonexistence of clean 2-poles, and the full Erdős–Gyárfás conjecture all remain OPEN.
