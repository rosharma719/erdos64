/* Direct slot-matching generator for the zero-slack delta=2 Type-B bridge
 * remainder layer (see type_b_delta2_zero_slack.md).
 *
 * A minimum-order delta=2 bridge B has |V(B)|=20 and a required length-19
 * x-y path, which is Hamiltonian in B. R=B-x has 19 vertices and the path
 * P=p_0..p_18 (p_0=a, p_18=y) spans ALL of R -- there is no off-path
 * vertex, unlike the one-slack (delta=1) B20 case. |E(R)|=28 forces the
 * degree sequence 2,3^18 (Family I) or 2^2,3^16,4 (Family II) by the same
 * excess-counting argument as before. Family I reuses the existing
 * 86,047-graph certificate verbatim (see type_b_delta2_zero_slack.md
 * Section 7); this program generates and checks Family II, whose degree-4
 * role is one of the 17 internal path vertices p_1..p_17 (no z role,
 * since there is no off-path vertex here).
 *
 * Path edges: (i,i+1) for i=0..17 (18 edges, 19 vertices, indices 0..18).
 * Non-path edges to add: exactly 10 (28-18=10).
 * Deficits: a=p_0:1, y=p_18:1, ordinary internal p_i (i!=role):1, role p_j:2.
 * Total deficit = 1+1+16*1+2 = 20 = 2*10.
 *
 * Cycle pruning: adding edge uv creates a k-cycle iff the graph so far has
 * a simple u-v path of length k-1. Reject on length 3 (C4) or 7 (C8).
 * C16 is checked post-hoc, not pruned incrementally (same policy and same
 * has_cycle_len routine as verifier/type_b_slack_path_search.c, reused
 * here by direct inclusion of an equivalent implementation, written fresh
 * for this file -- not literally #included from that file, so this is a
 * fresh independent instance of the same well-tested logic, unit-tested
 * again below).
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NV 19
#define NCAND 153

static int adj[NV][NV];
static int visited[NV];
static int path_buf[NV];
static int n_vertices = NV;

static int found_cycle;

static void dfs_cycle(int start, int u, int depth, int L) {
    if (found_cycle) return;
    if (depth == L - 1) {
        if (adj[u][start]) found_cycle = 1;
        return;
    }
    for (int w = start; w < n_vertices; w++) {
        if (!adj[u][w]) continue;
        if (visited[w]) continue;
        visited[w] = 1;
        path_buf[depth + 1] = w;
        dfs_cycle(start, w, depth + 1, L);
        visited[w] = 0;
        if (found_cycle) return;
    }
}

static int has_cycle_len(int L) {
    for (int s = 0; s < n_vertices; s++) {
        memset(visited, 0, sizeof(visited));
        visited[s] = 1;
        path_buf[0] = s;
        found_cycle = 0;
        dfs_cycle(s, s, 0, L);
        if (found_cycle) return 1;
    }
    return 0;
}

static int cand_u[NCAND], cand_v[NCAND];
static int ncand;
static int deficit[NV];
static int avail[NV];
static int visited2[NV];
static long dfs_nodes = 0;
static long solutions_found = 0;
static int current_role;

static void build_candidates(void) {
    ncand = 0;
    for (int u = 0; u < NV; u++) {
        for (int v = u + 1; v < NV; v++) {
            int is_path_edge = (v == u + 1 && u <= 17);
            if (is_path_edge) continue;
            cand_u[ncand] = u;
            cand_v[ncand] = v;
            ncand++;
        }
    }
}

static int exists_path_len_helper(int cur, int target, int remaining) {
    if (remaining == 0) return cur == target;
    for (int w = 0; w < NV; w++) {
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
    for (int w = 0; w < NV; w++) {
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

static void emit_solution(void) {
    solutions_found++;
    int edges_u[10], edges_v[10], ne = 0;
    for (int i = 0; i < ncand; i++) {
        int u = cand_u[i], v = cand_v[i];
        if (adj[u][v]) {
            edges_u[ne] = u;
            edges_v[ne] = v;
            ne++;
        }
    }

    int c4 = has_cycle_len(4);
    int c8 = has_cycle_len(8);
    int c16 = has_cycle_len(16);
    int c16_witness[16];
    if (c16) {
        for (int k = 0; k < 16; k++) c16_witness[k] = path_buf[k];
    }

    /* terminal-closing witnesses: a=vertex0, y=vertex18. r=2,6,14 close to
     * C4,C8,C16 through a-x-y (two closing edges). */
    int ay2[3], has_ay2 = record_path_len(0, 18, 2, ay2);
    int ay6[7], has_ay6 = record_path_len(0, 18, 6, ay6);
    int ay14[15], has_ay14 = record_path_len(0, 18, 14, ay14);

    int degrees[NV];
    for (int v = 0; v < NV; v++) {
        int d = 0;
        for (int w = 0; w < NV; w++) d += adj[v][w];
        degrees[v] = d;
    }

    printf("{\"role\": %d, \"edges\": [", current_role);
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
    printf(", \"has_ay_len2\": %s", has_ay2 ? "true" : "false");
    if (has_ay2) {
        printf(", \"ay_len2\": [");
        for (int k = 0; k < 3; k++) printf("%s%d", k ? "," : "", ay2[k]);
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
    for (int v = 0; v < NV; v++) printf("%s%d", v ? "," : "", degrees[v]);
    printf("]}\n");
    fflush(stdout);
}

static void gsearch(int idx, int edges_included) {
    dfs_nodes++;
    if (edges_included == 10) {
        emit_solution();
        return;
    }
    if (idx == ncand) return;
    if (edges_included + (ncand - idx) < 10) return;

    int u = cand_u[idx], v = cand_v[idx];

    avail[u]--;
    avail[v]--;

    if (deficit[u] <= avail[u] && deficit[v] <= avail[v]) {
        gsearch(idx + 1, edges_included);
    }

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
    memset(adj, 0, sizeof(adj));
    for (int i = 0; i <= 17; i++) {
        adj[i][i + 1] = adj[i + 1][i] = 1;
    }
    for (int v = 0; v < NV; v++) deficit[v] = 1;
    deficit[0] = 1;  /* a */
    deficit[18] = 1; /* y */
    deficit[role] = 2;

    for (int v = 0; v < NV; v++) {
        int pd;
        if (v == 0 || v == 18) pd = 1;
        else pd = 2;
        avail[v] = (NV - 1) - pd;
    }

    long nodes_before = dfs_nodes;
    long sols_before = solutions_found;
    gsearch(0, 0);
    fprintf(stderr, "role=%d dfs_nodes=%ld solutions=%ld\n",
            role, dfs_nodes - nodes_before, solutions_found - sols_before);
}

static void run_generate_all(void) {
    build_candidates();
    fprintf(stderr, "candidate edges: %d\n", ncand);
    for (int role = 1; role <= 17; role++) {
        run_role(role);
    }
    fprintf(stderr, "TOTAL dfs_nodes=%ld TOTAL solutions=%ld\n", dfs_nodes, solutions_found);
}

/* ---- unit tests for has_cycle_len, independent of any candidate search ---- */
static void run_selftest(void) {
    n_vertices = 4;
    memset(adj, 0, sizeof(adj));
    int e[][2] = {{0,1},{0,2},{0,3},{1,2},{1,3},{2,3}};
    for (int i = 0; i < 6; i++) { adj[e[i][0]][e[i][1]] = adj[e[i][1]][e[i][0]] = 1; }
    if (!has_cycle_len(4)) { fprintf(stderr, "SELFTEST FAIL: K4 should have C4\n"); exit(1); }

    n_vertices = 8;
    memset(adj, 0, sizeof(adj));
    for (int v = 0; v < 8; v++) { adj[v][(v+1)%8] = adj[(v+1)%8][v] = 1; }
    if (!has_cycle_len(8)) { fprintf(stderr, "SELFTEST FAIL: C8 graph should have C8\n"); exit(1); }
    if (has_cycle_len(4)) { fprintf(stderr, "SELFTEST FAIL: C8 graph should not have C4\n"); exit(1); }

    n_vertices = 5;
    memset(adj, 0, sizeof(adj));
    for (int v = 0; v < 4; v++) { adj[v][v+1] = adj[v+1][v] = 1; }
    if (has_cycle_len(4)) { fprintf(stderr, "SELFTEST FAIL: path graph should have no cycle\n"); exit(1); }

    n_vertices = NV;
    fprintf(stderr, "selftest passed: K4=C4, C8-graph=C8/no-C4, path=no-cycle\n");
}

int main(int argc, char **argv) {
    int generate_mode = 0, selftest_mode = 0;
    for (int a = 1; a < argc; a++) {
        if (strcmp(argv[a], "-generate-all") == 0) generate_mode = 1;
        if (strcmp(argv[a], "-selftest") == 0) selftest_mode = 1;
    }
    if (selftest_mode) {
        run_selftest();
        return 0;
    }
    if (generate_mode) {
        run_generate_all();
        return 0;
    }
    fprintf(stderr, "usage: %s [-generate-all | -selftest]\n", argv[0]);
    return 1;
}
