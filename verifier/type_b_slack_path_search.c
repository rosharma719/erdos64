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

/* ===========================================================================
 * Direct slot-matching generator for the Family II (2^2,3^16,4) layer.
 *
 * Fixed distinguished path p_0..p_17 (vertices 0..17), off-path vertex z
 * (vertex 18). Path edges (i,i+1) for i=0..16 are fixed. For a given role
 * (which vertex carries the single +1 degree excess beyond the base
 * 2,2,3^16,3 pattern -- see type_b_one_slack_resolution.md Section 1), this
 * enumerates every set of exactly 11 additional (non-path) edges giving the
 * exact required degree sequence, pruning any edge whose addition would
 * create a C4 or C8 (checked via the edge-local rule: adding edge uv creates
 * a k-cycle iff a simple u-v path of length k-1 already exists -- see
 * type_b_one_slack_resolution.md Section 3 for why this incremental check is
 * safe and why C16 is deferred to a post-hoc check instead of being pruned
 * incrementally).
 * ===========================================================================
 */

#define GNV 19
#define GNCAND 154

static int cand_u[GNCAND], cand_v[GNCAND];
static int ncand;
static int deficit[GNV];
static int avail[GNV];
static int visited2[GNV];
static long dfs_nodes = 0;
static long solutions_found = 0;
static int current_role; /* 1..16 = p_role carries the excess; 0 = z carries it */

static void build_candidates(void) {
    ncand = 0;
    for (int u = 0; u < GNV; u++) {
        for (int v = u + 1; v < GNV; v++) {
            int is_path_edge = (v == u + 1 && u <= 16);
            if (is_path_edge) continue;
            cand_u[ncand] = u;
            cand_v[ncand] = v;
            ncand++;
        }
    }
}

static int exists_path_len_helper(int cur, int target, int remaining) {
    if (remaining == 0) return cur == target;
    for (int w = 0; w < GNV; w++) {
        if (!adj[cur][w]) continue;
        if (visited2[w]) continue;
        if (w == target && remaining != 1) continue;
        visited2[w] = 1;
        if (exists_path_len_helper(w, target, remaining - 1)) {
            visited2[w] = 0;
            return 1;
        }
        visited2[w] = 0;
    }
    return 0;
}

static int exists_path_len(int u, int v, int L) {
    memset(visited2, 0, sizeof(visited2));
    visited2[u] = 1;
    return exists_path_len_helper(u, v, L);
}

static int record_path_len_helper(int cur, int target, int remaining, int *outpath, int pathlen) {
    outpath[pathlen] = cur;
    if (remaining == 0) return cur == target;
    for (int w = 0; w < GNV; w++) {
        if (!adj[cur][w]) continue;
        if (visited2[w]) continue;
        if (w == target && remaining != 1) continue;
        visited2[w] = 1;
        if (record_path_len_helper(w, target, remaining - 1, outpath, pathlen + 1)) {
            visited2[w] = 0;
            return 1;
        }
        visited2[w] = 0;
    }
    return 0;
}

static int record_path_len(int u, int v, int L, int *outpath) {
    memset(visited2, 0, sizeof(visited2));
    visited2[u] = 1;
    return record_path_len_helper(u, v, L, outpath, 0);
}

/* n_vertices/adj are the shared globals from the checker above. */

static void emit_solution(void) {
    solutions_found++;
    /* Collect the 11 included non-path edges. */
    int edges_u[11], edges_v[11], ne = 0;
    for (int i = 0; i < ncand; i++) {
        int u = cand_u[i], v = cand_v[i];
        if (adj[u][v]) {
            edges_u[ne] = u;
            edges_v[ne] = v;
            ne++;
        }
    }

    /* Self-consistency re-check: the completed graph must be C4/C8-free
     * (should always hold given incremental pruning; this independently
     * re-verifies using the SAME has_cycle_len routine used for Family I). */
    int c4 = has_cycle_len(4);
    int c8 = has_cycle_len(8);
    int c16 = has_cycle_len(16);
    int c16_witness[16];
    if (c16) {
        for (int k = 0; k < 16; k++) c16_witness[k] = path[k];
    }

    int ay6[7], has_ay6 = record_path_len(0, 17, 6, ay6);
    int ay14[15], has_ay14 = record_path_len(0, 17, 14, ay14);

    /* degree check */
    int degrees[GNV];
    for (int v = 0; v < GNV; v++) {
        int d = 0;
        for (int w = 0; w < GNV; w++) d += adj[v][w];
        degrees[v] = d;
    }

    printf("{\"role\": ");
    if (current_role == 0) printf("\"z\""); else printf("%d", current_role);
    printf(", \"edges\": [");
    for (int i = 0; i < ne; i++) {
        printf("%s[%d,%d]", i ? "," : "", edges_u[i], edges_v[i]);
    }
    printf("], \"c4\": %s, \"c8\": %s, \"c16\": %s", c4 ? "true" : "false",
           c8 ? "true" : "false", c16 ? "true" : "false");
    if (c16) {
        printf(", \"c16_witness\": [");
        for (int k = 0; k < 16; k++) printf("%s%d", k ? "," : "", c16_witness[k]);
        printf("]");
    }
    printf(", \"has_ay_len6\": %s", has_ay6 ? "true" : "false");
    if (has_ay6) {
        printf(", \"ay_len6\": [");
        for (int k = 0; k < 7; k++) printf("%s%d", k ? "," : "", ay6[k]);
        printf("]");
    }
    printf(", \"has_ay_len14\": %s", has_ay14 ? "true" : "false");
    if (has_ay14) {
        printf(", \"ay_len14\": [");
        for (int k = 0; k < 15; k++) printf("%s%d", k ? "," : "", ay14[k]);
        printf("]");
    }
    printf(", \"degrees\": [");
    for (int v = 0; v < GNV; v++) printf("%s%d", v ? "," : "", degrees[v]);
    printf("]}\n");
    fflush(stdout);
}

static void gsearch(int idx, int edges_included) {
    dfs_nodes++;
    if (edges_included == 11) {
        emit_solution();
        return;
    }
    if (idx == ncand) return;
    if (edges_included + (ncand - idx) < 11) return;

    int u = cand_u[idx], v = cand_v[idx];

    avail[u]--;
    avail[v]--;

    /* exclude branch */
    if (deficit[u] <= avail[u] && deficit[v] <= avail[v]) {
        gsearch(idx + 1, edges_included);
    }

    /* include branch */
    if (deficit[u] > 0 && deficit[v] > 0) {
        int c4 = exists_path_len(u, v, 3);
        int c8 = !c4 && exists_path_len(u, v, 7);
        if (!c4 && !c8) {
            adj[u][v] = adj[v][u] = 1;
            deficit[u]--;
            deficit[v]--;
            if (deficit[u] <= avail[u] && deficit[v] <= avail[v]) {
                gsearch(idx + 1, edges_included + 1);
            }
            deficit[u]++;
            deficit[v]++;
            adj[u][v] = adj[v][u] = 0;
        }
    }

    avail[u]++;
    avail[v]++;
}

static void run_role(int role) {
    current_role = role;
    n_vertices = GNV;
    memset(adj, 0, sizeof(adj));
    for (int i = 0; i <= 16; i++) {
        adj[i][i + 1] = adj[i + 1][i] = 1;
    }
    for (int v = 0; v < GNV; v++) deficit[v] = 0;
    deficit[0] = 1;  /* a */
    deficit[17] = 1; /* y */
    for (int i = 1; i <= 16; i++) deficit[i] = 1;
    deficit[18] = 3; /* z */
    if (role == 0) {
        deficit[18] = 4;
    } else {
        deficit[role] = 2;
    }
    for (int v = 0; v < GNV; v++) {
        int pd = 0;
        if (v >= 1 && v <= 16) pd = 2;
        else if (v == 0 || v == 17) pd = 1;
        else pd = 0; /* z */
        avail[v] = (GNV - 1) - pd;
    }

    long nodes_before = dfs_nodes;
    long sols_before = solutions_found;
    gsearch(0, 0);
    fprintf(stderr, "role=%s dfs_nodes=%ld solutions=%ld\n",
            role == 0 ? "z" : "p", dfs_nodes - nodes_before,
            solutions_found - sols_before);
}

static void run_generate_all(void) {
    build_candidates();
    fprintf(stderr, "candidate edges: %d\n", ncand);
    for (int role = 1; role <= 16; role++) {
        run_role(role);
    }
    run_role(0);
    fprintf(stderr, "TOTAL dfs_nodes=%ld TOTAL solutions=%ld\n", dfs_nodes, solutions_found);
}

int main(int argc, char **argv) {
    n_vertices = 19;
    int generate_mode = 0;
    for (int a = 1; a < argc; a++) {
        if (strcmp(argv[a], "-n") == 0 && a + 1 < argc) {
            n_vertices = atoi(argv[++a]);
        }
        if (strcmp(argv[a], "-generate-all") == 0) {
            generate_mode = 1;
        }
    }

    if (generate_mode) {
        run_generate_all();
        return 0;
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
