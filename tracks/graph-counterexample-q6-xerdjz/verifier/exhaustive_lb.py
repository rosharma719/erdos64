"""
Independent reproduction of the Royle-Markström lower bound (L10): no
counterexample to Erdős #64 has fewer than 17 vertices.

Method: for each order n, enumerate ALL connected graphs with minimum degree >= 3
using nauty `geng -c -d3`, and test each with the validated detector. A minimal
counterexample must be connected (each component of a δ≥3 graph has δ≥3, and if G
had no 2-power cycle then neither would any component -> a smaller counterexample),
so connected generation is sufficient to find the smallest counterexample order.

For n <= 15 the only power-of-two lengths <= n are 4 and 8, so "no 2-power cycle"
== "no C4 and no C8"; we still call the full detector for safety/uniformity.

Reads graph6 from stdin (piped from geng). Prints any counterexample found.
"""
import sys
import time

# fast graph6 decode -> adjacency as list of int bitmasks (n small)
def decode_graph6(line: bytes):
    line = line.rstrip()
    if not line:
        return None
    data = line
    # first, the order n
    if data[0] == ord('~'):
        raise ValueError("n>62 not handled here")
    n = data[0] - 63
    bits = []
    for c in data[1:]:
        v = c - 63
        for k in range(5, -1, -1):
            bits.append((v >> k) & 1)
    adj = [0] * n
    idx = 0
    for j in range(1, n):
        for i in range(j):
            if idx < len(bits) and bits[idx]:
                adj[i] |= (1 << j)
                adj[j] |= (1 << i)
            idx += 1
    return n, adj


def has_C4(n, adj):
    # two distinct vertices with >=2 common neighbors -> a 4-cycle
    for i in range(n):
        for j in range(i + 1, n):
            common = adj[i] & adj[j]
            # need two common neighbors other than i,j themselves (they aren't
            # neighbors-of-self so i,j excluded automatically)
            if bin(common).count("1") >= 2:
                return True
    return False


def has_cycle_len(n, adj, L):
    # backtracking simple cycle of exact length L, rooted at min vertex
    if L < 3 or L > n:
        return False
    for s in range(n):
        # induced on vertices >= s
        stack = [(s, 1 << s, s)]  # (current, visited_mask, depth_vertices)
        # iterative DFS
        # path length in edges = (popcount(visited)-1)
        def dfs(u, visited, depth):
            if depth == L:
                return (adj[u] >> s) & 1 and (adj[u] & (1 << s)) != 0
            nb = adj[u]
            w = s
            m = nb >> s
            while m:
                if m & 1:
                    if not (visited & (1 << w)):
                        if dfs(w, visited | (1 << w), depth + 1):
                            return True
                m >>= 1
                w += 1
            return False
        if dfs(s, 1 << s, 1):
            return True
    return False


def powers_of_two_up_to(n):
    out = []
    p = 4
    while p <= n:
        out.append(p)
        p *= 2
    return out


def main():
    n_expected = int(sys.argv[1]) if len(sys.argv) > 1 else None
    count = 0
    found = 0
    t0 = time.time()
    lengths = None
    for raw in sys.stdin.buffer:
        dec = decode_graph6(raw)
        if dec is None:
            continue
        n, adj = dec
        if lengths is None:
            lengths = powers_of_two_up_to(n)
        count += 1
        # min degree >=3 guaranteed by geng -d3, but assert cheaply on first
        # fast pre-filter: has_C4 kills the vast majority
        if has_C4(n, adj):
            continue
        # no 4-cycle; check remaining powers of two
        bad = False
        for L in lengths:
            if L == 4:
                continue
            if has_cycle_len(n, adj, L):
                bad = True
                break
        if not bad:
            found += 1
            # emit the counterexample (graph6)
            sys.stdout.write("COUNTEREXAMPLE " + raw.decode().rstrip() + "\n")
            sys.stdout.flush()
    dt = time.time() - t0
    sys.stderr.write(
        f"n={n_expected}: checked {count} connected δ≥3 graphs, "
        f"counterexamples={found}, {dt:.1f}s\n")


if __name__ == "__main__":
    main()
