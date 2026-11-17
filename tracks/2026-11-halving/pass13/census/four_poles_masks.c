/* Independent order-6 clean 4-pole census from all 2^15 labeled graphs.
 * Connectivity, degree checks, simple cycle enumeration, permutations and
 * isomorphism-canonical bitmask all implemented without graph libraries.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 6
#define M 15
static int ei[M],ej[M],adj[N][N],best,perm[N],used[N];
static unsigned allclen;
static struct Row {int key,count,bridges; unsigned cycles;} rows[100];
static int nr;

static void setadj(unsigned bits){
 memset(adj,0,sizeof(adj));
 for(int i=0;i<M;i++) if(bits&(1u<<i))adj[ei[i]][ej[i]]=adj[ej[i]][ei[i]]=1;
}
static int degrees(void){
 int n2=0,n3=0;
 for(int i=0;i<N;i++){
  int d=0;for(int j=0;j<N;j++)d+=adj[i][j];
  if(d==2)n2++;else if(d==3)n3++;else return 0;
 }
 return n2==4&&n3==2;
}
static int connected(void){
 int seen[N]={0},q[N],b=0,e=0;q[e++]=0;seen[0]=1;
 while(b<e){int x=q[b++];for(int y=0;y<N;y++)if(adj[x][y]&&!seen[y]){seen[y]=1;q[e++]=y;}}
 return e==N;
}
static void dfs(int start,int at,int vis,int len){
 for(int v=0;v<N;v++)if(adj[at][v]){
  if(v==start && len>=2)allclen|=1u<<(len+1);
  else if(!(vis&(1<<v)))dfs(start,v,vis|(1<<v),len+1);
 }
}
static unsigned cycles(void){
 allclen=0;
 for(int i=0;i<N;i++)dfs(i,i,1<<i,0);
 return allclen;
}
static int bridges(void){
 int count=0;
 for(int i=0;i<M;i++)if(adj[ei[i]][ej[i]]){
  adj[ei[i]][ej[i]]=adj[ej[i]][ei[i]]=0;
  if(!connected())count++;
  adj[ei[i]][ej[i]]=adj[ej[i]][ei[i]]=1;
 }
 return count;
}
static void canonical_rec(int depth){
 if(depth==N){
  int bits=0;
  for(int i=0;i<M;i++)if(adj[ei[i]][ej[i]]){
   int a=perm[ei[i]],b=perm[ej[i]];if(a>b){int t=a;a=b;b=t;}
   for(int j=0;j<M;j++)if(ei[j]==a&&ej[j]==b){bits|=1<<j;break;}
  }
  if(bits<best)best=bits;
  return;
 }
 for(int i=0;i<N;i++)if(!used[i]){used[i]=1;perm[depth]=i;canonical_rec(depth+1);used[i]=0;}
}
static int cmp(const void *a,const void *b){
 const struct Row *x=a,*y=b;return x->key-y->key;
}
int main(void){
 int t=0;for(int a=0;a<N;a++)for(int b=a+1;b<N;b++){ei[t]=a;ej[t]=b;t++;}
 for(unsigned bits=0;bits<(1u<<M);bits++){
  if(__builtin_popcount(bits)!=7)continue;
  setadj(bits);
  if(!degrees()||!connected())continue;
  unsigned cyc=cycles();if(cyc & (1u<<4))continue;
  int br=bridges();best=1<<M;memset(used,0,sizeof(used));canonical_rec(0);
  int idx=-1;for(int j=0;j<nr;j++)if(rows[j].key==best){idx=j;break;}
  if(idx<0){idx=nr++;rows[idx]=(struct Row){.key=best,.count=0,.bridges=br,.cycles=cyc};}
  if(rows[idx].bridges!=br||rows[idx].cycles!=cyc){fprintf(stderr,"class mismatch\n");return 2;}
  rows[idx].count++;
 }
 qsort(rows,nr,sizeof(rows[0]),cmp);
 for(int j=0;j<nr;j++){
  printf("%04x\t%d\t%d\t",rows[j].key,rows[j].count,rows[j].bridges);
  int first=1;
  for(int len=3;len<=N;len++)if(rows[j].cycles&(1u<<len)){
   if(!first)printf(",");
   printf("%d",len);first=0;
  }
  printf("\n");
 }
 return 0;
}
