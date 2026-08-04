// t=2 analogue of the audited t4_intersection_filter.cpp / t3_intersection_filter.cpp.
// Same exact triangle-quotient interval theorem; N=26 (quotient order for
// t=2 is 30-2*2=26), marks=2 (C(26,2)=325 candidates/quotient), 2 triangles
// (6 marked-expanded vertices) + 24 unmarked = 30 total. allowed_bits is the
// independently-derived t=2 table (derive_t3_table.py's allowed_e(L,2)),
// same derivation method already validated by exactly reproducing the
// externally-supplied, audited t=4 table before being trusted for any
// other t.
#include <bits/stdc++.h>
using namespace std;

struct G { int n=0; vector<uint32_t> a; vector<pair<int,int>> e; };
static bool add_edge(G& g,int u,int v){ if(u==v||((g.a[u]>>v)&1u))return false; g.a[u]|=1u<<v;g.a[v]|=1u<<u;g.e.push_back({min(u,v),max(u,v)});return true; }
static bool connected(const G& g){if(!g.n)return true;uint32_t seen=1,q=1;while(q){int u=__builtin_ctz(q);q&=q-1;uint32_t z=g.a[u]&~seen;seen|=z;q|=z;}return __builtin_popcount(seen)==g.n;}
static bool parse_graph6(string line,G&g){
 if(line.rfind(">>graph6<<",0)==0)line=line.substr(10);while(!line.empty()&&isspace((unsigned char)line.back()))line.pop_back();size_t p=0;while(p<line.size()&&isspace((unsigned char)line[p]))++p;if(p)line.erase(0,p);if(line.empty())return false;
 int n;size_t pos;unsigned char c0=line[0];if(c0!='~'){n=int(c0)-63;pos=1;}else{if(line.size()<4||line[1]=='~')return false;n=((int(line[1])-63)<<12)|((int(line[2])-63)<<6)|(int(line[3])-63);pos=4;}if(n<=0||n>31)return false;g=G{n,vector<uint32_t>(n),{}};int x=0,y=1;
 for(;pos<line.size()&&y<n;++pos){int val=int((unsigned char)line[pos])-63;if(val<0||val>63)return false;for(int b=5;b>=0&&y<n;--b){if((val>>b)&1)add_edge(g,x,y);if(++x==y){x=0;++y;}}}return y==n;
}
static string to_graph6(const G&g){string s;if(g.n>62)throw runtime_error("n too large");s.push_back(char(g.n+63));int val=0,cnt=0;for(int y=1;y<g.n;++y)for(int x=0;x<y;++x){val=(val<<1)|int((g.a[x]>>y)&1u);if(++cnt==6){s.push_back(char(val+63));val=cnt=0;}}if(cnt){val<<=6-cnt;s.push_back(char(val+63));}return s;}
static G expand_marked(const G&q,uint32_t S){vector<int>m,c;for(int v=0;v<q.n;++v)(((S>>v)&1u)?m:c).push_back(v);if(m.size()!=2)return{};int mid[32],cid[32],port[32][32];fill(begin(mid),end(mid),-1);fill(begin(cid),end(cid),-1);memset(port,-1,sizeof(port));for(int i=0;i<2;++i)mid[m[i]]=i;for(int i=0;i<(int)c.size();++i)cid[c[i]]=6+i;for(int i=0;i<2;++i){int k=0,u=m[i];uint32_t z=q.a[u];while(z){int v=__builtin_ctz(z);z&=z-1;port[u][v]=3*i+k++;}if(k!=3)return{};}G g{30,vector<uint32_t>(30),{}};for(int i=0;i<2;++i){int b=3*i;add_edge(g,b,b+1);add_edge(g,b+1,b+2);add_edge(g,b,b+2);}for(auto [u,v]:q.e){int U=((S>>u)&1u)?port[u][v]:cid[u],V=((S>>v)&1u)?port[v][u]:cid[v];if(!add_edge(g,U,V))return{};}return g;}
static bool cycle_find_dfs(const G&g,int s,int first,int u,int depth,int L,uint32_t used){if(depth==L)return ((g.a[u]>>s)&1u)&&first<u;uint32_t z=g.a[u]&~used;z&=~((1u<<(s+1))-1u);while(z){int v=__builtin_ctz(z);z&=z-1;if(cycle_find_dfs(g,s,first,v,depth+1,L,used|(1u<<v)))return true;}return false;}
static bool has_cycle(const G&g,int L){for(int s=0;s<g.n;++s){uint32_t z=g.a[s]&~((1u<<(s+1))-1u);while(z){int v=__builtin_ctz(z);z&=z-1;if(cycle_find_dfs(g,s,v,v,2,L,(1u<<s)|(1u<<v)))return true;}}return false;}
static long long count_cycle_dfs(const G&g,int s,int first,int u,int depth,int L,uint32_t used){if(depth==L)return (((g.a[u]>>s)&1u)&&first<u)?1:0;long long ans=0;uint32_t z=g.a[u]&~used;z&=~((1u<<(s+1))-1u);while(z){int v=__builtin_ctz(z);z&=z-1;ans+=count_cycle_dfs(g,s,first,v,depth+1,L,used|(1u<<v));}return ans;}
static long long count_cycles(const G&g,int L){long long ans=0;for(int s=0;s<g.n;++s){uint32_t z=g.a[s]&~((1u<<(s+1))-1u);while(z){int v=__builtin_ctz(z);z&=z-1;ans+=count_cycle_dfs(g,s,v,v,2,L,(1u<<s)|(1u<<v));}}return ans;}
static void save_edges(const G&g,const string&p){ofstream o(p);o<<g.n<<' '<<g.e.size()<<'\n';auto e=g.e;sort(e.begin(),e.end());for(auto [u,v]:e)o<<u<<' '<<v<<'\n';}

static uint8_t allowed_bits(int L){
 // bit e says |C cap S|=e is allowed, t=2. Independently derived (same
 // method validated against the audited t=4 table -- see derive_t3_table.py).
 static const uint8_t A[17]={0,0,0,
  (1u<<2),         // 3
  (1u<<1),         // 4
  (1u<<0)|(1u<<1), // 5
  (1u<<0),         // 6
  (1u<<0)|(1u<<2), // 7
  (1u<<1)|(1u<<2), // 8
  (1u<<0)|(1u<<1)|(1u<<2), // 9
  (1u<<0)|(1u<<1)|(1u<<2), // 10
  (1u<<0)|(1u<<1)|(1u<<2), // 11
  (1u<<0)|(1u<<1), // 12
  (1u<<0)|(1u<<1), // 13
  (1u<<0),         // 14
  (1u<<0)|(1u<<2), // 15
  (1u<<1)|(1u<<2)  // 16
 };
 return A[L];
}

struct Stats{
 uint64_t lines=0,parsed=0,cubic=0,conn=0,graphs_with_candidates=0;
 uint64_t cycles_seen[17]={}, candidate_tests=0, initial_markings=0, final_markings=0;
 uint64_t literal_checked=0,literal_mismatch=0,counterexamples=0;
};

struct IntersectSolver{
 const G&q; Stats&st; vector<uint32_t> cand; bool stop_cycles=false;
 IntersectSolver(const G&Q,Stats&S):q(Q),st(S){
  cand.reserve(325);for(int a=0;a<25;++a)for(int b=a+1;b<26;++b)cand.push_back((1u<<a)|(1u<<b));
  st.initial_markings+=cand.size();
 }
 bool apply_cycle(int L,uint32_t M){
  ++st.cycles_seen[L]; uint8_t allow=allowed_bits(L); size_t w=0;
  for(uint32_t S:cand){++st.candidate_tests;int e=__builtin_popcount(S&M);if((allow>>e)&1u)cand[w++]=S;}
  cand.resize(w);return cand.empty();
 }
 void dfs(int s,int first,int u,int depth,int L,uint32_t used){
  if(stop_cycles)return;
  if(depth==L){if(((q.a[u]>>s)&1u)&&first<u)stop_cycles=apply_cycle(L,used);return;}
  uint32_t z=q.a[u]&~used;z&=~((1u<<(s+1))-1u);while(z&&!stop_cycles){int v=__builtin_ctz(z);z&=z-1;dfs(s,first,v,depth+1,L,used|(1u<<v));}
 }
 void enumerate_length(int L){for(int s=0;s<q.n&&!stop_cycles;++s){uint32_t z=q.a[s]&~((1u<<(s+1))-1u);while(z&&!stop_cycles){int v=__builtin_ctz(z);z&=z-1;dfs(s,v,v,2,L,(1u<<s)|(1u<<v));}}}
 void solve(){
  static const int order[]={3,4,8,16,12,13,14,15,5,6,7,9,10,11};
  for(int L:order){enumerate_length(L);if(cand.empty())break;}
  st.final_markings+=cand.size();if(!cand.empty())++st.graphs_with_candidates;
 }
};

int main(int argc,char**argv){string outdir=".";uint64_t maxg=ULLONG_MAX;bool all=false,verify=true;
 for(int i=1;i<argc;++i){string a=argv[i];if(a=="--outdir"&&i+1<argc)outdir=argv[++i];else if(a=="--max"&&i+1<argc)maxg=stoull(argv[++i]);else if(a=="--all")all=true;else if(a=="--no-literal-verify")verify=false;else{cerr<<"usage: t2_intersection_filter [--outdir D] [--max N] [--all] [--no-literal-verify] < q.g6\n";return 2;}}
 filesystem::create_directories(outdir);Stats st;string line;auto t0=chrono::steady_clock::now();
 while(getline(cin,line)&&st.parsed<maxg){++st.lines;G q;if(!parse_graph6(line,q))continue;++st.parsed;bool cub=q.n==26&&q.e.size()==39;for(int v=0;v<q.n&&cub;++v)cub&=__builtin_popcount(q.a[v])==3;if(!cub)continue;++st.cubic;if(!connected(q))continue;++st.conn;
  IntersectSolver sol(q,st);sol.solve();
  for(uint32_t S:sol.cand){++st.literal_checked;if(verify){G g=expand_marked(q,S);bool literal=(g.n==30&&g.e.size()==45&&connected(g)&&count_cycles(g,3)==2&&!has_cycle(g,4)&&!has_cycle(g,8)&&!has_cycle(g,16));if(!literal){++st.literal_mismatch;cerr<<"THEOREM_MISMATCH q="<<st.parsed<<" S="<<S<<"\n";continue;}}
   ++st.counterexamples;string b=outdir+"/counterexample_q"+to_string(st.parsed)+"_S"+to_string(S);save_edges(q,b+"_quotient.edges");G g=expand_marked(q,S);save_edges(g,b+"_expanded.edges");ofstream m(b+".json");m<<"{\n  \"graph_index\": "<<st.parsed<<",\n  \"marked_mask\": "<<S<<",\n  \"quotient_graph6\": \""<<to_graph6(q)<<"\"\n}\n";cerr<<"COUNTEREXAMPLE q="<<st.parsed<<" S="<<S<<"\n";if(!all)goto done;
  }
  if(st.parsed%1000==0)cerr<<"graphs="<<st.parsed<<" candidates="<<st.final_markings<<" checks="<<st.candidate_tests<<"\n";
 }
done: double sec=chrono::duration<double>(chrono::steady_clock::now()-t0).count();
 cout<<"{\n  \"lines\": "<<st.lines<<",\n  \"parsed\": "<<st.parsed<<",\n  \"cubic26\": "<<st.cubic<<",\n  \"connected\": "<<st.conn<<",\n  \"initial_markings\": "<<st.initial_markings<<",\n  \"candidate_intersection_tests\": "<<st.candidate_tests<<",\n  \"graphs_with_candidates\": "<<st.graphs_with_candidates<<",\n  \"final_markings\": "<<st.final_markings<<",\n  \"literal_checked\": "<<st.literal_checked<<",\n  \"literal_mismatch\": "<<st.literal_mismatch<<",\n  \"counterexamples\": "<<st.counterexamples<<",\n  \"cycles_seen_by_length\": {";
 bool first=true;for(int L=3;L<=16;++L)if(st.cycles_seen[L]){if(!first)cout<<",";first=false;cout<<"\n    \""<<L<<"\": "<<st.cycles_seen[L];}if(!first)cout<<'\n';cout<<"  },\n  \"seconds\": "<<fixed<<setprecision(6)<<sec<<"\n}\n";
 return st.literal_mismatch?3:0;
}
