/* Exhaustive labeled edge-subset enumeration, independently canonicalized
 * under the 2!*(n-2)! permutations preserving the two degree-2 vertices.
 * n<=6 only; unlike the Python checker this does not use an atlas.
 */
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
static int n,edA[15],edB[15],m,perms[48][6],pc,cur[6],used[6];
static uint64_t seen[128];static int sc;
static int pop(int x){return __builtin_popcount((unsigned)x);}
static void perm(int pos){
 if(pos==n){memcpy(perms[pc++],cur,n*sizeof(int));return;}
 for(int k=(pos<2?0:2);k<(pos<2?2:n);k++)if(!used[k]){
   used[k]=1;cur[pos]=k;perm(pos+1);used[k]=0;
 }
}
static int adjacency(uint32_t mask,int a,int b){
 if(a>b){int t=a;a=b;b=t;}
 for(int i=0;i<m;i++)if(edA[i]==a&&edB[i]==b)return mask>>i&1;
 return 0;
}
static uint64_t canon(uint32_t mask){
 uint64_t best=UINT64_MAX;
 for(int k=0;k<pc;k++){
  uint64_t x=0;
  for(int i=0;i<m;i++)if(adjacency(mask,perms[k][edA[i]],perms[k][edB[i]]))x|=(uint64_t)1<<i;
  if(x<best)best=x;
 }
 return best;
}
static int has_four(uint32_t mask){
 for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)for(int d=c+1;d<n;d++){
  int x[4]={a,b,c,d};
  for(int s=0;s<3;s++){
    int y[4]={x[0],x[1+(s%3)],x[1+((s+1)%3)],x[1+((s+2)%3)]};
    if(adjacency(mask,y[0],y[1])&&adjacency(mask,y[1],y[2])&&adjacency(mask,y[2],y[3])&&adjacency(mask,y[3],y[0]))return 1;
  }
 }
 return 0;
}
static int connected(uint32_t mask){
 uint32_t have=1,old=0;
 while(have!=old){old=have;for(int i=0;i<m;i++)if(mask>>i&1){
  if(have>>edA[i]&1)have|=1u<<edB[i];
  if(have>>edB[i]&1)have|=1u<<edA[i];
 }}
 return have==((1u<<n)-1);
}
static void solve(int k){
 n=k;m=0;for(int a=0;a<n;a++)for(int b=a+1;b<n;b++){edA[m]=a;edB[m++]=b;}
 pc=0;memset(used,0,sizeof(used));perm(0);sc=0;int count=0,clean=0;
 for(uint32_t mask=0;mask<(1u<<m);mask++){
  int deg[6]={0};for(int i=0;i<m;i++)if(mask>>i&1){deg[edA[i]]++;deg[edB[i]]++;}
  if(deg[0]!=2||deg[1]!=2)continue;
  int good=1;for(int i=2;i<n;i++)if(deg[i]!=3)good=0;
  if(!good||!connected(mask))continue;
  uint64_t can=canon(mask);int dup=0;
  for(int i=0;i<sc;i++)if(seen[i]==can){dup=1;break;}
  if(dup)continue;
  if(sc>=128){fprintf(stderr,"overflow\n");exit(4);}
  seen[sc++]=can;count++;if(!has_four(mask))clean++;
 }
 printf("2POLE|%d|%d|%d\n",n,count,clean);
}
int main(void){solve(4);solve(6);return 0;}
