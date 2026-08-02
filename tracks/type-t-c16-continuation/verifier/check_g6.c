/* Fast independent power-of-two-cycle checker for Erdos #64 lower-bound
 * reproduction. Reads graph6 (one graph per line) from stdin, each assumed
 * connected with min degree >= 3 (as produced by `geng -c -d3 n`).
 *
 * A counterexample must have NO simple cycle of length 4, 8, 16, ... For n<=15
 * that means no C4 and no C8. We check no-C4 (cheap) then no-C8, no-C16 (DFS).
 * Any graph passing all checks is printed as "COUNTEREXAMPLE <g6>".
 *
 * Independent of the Python detector; the two must agree (cross-checked).
 * Handles n <= 62 (single graph6 header byte); adjacency as 64-bit masks.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n;
static uint64_t adj[64];

static int popcount64(uint64_t x){ return __builtin_popcountll(x); }

/* decode one graph6 line (no '~', n<=62). returns 1 ok, 0 blank/eof */
static int decode(const char *line){
    if(line[0]=='\0' || line[0]=='\n') return 0;
    const unsigned char *p=(const unsigned char*)line;
    n = p[0]-63;
    for(int i=0;i<n;i++) adj[i]=0;
    /* bits are upper triangle column-major: for j=1..n-1, for i=0..j-1 */
    int bitpos=0;
    int i=1; /* we'll iterate (i<j) pairs */
    int col=1, row=0;
    const unsigned char *d=p+1;
    /* reconstruct byte/bit stream */
    /* total bits = n*(n-1)/2 */
    long total = (long)n*(n-1)/2;
    for(long b=0;b<total;b++){
        int byteidx = b/6;
        int within = b%6;
        unsigned char val = d[byteidx]-63;
        int bit = (val >> (5-within)) & 1;
        if(bit){ adj[row] |= (1ULL<<col); adj[col] |= (1ULL<<row); }
        /* advance (row,col) with row<col */
        row++;
        if(row==col){ row=0; col++; }
    }
    (void)i;(void)bitpos;
    return 1;
}

static int has_C4(void){
    for(int i=0;i<n;i++)
        for(int j=i+1;j<n;j++)
            if(popcount64(adj[i]&adj[j])>=2) return 1;
    return 0;
}

/* DFS for a simple cycle of exact length L, rooted at min vertex s. */
static int L_target, root;
static int dfs(int u, uint64_t vis, int depth){
    if(depth==L_target){
        return (adj[u]>>root)&1;
    }
    uint64_t m = adj[u] >> root;      /* only vertices >= root */
    int w=root;
    while(m){
        if(m&1){
            if(!((vis>>w)&1)){
                if(dfs(w, vis|(1ULL<<w), depth+1)) return 1;
            }
        }
        m>>=1; w++;
    }
    return 0;
}
static int has_cycle_len(int L){
    if(L<3||L>n) return 0;
    L_target=L;
    for(int s=0;s<n;s++){
        root=s;
        if(dfs(s, 1ULL<<s, 1)) return 1;
    }
    return 0;
}

int main(void){
    char line[4096];
    long count=0, found=0;
    while(fgets(line,sizeof line,stdin)){
        if(!decode(line)) continue;
        count++;
        if(has_C4()) continue;              /* has 4-cycle: not a counterexample */
        int bad=0;
        for(int L=8; L<=n; L*=2){
            if(has_cycle_len(L)){ bad=1; break; }
        }
        if(!bad){
            found++;
            /* strip newline */
            char *nl=strchr(line,'\n'); if(nl)*nl=0;
            printf("COUNTEREXAMPLE %s\n", line);
            fflush(stdout);
        }
    }
    fprintf(stderr,"checked %ld graphs, counterexamples=%ld\n", count, found);
    return 0;
}
