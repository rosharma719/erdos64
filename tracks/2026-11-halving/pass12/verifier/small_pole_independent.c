/* Independent fixed-size C bitmask DFS for all rooted deletions (n<=11).
 * Accepts explicit adjacency lists of poles, not graph6 or NetworkX data.
 */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
static int n;static uint32_t adj[32],lengths;
static void dfs(int start,int v,uint32_t used,int len){
 for(int w=0;w<n;w++)if(adj[v]>>w&1){
  if(w==start && len>=3)lengths|=1u<<len;
  else if(w>start && !(used>>w&1))dfs(start,w,used|1u<<w,len+1);
 }
}
int main(int argc,char**argv){
 if(argc!=2)return 2;
 FILE*f=fopen(argv[1],"r");if(!f)return 3;
 int cap,i,root,edges;
 while(fscanf(f,"%d %d %d %d %d",&cap,&i,&root,&n,&edges)==5){
  if(n>31||n<3||edges>100){fclose(f);return 4;}
  memset(adj,0,sizeof(adj));
  for(int j=0;j<edges;j++){
   int a,b;if(fscanf(f,"%d %d",&a,&b)!=2||a<0||b<0||a>=n||b>=n){fclose(f);return 5;}
   adj[a]|=1u<<b;adj[b]|=1u<<a;
  }
  int degree2=0;for(int j=0;j<n;j++){int d=__builtin_popcount(adj[j]);if(d==2)degree2++;else if(d!=3){fclose(f);return 6;}}
  if(degree2!=3){fclose(f);return 7;}
  lengths=0;for(int j=0;j<n;j++)dfs(j,j,1u<<j,1);
  int good=!(lengths & ((1u<<4)|(1u<<8)|(1u<<16)));
  printf("ROOT|%d|%d|%d|%d|",cap,i,root,good);
  int first=1;for(int j=3;j<n+1;j++)if(lengths>>j&1){if(!first)putchar(',');printf("%d",j);first=0;}putchar('\n');
 }
 fclose(f);return 0;
}
