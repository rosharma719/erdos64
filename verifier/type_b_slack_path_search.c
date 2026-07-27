/* Independent C-language cross-check for the one-slack 28-edge remainder
 * layer (type_b_one_slack.md, Section 4).
 *
 * Reads graph6-encoded candidate graphs from stdin, one per line, each on
 * n vertices (n given via -n, default 19). For each graph, checks:
 *   - degree sequence matches one of the two admissible profiles
 *     (2,3^{n-1}) or (2,2,4,3^{n-3})
 *   - contains no simple cycle of length 4, 8, or 16 (exhaustive DFS,
 *     written from scratch: independent of verifier/cycle_detect.py's
 *     Python DFS and of networkx's simple_cycles and of the pysat
 *     encoding in verifier/type_b_slack_path_sat.py).
 *
 * Prints a summary: graphs checked, graphs surviving the C4/C8/C16-free
 * test. A survivor count of 0 means this C implementation independently
 * confirms the layer is empty.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 32

static int n_vertices;
static int adj[MAXN][MAXN];
static int visited[MAXN];
static int path[MAXN];

/* Decode one graph6 line (n <= 62 case: single leading byte n+63) into
 * the global adjacency matrix. Returns 0 on success, -1 on malformed
 * input (e.g. truncated line). */
static int decode_graph6(const char *line, int n) {
    memset(adj, 0, sizeof(adj));
    int total_bits = n * (n - 1) / 2;
    const unsigned char *body = (const unsigned char *)(line + 1);
    int body_len = (int)strlen((const char *)body);
    int needed_bytes = (total_bits + 5) / 6;
    if (body_len < needed_bytes) {
        return -1;
    }
    int i = 1, j = 0;
    int bit_pos = 0;
    for (int b = 0; b < total_bits; b++) {
        int byte_idx = bit_pos / 6;
        int bit_in_byte = 5 - (bit_pos % 6);
        int value = body[byte_idx] - 63;
        int bit = (value >> bit_in_byte) & 1;
        if (bit) {
            adj[i][j] = 1;
            adj[j][i] = 1;
        }
        bit_pos++;
        j++;
        if (j == i) {
            i++;
            j = 0;
        }
    }
    return 0;
}

/* Exhaustive DFS search (independent implementation) for a simple cycle
 * of length exactly L, rooted at each possible minimum vertex, restricted
 * to vertices >= that root, matching the same correctness principle as
 * verifier/cycle_detect.py but written independently in C. */
static int found_cycle;

static void dfs(int start, int u, int depth, int L) {
    if (found_cycle) return;
    if (depth == L - 1) {
        if (adj[u][start]) {
            found_cycle = 1;
        }
        return;
    }
    for (int w = start; w < n_vertices; w++) {
        if (!adj[u][w]) continue;
        if (visited[w]) continue;
        visited[w] = 1;
        path[depth + 1] = w;
        dfs(start, w, depth + 1, L);
        visited[w] = 0;
        if (found_cycle) return;
    }
}

static int has_cycle_len(int L) {
    for (int s = 0; s < n_vertices; s++) {
        memset(visited, 0, sizeof(visited));
        visited[s] = 1;
        path[0] = s;
        found_cycle = 0;
        dfs(s, s, 0, L);
        if (found_cycle) return 1;
    }
    return 0;
}

static int degree_matches_family(int *degrees, int n) {
    int cnt2 = 0, cnt3 = 0, cnt4 = 0, other = 0;
    for (int v = 0; v < n; v++) {
        if (degrees[v] == 2) cnt2++;
        else if (degrees[v] == 3) cnt3++;
        else if (degrees[v] == 4) cnt4++;
        else other++;
    }
    if (other) return 0;
    if (cnt2 == 1 && cnt3 == n - 1 && cnt4 == 0) return 1; /* Family I */
    if (cnt2 == 2 && cnt3 == n - 3 && cnt4 == 1) return 1; /* Family II */
    return 0;
}

int main(int argc, char **argv) {
    n_vertices = 19;
    for (int a = 1; a < argc; a++) {
        if (strcmp(argv[a], "-n") == 0 && a + 1 < argc) {
            n_vertices = atoi(argv[++a]);
        }
    }

    char line[4096];
    long checked = 0, malformed = 0, degree_mismatch = 0;
    long c4_found = 0, c8_found = 0, c16_found = 0, survivors = 0;

    while (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) {
            line[--len] = '\0';
        }
        if (len == 0) continue;
        checked++;
        if (decode_graph6(line, n_vertices) != 0) {
            malformed++;
            continue;
        }
        int degrees[MAXN];
        for (int v = 0; v < n_vertices; v++) {
            int d = 0;
            for (int w = 0; w < n_vertices; w++) d += adj[v][w];
            degrees[v] = d;
        }
        if (!degree_matches_family(degrees, n_vertices)) {
            degree_mismatch++;
            continue;
        }
        if (has_cycle_len(4)) { c4_found++; continue; }
        if (has_cycle_len(8)) { c8_found++; continue; }
        if (n_vertices >= 16 && has_cycle_len(16)) { c16_found++; continue; }
        survivors++;
        fprintf(stderr, "SURVIVOR: %s\n", line);
    }

    printf("{\n");
    printf("  \"checked\": %ld,\n", checked);
    printf("  \"malformed\": %ld,\n", malformed);
    printf("  \"degree_mismatch\": %ld,\n", degree_mismatch);
    printf("  \"c4_found\": %ld,\n", c4_found);
    printf("  \"c8_found\": %ld,\n", c8_found);
    printf("  \"c16_found\": %ld,\n", c16_found);
    printf("  \"survivors\": %ld\n", survivors);
    printf("}\n");
    return 0;
}
