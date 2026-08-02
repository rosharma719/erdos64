/* Independent batch detector for exact C4/C8/C16 presence masks.
 *
 * Reads one graph6 graph per line from stdin (n<=62) and prints one integer:
 * bit 0 = C4 present, bit 1 = C8 present, bit 2 = C16 present.
 * The implementation is independent of Python/networkx and evaluates every
 * requested length even when a shorter forbidden cycle is already present.
 */
#include <stdint.h>
#include <stdio.h>

static int n;
static uint64_t adj[64];

static int decode(const char *line) {
    if (line[0] == '\0' || line[0] == '\n') return 0;
    const unsigned char *p = (const unsigned char *)line;
    n = p[0] - 63;
    if (n < 0 || n > 62) return -1;
    for (int i = 0; i < n; ++i) adj[i] = 0;
    const unsigned char *data = p + 1;
    long total = (long)n * (n - 1) / 2;
    int row = 0, col = 1;
    for (long bit_index = 0; bit_index < total; ++bit_index) {
        unsigned char value = data[bit_index / 6] - 63;
        int bit = (value >> (5 - bit_index % 6)) & 1;
        if (bit) {
            adj[row] |= 1ULL << col;
            adj[col] |= 1ULL << row;
        }
        if (++row == col) {
            row = 0;
            ++col;
        }
    }
    return 1;
}

static int has_c4(void) {
    for (int u = 0; u < n; ++u)
        for (int v = u + 1; v < n; ++v)
            if (__builtin_popcountll(adj[u] & adj[v]) >= 2) return 1;
    return 0;
}

static int target, root;

static int dfs(int current, uint64_t visited, int vertices_used) {
    if (vertices_used == target)
        return (int)((adj[current] >> root) & 1ULL);
    uint64_t candidates = adj[current];
    /* Root is the least-labelled cycle vertex, removing duplicate roots and
       making the exact search finite without changing existence. */
    if (root > 0) candidates &= ~((1ULL << root) - 1ULL);
    candidates &= ~visited;
    while (candidates) {
        int next = __builtin_ctzll(candidates);
        candidates &= candidates - 1;
        if (dfs(next, visited | (1ULL << next), vertices_used + 1)) return 1;
    }
    return 0;
}

static int has_cycle_length(int length) {
    if (length < 3 || length > n) return 0;
    target = length;
    for (root = 0; root < n; ++root)
        if (dfs(root, 1ULL << root, 1)) return 1;
    return 0;
}

int main(void) {
    char line[4096];
    long count = 0;
    while (fgets(line, sizeof line, stdin)) {
        int decoded = decode(line);
        if (decoded == 0) continue;
        if (decoded < 0) return 2;
        unsigned mask = 0;
        if (has_c4()) mask |= 1U;
        if (has_cycle_length(8)) mask |= 2U;
        if (has_cycle_length(16)) mask |= 4U;
        printf("%u\n", mask);
        ++count;
    }
    fprintf(stderr, "checked %ld graph6 records\n", count);
    return 0;
}
