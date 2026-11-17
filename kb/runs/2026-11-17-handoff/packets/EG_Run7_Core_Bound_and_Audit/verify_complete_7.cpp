// Standalone exhaustive enumeration; requires a C++17 compiler.
// Each simple labeled graph on 7 vertices corresponds to a 21-bit integer.
// Checks: (1) max edges among 2-degenerate C4-free labeled 7-graphs;
// (2) all eight-vertex 11-edge (C4,C8)-free 2-degenerate extensions;
// (3) no such 8-vertex extremal accepts a degree-2 ninth vertex.
#include <array>
#include <cstdint>
#include <iostream>
#include <cassert>
using namespace std;
using A = array<uint16_t,9>;
constexpr int pop(unsigned x){return __builtin_popcount(x);}

bool deg2(const A& a, int n){
  unsigned alive=(1u<<n)-1;
  while(alive){
    int pick=-1;
    for(int v=0;v<n;v++)
      if((alive&(1u<<v)) && pop(a[v]&alive)<=2){pick=v;break;}
    if(pick<0)return false;
    alive &=~(1u<<pick);
  }
  return true;
}
bool c4(const A& a,int n){
  for(int u=0;u<n;u++)for(int v=u+1;v<n;v++)
    if(pop(a[u]&a[v])>=2)return true;
  return false;
}
bool simple_path(const A& a,int u,int target,int edges,unsigned used){
  if(edges==0)return u==target;
  unsigned nb=a[u]&~used;
  while(nb){
    unsigned bit=nb&-nb;nb-=bit;
    if(simple_path(a,__builtin_ctz(bit),target,edges-1,used|bit))return true;
  }
  return false;
}
A add2(A a,int n,int u,int v){
  a[n]=(1u<<u)|(1u<<v);
  a[u]|=1u<<n;a[v]|=1u<<n;
  return a;
}
int main(){
  uint64_t tested=0,eligible=0,eligible9=0,extremals=0,valid9=0;
  int max7=0;
  const uint32_t limit=1u<<21;
  int eu[21],ev[21],k=0;
  for(int u=0;u<7;u++)for(int v=u+1;v<7;v++){
    eu[k]=u;ev[k]=v;k++;
  }
  for(uint32_t mask=0;mask<limit;mask++){
    tested++;
    A a={};
    int e=pop(mask);
    for(int j=0;j<21;j++)if(mask&(1u<<j)){
      int u=eu[j],v=ev[j];a[u]|=1u<<v;a[v]|=1u<<u;
    }
    if(c4(a,7) || !deg2(a,7))continue;
    eligible++;
    if(e>max7)max7=e;
    if(e!=9)continue;
    eligible9++;
    for(int u=0;u<7;u++)for(int v=u+1;v<7;v++){
      if(a[u]&a[v])continue; // adding vertex creates C4
      if(simple_path(a,u,v,6,1u<<u))continue; // creates C8
      A b=add2(a,7,u,v); // 8 vertices, 11 edges
      assert(!c4(b,8) && deg2(b,8));
      extremals++;
      for(int x=0;x<8;x++)for(int y=x+1;y<8;y++){
        bool creates4=(b[x]&b[y])!=0;
        bool creates8=simple_path(b,x,y,6,1u<<x);
        if(!creates4 && !creates8){
          valid9++;
          cerr<<"COUNTEREXAMPLE: labelled 7 graph="<<mask<<" first pair="<<u<<","<<v<<" extend pair="<<x<<","<<y<<"\n";
        }
      }
    }
  }
  cout<<"enumerated="<<tested<<" eligible_C4free_2deg_7="<<eligible
      <<" max_edges_7="<<max7<<" eligible_edges9="<<eligible9
      <<" labelled_8vertex_11edge_extremals="<<extremals
      <<" degree2_extensions_without_C4_C8="<<valid9<<"\n";
  assert(tested==(1u<<21));
  assert(max7==9 && extremals>0 && valid9==0);
  cout<<"PASS: every 2deg C4,C8-free n=8 graph has <=11 edges;"
      <<" n=8 m=11 cannot accept 9th degree-2 vertex without C4 or C8.\n";
}
