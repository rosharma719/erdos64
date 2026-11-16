/* Independent checker written for this audit: reads graph6 (n<=62), reports
   counts of graphs with no C4, no C8, no power-of-two cycle at all. */
#include <stdio.h>
#include <string.h>
#include <stdint.h>
static int n; static uint64_t adj[64];
static int target, startv;
static int dfs(int v, uint64_t vis, int len){
  /* path from startv to v using len edges; all vertices > startv */
  if(len==target-1) return (adj[v]>>startv)&1;
  uint64_t c = adj[v] & ~vis & (~0ULL << (startv+1));
  while(c){ int w=__builtin_ctzll(c); c&=c-1;
    if(dfs(w, vis|(1ULL<<w), len+1)) return 1; }
  return 0;
}
static int hascycle(int L){
  if(L>n) return 0; target=L;
  for(startv=0; startv<n; startv++)
    if(dfs(startv, 1ULL<<startv, 0)) return 1;
  return 0;
}
int main(void){
  static char line[4096]; long total=0, noc4=0, noc48=0, nopow=0;
  while(fgets(line,sizeof line,stdin)){
    if(line[0]=='>'||line[0]=='\n') continue;
    n=line[0]-63; memset(adj,0,sizeof adj);
    int k=1, bit=0, x=0;
    for(int j=1;j<n;j++) for(int i=0;i<j;i++){
      if(bit==0){ x=line[k++]-63; bit=6; }
      bit--; if((x>>bit)&1){ adj[i]|=1ULL<<j; adj[j]|=1ULL<<i; }
    }
    total++;
    if(hascycle(4)) continue; noc4++;
    if(hascycle(8)) continue; noc48++;
    int any=0; for(int L=16; L<=n; L*=2) if(hascycle(L)){any=1;break;}
    if(!any){ nopow++; fputs(line,stderr); }
  }
  printf("total=%ld C4free=%ld C4C8free=%ld powerfree=%ld\n",total,noc4,noc48,nopow);
  return 0;
}
