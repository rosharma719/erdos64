# Pass XXIV: theta subset-sum cancellation and the scale obstruction

**Status:** PUBLISHED input (Lyngsie–Merker, Lemma 2.3 and Definition 2.2); PROVED statements below (elementary hand proofs); COMPUTED explicit fixtures (independent graph-level Python/NetworkX versus symbolic C enumeration); OPEN absolute-scale forcing in the ambient 3-connected cubic graph.

**Source:** K. S. Lyngsie and M. Merker, *Cycle Lengths Modulo k in Large 3-connected Cubic Graphs*, Advances in Combinatorics (2021), §§2 and 5.3, https://doi.org/10.19086/aic.18971. The notation below uses their four w1–w2 routes.

## 1. Route algebra and the general cancellation theorem (PROVED)

Let a theta(i) necklace have disjoint theta blocks j=1,...,N, i a positive integer, and its four attachment-to-attachment path lengths be

    R_j(x,y) = B_j + x X_j + y Y_j - 2i x y,    x,y in {0,1}.

This is exactly the published route matrix (after setting B=a+b, X=c-a, Y=d-b). Any selection of one route per block, plus the fixed connecting paths around the necklace, makes a simple cycle.

**Lemma 1 (signed collision -> one exact small switch).** If the integers Y_1,...,Y_N have two distinct subsets with equal sums, then the necklace has two simple cycles whose lengths differ by exactly 2i.

*Proof.* Cancel their intersection to obtain disjoint U,V with U union V nonempty and sum_U Y = sum_V Y. Put epsilon_j=+1 on U and -1 on V. Choose any distinguished h in U union V and fix x_h=1, x_j=0 for all other participating blocks. For each j in U change y from 0 to 1; for j in V change y from 1 to 0. All unmentioned coordinates stay fixed. The two globally valid cycles differ in length by

    sum_j epsilon_j (Y_j - 2i x_j)
      = (sum_U Y - sum_V Y) - 2i epsilon_h
      = -2i epsilon_h.

Its absolute value is 2i. No equality of individual increments X_j or Y_j is needed. QED.

**Lemma 2 (entropy threshold).** If

    2^N > 1 + sum_j |Y_j|,

there are two cycles whose lengths differ by 2i.

*Proof.* There are 2^N subsets. All their sums lie between the sum of negative Y_j and the sum of positive Y_j, an inclusive integer interval containing at most 1+sum|Y_j| points. Pigeonhole and Lemma 1. QED.

This is the correct replacement for the equal-increment hypothesis in Pass XXIII. Equal increments are merely the easiest way for subset-sum collisions to arise. Example with **all distinct** Y's: 1+2=3 already supplies the relation and hence the 2i switch.

**Lemma 3 (vertex-budget version).** If the necklace has n vertices and its short theta leg has length i, then

    sum_j |Y_j| <= n + (i-1)N.

Consequently, 2^N > 1+n+(i-1)N guarantees an exact 2i cycle-length difference.

*Proof.* Let L_{j,2} be the leg on which the outgoing connector meets theta block j. In Lyngsie–Merker's notation, Y_j=d_j-b_j, where b_j is the length from the attachment point to one branch vertex along L_{j,2} and d_j-i the length to the other branch vertex. Hence |Y_j| <= |L_{j,2}|+i. Because the theta blocks are vertex-disjoint, sum_j |L_{j,2}| <= sum_j(|V(theta_j)|-1) <= n-N. Sum over j. QED.

**Sharpness of the counting method:** for Y_j=2^{j-1}, all 2^N subset sums are distinct and sum_j|Y_j|=2^N-1. The strict inequality in Lemma 2 fails at equality. This does not prove that the corresponding necklace lacks a 2i difference by some *other* route choice.

## 2. Many disjoint exact switches (PROVED)

**Theorem 4 (quantitative packing).** Choose any integer r>=1. Partition floor(N/r) blocks into disjoint consecutive groups of r. Let

    T = sum_j |Y_j|,   m = max(0, floor(N/r)-floor(T/(2^r-1))).

Then the necklace contains cycles of all lengths in

    L, L+2i, L+4i, ..., L+2i*m

for some L (and possibly more lengths).

*Proof.* A group without an equal-subset-sum collision must have at least 2^r distinct integer subset sums, so its sum of |Y_j| is at least 2^r-1 by Lemma 2 contraposition. Thus at most floor(T/(2^r-1)) groups are bad. Every good group has the two simple-route choices in Lemma 1 with length difference exactly 2i. Pick the shorter choice as baseline in every group; disjoint groups are independent and remain compatible with the necklace scaffold. By selecting any of the m switches we obtain every k from 0 through m. QED.

In particular, one may replace T by the bound n+(i-1)N. The theorem works with completely different increments in each block and yields an absolute (not merely modular) arithmetic progression. It applies to any theta(i) necklace, not just one produced by Lemma 5.13.

A resulting dyadic certificate is valid only if this progression contains an actual power of two, including residue alignment. In particular, the theorem does **not** assert that L has the right parity/mod-4 class or that 2im is comparable to L.

## 3. No-go theorem: necklaces alone cannot force a dyadic cycle (PROVED)

**Theorem 5 (arbitrarily long clean theta necklaces).** For every N>=3 there exist connected subcubic theta(N,1) necklaces with exactly N theta blocks, equal route increments, and no cycle of power-of-two length. Moreover their connectors may be chosen arbitrarily long.

*Construction and proof.* In each block use a theta with three internally disjoint arms of lengths 5, 6, and 1 between branch vertices u,v. Put the incoming connector endpoint at distance 2 from u on the length-5 arm, and the outgoing endpoint at distance 2 from u on the length-6 arm. The three internal theta cycles have lengths 6, 7, and 11. The four incoming-to-outgoing routes have lengths 4, 6, 7, 7; in particular every block has the identical Y increment 3 and i=1.

Connect the N blocks cyclically by internally disjoint paths, each of edge length t. Any simple cycle in the resulting ring lies wholly inside one theta block or crosses all N connectors (contract the blocks to obtain the cycle graph C_N). Therefore all cycle lengths belong to

    {6,7,11} union [N(t+4), N(t+7)].

For any fixed N choose k so large that the open interval of integer values t satisfying

    2^k < N(t+4) <= N(t+7) < 2^(k+1)

is nonempty. Its real width is approximately 2^k/N-3, which tends to infinity. The internal cycles are non-dyadic, and all connector-crossing cycles lie strictly between consecutive powers of two. QED.

*Important scope:* these necklaces have many degree-two vertices and are **not** cubic 3-connected graphs. They refute the idea that theta-necklace route data or arbitrarily many equal increments suffice on their own to force a power-of-two cycle. They do not refute Erdős–Gyárfás. A solution using the published structural theorem must exploit the **ambient cubic completion**, including the third edges at degree-two vertices of the necklace or alternate cycles beyond the necklace.

## 4. Independently verified examples (COMPUTED)

- N=4, t=20: 120 vertices; internal cycles of lengths 6,7,11; all crossing cycles have lengths 96,...,108 (not necessarily every integer in that interval). Number of distinct simple cycles, including multiplicities: 268 = 4^4 + 3*4.
- N=5, t=40: 250 vertices; internal cycles of lengths 6,7,11; crossing lengths 220,...,235; 1039=4^5+3*5 simple cycles.

The Python checker builds the full undirected graph and uses `networkx.simple_cycles`; the C checker independently sums the symbolic route lengths and enumerates internal cycles. Exact length-count output streams agree byte for byte. Command lines, exit codes, and SHA-256 values are recorded in `pass24_certificates/manifest.md`.

## 5. Implications for the research plan

**PROVED:** The low-diversity/high-diversity dichotomy proposed in Pass XXIII can be replaced by a universal *subset-sum cancellation* mechanism; enough blocks relative to their total length budget force exact 2i switches.

**PROVED:** Even linear numbers of such switches (for equal-increment blocks) need not reach the dyadic scale. There exist arbitrarily large clean subcubic necklaces with the same local route freedom.

**OPEN, now the central target:** Prove an **ambient connector-repair theorem**: in a cubic 3-connected graph, a theta necklace whose connectors are too long relative to its switching budget necessarily has external attachments that generate a second cycle family near a dyadic boundary, or a new necklace with better length-scale ratio. This must quantify relative baseline, absolute width, residue alignment, and prescribed-edge avoidance if aiming for the stronger edge-avoidance property.

This target asks for a graph-theoretic mechanism not contained in the existing modular theorem. Repeating the same subset-sum argument or cataloguing gadgets will not close it.
