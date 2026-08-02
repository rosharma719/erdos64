/* Direct slot-matching generator: gap-two order-21 bridge, E=30 layer.
 * See type_b_order40_frontier.md Sections 3-4, rows G2-30-A1/A2/B1/B2/B3.
 *
 * R = B-x has 20 vertices: 19-vertex path p_0..p_18 (18 edges, p_0=a,
 * p_18=y) + one off-path vertex z (index 19). At E=30 (q=2), five
 * sub-cases from the integer partitions of 2 (see frontier doc):
 *   A1: one of {a,y} gains 2      -> degree sequence 4,2,3^18   (2 roles)
 *   A2: one ordinary vertex gains 2 -> 2^2,3^17,5               (18 roles)
 *   B1: both a,y gain 1            -> 3^20 (fully cubic)        (1 role)
 *   B2: one of {a,y} gains 1, one ordinary gains 1 -> 2,3^18,4  (36 roles)
 *   B3: two distinct ordinary vertices gain 1 each -> 2^2,3^16,4^2 (153 roles)
 * Total 210 role configurations, looped internally (like B20's -generate-all).
 *
 * Non-path edges: 30-18=12.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NV 20
#define NCAND 172
#define A_V 0
#define Y_V 18
#define Z_V 19

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
static char current_label[64];
static int target_edges;

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
    int edges_u[16], edges_v[16], ne = 0;
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

    int ay2[3], has_ay2 = record_path_len(A_V, Y_V, 2, ay2);
    int ay6[7], has_ay6 = record_path_len(A_V, Y_V, 6, ay6);
    int ay14[15], has_ay14 = record_path_len(A_V, Y_V, 14, ay14);

    int degrees[NV];
    for (int v = 0; v < NV; v++) {
        int d = 0;
        for (int w = 0; w < NV; w++) d += adj[v][w];
        degrees[v] = d;
    }

    printf("{\"label\": \"%s\", \"edges\": [", current_label);
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
    if (edges_included == target_edges) {
        emit_solution();
        return;
    }
    if (idx == ncand) return;
    if (edges_included + (ncand - idx) < target_edges) return;

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

/* base_deg[v] = path-induced degree for vertex v (before non-path edges) */
static int base_deg[NV];

static void run_config(const char *label, int *target_degree) {
    strncpy(current_label, label, sizeof(current_label) - 1);
    memset(adj, 0, sizeof(adj));
    for (int i = 0; i <= 17; i++) adj[i][i + 1] = adj[i + 1][i] = 1;

    for (int v = 0; v < NV; v++) {
        deficit[v] = target_degree[v] - base_deg[v];
        avail[v] = (NV - 1) - base_deg[v];
    }

    long nodes_before = dfs_nodes;
    long sols_before = solutions_found;
    gsearch(0, 0);
    fprintf(stderr, "label=%s dfs_nodes=%ld solutions=%ld\n", label,
            dfs_nodes - nodes_before, solutions_found - sols_before);
}

static void run_generate_all(void) {
    build_candidates();
    target_edges = 12;
    fprintf(stderr, "candidate edges: %d target_edges=%d\n", ncand, target_edges);

    for (int v = 0; v < NV; v++) {
        if (v == A_V || v == Y_V) base_deg[v] = 1;
        else if (v == Z_V) base_deg[v] = 0;
        else base_deg[v] = 2;
    }

    int td[NV];
    char label[64];

    /* A1: a or y gains 2 -> degree 4 */
    for (int who = 0; who < 2; who++) {
        int target_v = who == 0 ? A_V : Y_V;
        /* baseline: all ordinary vertices target 3, a,y target 2, then bump target_v to 4 */
        for (int v = 0; v < NV; v++) {
            if (v == A_V || v == Y_V) td[v] = 2;
            else td[v] = 3;
        }
        td[target_v] = 4;
        snprintf(label, sizeof(label), "A1_%s", who == 0 ? "a" : "y");
        run_config(label, td);
    }

    /* A2: one ordinary vertex gains 2 -> degree 5 */
    for (int ov = 0; ov < NV; ov++) {
        if (ov == A_V || ov == Y_V) continue;
        for (int v = 0; v < NV; v++) {
            if (v == A_V || v == Y_V) td[v] = 2;
            else td[v] = 3;
        }
        td[ov] = 5;
        snprintf(label, sizeof(label), "A2_v%d", ov);
        run_config(label, td);
    }

    /* B1: both a,y gain 1 -> fully cubic 3^20 */
    for (int v = 0; v < NV; v++) td[v] = 3;
    run_config("B1_cubic", td);

    /* B2: one of a,y gains 1 (degree 3), one ordinary gains 1 (degree 4) */
    for (int who = 0; who < 2; who++) {
        int term_v = who == 0 ? A_V : Y_V;
        for (int ov = 0; ov < NV; ov++) {
            if (ov == A_V || ov == Y_V) continue;
            for (int v = 0; v < NV; v++) {
                if (v == A_V || v == Y_V) td[v] = 2;
                else td[v] = 3;
            }
            td[term_v] = 3;
            td[ov] = 4;
            snprintf(label, sizeof(label), "B2_%s_v%d", who == 0 ? "a" : "y", ov);
            run_config(label, td);
        }
    }

    /* B3: two distinct ordinary vertices gain 1 each -> degree 4 each */
    for (int ov1 = 0; ov1 < NV; ov1++) {
        if (ov1 == A_V || ov1 == Y_V) continue;
        for (int ov2 = ov1 + 1; ov2 < NV; ov2++) {
            if (ov2 == A_V || ov2 == Y_V) continue;
            for (int v = 0; v < NV; v++) {
                if (v == A_V || v == Y_V) td[v] = 2;
                else td[v] = 3;
            }
            td[ov1] = 4;
            td[ov2] = 4;
            snprintf(label, sizeof(label), "B3_v%d_v%d", ov1, ov2);
            run_config(label, td);
        }
    }

    fprintf(stderr, "TOTAL dfs_nodes=%ld TOTAL solutions=%ld\n", dfs_nodes, solutions_found);
}

static void run_selftest(void) {
    n_vertices = 4;
    memset(adj, 0, sizeof(adj));
    int e[][2] = {{0,1},{0,2},{0,3},{1,2},{1,3},{2,3}};
    for (int i = 0; i < 6; i++) adj[e[i][0]][e[i][1]] = adj[e[i][1]][e[i][0]] = 1;
    if (!has_cycle_len(4)) { fprintf(stderr, "SELFTEST FAIL: K4\n"); exit(1); }

    n_vertices = 8;
    memset(adj, 0, sizeof(adj));
    for (int v = 0; v < 8; v++) adj[v][(v+1)%8] = adj[(v+1)%8][v] = 1;
    if (!has_cycle_len(8)) { fprintf(stderr, "SELFTEST FAIL: C8\n"); exit(1); }
    if (has_cycle_len(4)) { fprintf(stderr, "SELFTEST FAIL: C8-graph has no C4\n"); exit(1); }

    n_vertices = 5;
    memset(adj, 0, sizeof(adj));
    for (int v = 0; v < 4; v++) adj[v][v+1] = adj[v+1][v] = 1;
    if (has_cycle_len(4)) { fprintf(stderr, "SELFTEST FAIL: path has no cycle\n"); exit(1); }

    n_vertices = NV;
    fprintf(stderr, "selftest passed\n");
}

int main(int argc, char **argv) {
    int selftest_mode = 0;
    for (int a = 1; a < argc; a++) {
        if (strcmp(argv[a], "-selftest") == 0) selftest_mode = 1;
    }
    if (selftest_mode) { run_selftest(); return 0; }
    run_generate_all();
    return 0;
}
