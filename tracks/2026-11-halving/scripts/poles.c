/* For each graph6 input: if exactly two vertices have degree 2 and all others degree >=3,
   print n, the set of lengths of simple paths between the two degree-2 vertices (bitmask),
   whether they are adjacent, and whether the graph has a C8. Input assumed C4-free (geng -f). */
#include <stdio.h>
#include <string.h>
#include <stdint.h>
static int n; static uint64_t adj[64]; static uint64_t lens; static int tgt;
static void dfs(int v, uint64_t vis, int len){
  if(v==tgt){ lens |= 1ULL<<len; return; }
  uint64_t c = adj[v] & ~vis;
  while(c){ int w=__builtin_ctzll(c); c&=c-1; dfs(w, vis|(1ULL<<w), len+1); }
}
static int T, S;
static int cyc(int v, uint64_t vis, int len){
  if(len==T-1) return (adj[v]>>S)&1;
  uint64_t c = adj[v] & ~vis & (~0ULL<<(S+1));
  while(c){ int w=__builtin_ctzll(c); c&=c-1; if(cyc(w,vis|(1ULL<<w),len+1)) return 1; }
  return 0;
}
int main(void){
  static char line[4096];
  while(fgets(line,sizeof line,stdin)){
    if(line[0]=='>'||line[0]=='\n') continue;
    n=line[0]-63; memset(adj,0,sizeof adj);
    int k=1,bit=0,x=0;
    for(int j=1;j<n;j++) for(int i=0;i<j;i++){
      if(bit==0){ x=line[k++]-63; bit=6; }
      bit--; if((x>>bit)&1){ adj[i]|=1ULL<<j; adj[j]|=1ULL<<i; }
    }
    int p[2], np=0, ok=1;
    for(int v=0;v<n;v++){ int d=__builtin_popcountll(adj[v]);
      if(d==2){ if(np<2) p[np]=v; np++; } else if(d<2) ok=0; }
    if(!ok||np!=2) continue;
    lens=0; tgt=p[1]; dfs(p[0],1ULL<<p[0],0);
    int c8=0; T=8; for(S=0;S<n&&!c8;S++) c8=cyc(S,1ULL<<S,0);
    line[strcspn(line,"\n")]=0;
    printf("%d %llu %d %d %s\n", n, (unsigned long long)lens, (int)((adj[p[0]]>>p[1])&1), c8, line);
  }
  return 0;
}
