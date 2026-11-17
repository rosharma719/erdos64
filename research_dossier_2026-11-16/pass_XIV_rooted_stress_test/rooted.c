/* rooted.c — root-robustness checker for dyadic cycles.
 * For each graph6 line on stdin: for every vertex r, find a simple cycle of
 * length in {4,8,16,32,64,...} (<= n) that avoids r.  Search for a fixed L is
 * exhaustive (canonical minimum start vertex + BFS-distance pruning), so a
 * reported root-critical vertex is a proof, modulo code correctness.
 * Output per graph: n, min degree, per-length counts of roots first covered,
 * and any root-critical vertices.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 32768
#define MAXD 8
static int n, deg[MAXN], adj[MAXN][MAXD];
static int onpath[MAXN], path[MAXN], dist[MAXN], que[MAXN], banned[MAXN];
static long long nodes;

static int parse(const char *s) {
  const unsigned char *p = (const unsigned char *)s;
  int N;
  if (p[0] != 126) { N = p[0] - 63; p += 1; }
  else if (p[1] != 126) { N = ((p[1]-63)<<12)|((p[2]-63)<<6)|(p[3]-63); p += 4; }
  else return -1;
  if (N > MAXN) return -1;
  n = N; memset(deg, 0, sizeof(int)*n);
  int bit = 0; int k = 0;
  for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) {
    if (bit == 0) { k = *p++ - 63; bit = 6; }
    bit--;
    if ((k >> bit) & 1) {
      if (deg[i] >= MAXD || deg[j] >= MAXD) return -2;
      adj[i][deg[i]++] = j; adj[j][deg[j]++] = i;
    }
  }
  return n;
}

static int L, S;
/* DFS: path[0..d-1], current end u=path[d-1], need cycle of exactly L back to S */
static int dfs(int u, int d) {
  nodes++;
  if (d == L) {
    for (int t = 0; t < deg[u]; t++) if (adj[u][t] == S) return 1;
    return 0;
  }
  for (int t = 0; t < deg[u]; t++) {
    int v = adj[u][t];
    if (onpath[v] || banned[v] || v < S) continue;
    if (dist[v] < 0 || dist[v] > L - d) continue; /* need v..S in L-d edges */
    onpath[v] = 1; path[d] = v;
    if (dfs(v, d + 1)) return 1;
    onpath[v] = 0;
  }
  return 0;
}

static void bfs(int s) {
  for (int i = 0; i < n; i++) dist[i] = -1;
  int h = 0, t = 0; dist[s] = 0; que[t++] = s;
  while (h < t) { int u = que[h++];
    for (int k = 0; k < deg[u]; k++) { int v = adj[u][k];
      if (dist[v] < 0 && !banned[v] && v >= s) { dist[v] = dist[u] + 1; que[t++] = v; } } }
}

/* find cycle of length LL avoiding root r; returns 1 and leaves path[] */
static int find_cycle(int LL, int r) {
  L = LL;
  memset(banned, 0, sizeof(int)*n); banned[r] = 1;
  for (int s = 0; s < n; s++) {
    if (s == r) continue;
    S = s; bfs(s);
    memset(onpath, 0, sizeof(int)*n);
    onpath[s] = 1; path[0] = s;
    if (dfs(s, 1)) return 1;
  }
  return 0;
}

static int read_edges(FILE *f) {
  int u, v, mx = -1; n = 0; memset(deg, 0, sizeof deg);
  char buf[256];
  while (fgets(buf, sizeof buf, f)) {
    if (sscanf(buf, "%d %d", &u, &v) != 2) continue;
    if (u > mx) mx = u; if (v > mx) mx = v;
    if (u >= MAXN || v >= MAXN || deg[u] >= MAXD || deg[v] >= MAXD) return -1;
    adj[u][deg[u]++] = v; adj[v][deg[v]++] = u;
  }
  n = mx + 1; return n;
}
static int MINE = 2;
int main(int argc, char **argv) {
  if (argc > 1) MINE = atoi(argv[1]);
  int edgemode = (argc > 2 && !strcmp(argv[2], "edges"));
  static char line[1 << 20];
  int gi = 0; int once = 0;
  while (edgemode ? !once++ : (fgets(line, sizeof line, stdin) != NULL)) {
    if (edgemode) { gi++; if (read_edges(stdin) < 0) { printf("edge parse error\n"); return 1; } goto have; }
    size_t len = strlen(line); while (len && (line[len-1]=='\n'||line[len-1]=='\r')) line[--len]=0;
    if (!len) continue;
    if (line[0] == '>') continue;
    gi++;
    if (parse(line) < 0) { printf("graph %d: parse error\n", gi); continue; }
    have:;
    int mind = 99; for (int i = 0; i < n; i++) if (deg[i] < mind) mind = deg[i];
    if (getenv("FREECHECK")) { printf("graph %d n=%d has:", gi, n);
      for (int LL = 4; LL <= atoi(getenv("FREECHECK")); LL *= 2) printf(" C%d=%d", LL, find_cycle(LL, n));
      printf("\n"); fflush(stdout); continue; }
    static int covered[MAXN]; memset(covered, 0, sizeof(int)*n);
    int bylen[16] = {0}; int crit = 0; nodes = 0;
    static int incyc[MAXN];
    for (int r = 0; r < n; r++) {
      if (covered[r]) continue;
      int ok = 0;
      for (int e = MINE, LL = 1 << MINE; LL <= n; e++, LL *= 2) {
        if (find_cycle(LL, r)) {
          memset(incyc, 0, sizeof(int)*n);
          for (int i = 0; i < L; i++) { if (incyc[path[i]] || path[i] == r) { printf("SELFCHECK FAIL\n"); exit(2);} incyc[path[i]] = 1; }
          for (int i = 0; i < L; i++) { int a = path[i], b = path[(i+1)%L], ok2 = 0;
            for (int t = 0; t < deg[a]; t++) if (adj[a][t] == b) ok2 = 1;
            if (!ok2) { printf("SELFCHECK FAIL edge\n"); exit(2);} }
          if (getenv("WITNESS")) { printf("W %d %d %d", gi, r, L); for (int i = 0; i < L; i++) printf(" %d", path[i]); printf("\n"); }
          int newc = 0;
          for (int v = 0; v < n; v++) if (!incyc[v] && !covered[v]) { covered[v] = 1; newc++; }
          bylen[e] += newc; ok = 1; break;
        }
      }
      if (!ok) { crit++; printf("graph %d: ROOT-CRITICAL vertex %d\n", gi, r); covered[r] = 1; }
    }
    printf("graph %d n=%d mindeg=%d", gi, n, mind);
    for (int e = 2; e < 16; e++) if (bylen[e]) printf(" C%d:%d", 1 << e, bylen[e]);
    printf(" critical=%d dfsnodes=%lld\n", crit, nodes);
    fflush(stdout);
  }
  return 0;
}
