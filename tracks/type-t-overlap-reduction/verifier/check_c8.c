/* check_c8: fast C8-survivor checker for the 4-or-8 small-order search (Erdos #64).
 * Reads graph6 (one graph/line, n<=62) from stdin. A "survivor" of the 4-or-8
 * theorem is a graph with NO C4 and NO C8 (C16 is irrelevant to 4-or-8; it only
 * matters for Erdos-Gyarfas, so we report it but do not require its absence).
 * Input is expected C4-free (geng -f); c4_seen must stay 0 (sanity gate).
 * Prints each survivor as "SURVIVOR <g6> c16=<0|1>".
 * stderr summary: "checked <N> graphs c4_seen=<X> c8free_survivors=<M>".
 * Decode/DFS logic identical to check_g6.c so the two share a validated core.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n;
static uint64_t adj[64];
static int popcount64(uint64_t x){ return __builtin_popcountll(x); }

static int decode(const char *line){
    if(line[0]=='\0' || line[0]=='\n') return 0;
    const unsigned char *p=(const unsigned char*)line;
    n = p[0]-63;
    for(int i=0;i<n;i++) adj[i]=0;
    const unsigned char *d=p+1;
    long total = (long)n*(n-1)/2;
    int col=1, row=0;
    for(long b=0;b<total;b++){
        int byteidx = b/6, within = b%6;
        unsigned char val = d[byteidx]-63;
        int bit = (val >> (5-within)) & 1;
        if(bit){ adj[row] |= (1ULL<<col); adj[col] |= (1ULL<<row); }
        row++;
        if(row==col){ row=0; col++; }
    }
    return 1;
}

static int has_C4(void){
    for(int i=0;i<n;i++)
        for(int j=i+1;j<n;j++)
            if(popcount64(adj[i]&adj[j])>=2) return 1;
    return 0;
}

static int L_target, root;
static int dfs(int u, uint64_t vis, int depth){
    if(depth==L_target) return (adj[u]>>root)&1;
    uint64_t m = adj[u] >> root;      /* only vertices >= root */
    int w=root;
    while(m){
        if(m&1){
            if(!((vis>>w)&1))
                if(dfs(w, vis|(1ULL<<w), depth+1)) return 1;
        }
        m>>=1; w++;
    }
    return 0;
}
static int has_cycle_len(int L){
    if(L<3||L>n) return 0;
    L_target=L;
    for(int s=0;s<n;s++){ root=s; if(dfs(s, 1ULL<<s, 1)) return 1; }
    return 0;
}

int main(void){
    char line[4096];
    long count=0, c4_seen=0, found=0;
    while(fgets(line,sizeof line,stdin)){
        if(!decode(line)) continue;
        count++;
        if(has_C4()){ c4_seen++; continue; }   /* has C4: contains 4-cycle, not a survivor */
        if(has_cycle_len(8)) continue;          /* has C8: contains 8-cycle, not a survivor */
        found++;
        int c16 = has_cycle_len(16);
        char *nl=strchr(line,'\n'); if(nl)*nl=0;
        printf("SURVIVOR %s c16=%d\n", line, c16);
        fflush(stdout);
    }
    fprintf(stderr,"checked %ld graphs c4_seen=%ld c8free_survivors=%ld\n", count, c4_seen, found);
    return 0;
}
