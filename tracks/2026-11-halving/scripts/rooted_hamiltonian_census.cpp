// Independent C++ cross-check for rooted_hamiltonian_matching.py.
// Exhaustive Hamilton-cycle chord matching enumeration for even orders 4..16.
// This checks root-avoiding cycles C4 and C8 by canonical DFS.
// The remaining matching edges form a perfect matching disjoint from the
// fixed Hamilton cycle C=0..n-1. Root 0 is excluded from the search.
#include <bits/stdc++.h>
using namespace std;
int N=16, cnt[5]={},bade=0, matches[32], out=0; unsigned adj[32];
bool has_cycle_k(int k){
  auto dfs=[&](auto&& self,int start,int u,unsigned used,int depth)->bool{
   if(depth==k) return (adj[u]>>start)&1u;
   unsigned a=adj[u] & ~used & ~((1u<<(start+1))-1u);
   while(a){int w=__builtin_ctz(a);a&=a-1; if(self(self,start,w,used|(1u<<w),depth+1))return true;}
   return false;
  };
  for(int s=1;s<N;++s)if(dfs(dfs,s,s,1u<<s,1))return true;
  return false;
}
void work(){
 cnt[0]++;
 for(int i=0;i<N;i++)adj[i]=1u<<((i+1)%N)|1u<<((i+N-1)%N)|1u<<matches[i];
 adj[1]&=~1u; adj[N-1]&=~1u;
 for(int i=0;i<N;i++)adj[i]&=~1u;
 if(has_cycle_k(4)) {cnt[1]++;return;}
 if(has_cycle_k(8)) {cnt[2]++;return;}
 cnt[3]++;
 // print first survivors as matchings
 if(out<30){for(int i=0;i<N;i++)if(i<matches[i])cout<<i<<"-"<<matches[i]<<",";cout<<"\n";out++;}
}
void rec(unsigned rem){
 if(!rem){work();return;}
 int i=__builtin_ctz(rem);rem^=1u<<i;
 for(int j=i+1;j<N;j++)if(rem>>j&1u){
  int d=j-i;
  if(d==1||d==N-1)continue;
  if(i!=0&&(d==3||d==7||d==15))continue;
  matches[i]=j;matches[j]=i;
  rec(rem^(1u<<j));
 }
}
int main(int argc,char** argv){if(argc>1)N=atoi(argv[1]);if(N<4||N>16||N%2){cerr<<"even n in [4,16] required\n";return 1;}rec((1u<<N)-1);cerr<<"n="<<N<<" filtered matchings="<<cnt[0]<<" C4="<<cnt[1]<<" C8="<<cnt[2]<<" survive="<<cnt[3]<<"\n";}
