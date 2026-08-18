#include <bits/stdc++.h>
using namespace std;
static const int N=40;
uint64_t adjm[N], unmatched_mask, ALL;
long long nodes=0, leaves=0;
int solmate[N];
chrono::steady_clock::time_point startt;
double limitsec=300; int fixedOnly=-1;
vector<int> parts, cycStart, cycId, cycPos;
int T; vector<int> oddMasks, crossCnt, remC; vector<vector<vector<int>>> cutMasks;

void enum_paths_rec(int cur,int rem,uint64_t vis,int forbidden, vector<pair<int,uint64_t>>&out){
    if(rem==0){out.push_back({cur,vis});return;}
    uint64_t cand=adjm[cur]&~vis;
    if(forbidden>=0) cand&=~(1ULL<<forbidden);
    while(cand){
        int w=__builtin_ctzll(cand); cand&=cand-1;
        enum_paths_rec(w,rem-1,vis|(1ULL<<w),forbidden,out);
    }
}

bool path_exact_rec(int cur,int target,int rem,uint64_t vis){
    if(rem==0) return cur==target;
    if(cur==target) return false;
    uint64_t cand=adjm[cur]&~vis;
    while(cand){
        int w=__builtin_ctzll(cand); cand&=cand-1;
        if(rem==1 && w!=target) continue;
        if(rem>1 && w==target) continue;
        if(path_exact_rec(w,target,rem-1,vis|(1ULL<<w))) return true;
    }
    return false;
}

bool path_exact_mitm(int s,int t,int L){
    if(L<=5) return path_exact_rec(s,t,L,1ULL<<s);
    int a=L/2, b=L-a;
    vector<pair<int,uint64_t>> A,B;
    A.reserve(1<<(a+2)); B.reserve(1<<(b+2));
    enum_paths_rec(s,a,1ULL<<s,t,A);
    enum_paths_rec(t,b,1ULL<<t,s,B);
    array<vector<uint64_t>,N> ga,gb;
    for(auto [x,m]:A) ga[x].push_back(m);
    for(auto [x,m]:B) gb[x].push_back(m);
    for(int x=0;x<N;x++) if(!ga[x].empty()&&!gb[x].empty()){
        uint64_t only=1ULL<<x;
        for(uint64_t p:ga[x]) for(uint64_t q:gb[x])
            if((p&q)==only) return true;
    }
    return false;
}

bool creates_forbidden(int u,int v){
    uint64_t vis=1ULL<<u;
    for(int L: {3,7,15}) if(path_exact_rec(u,v,L,1ULL<<u)) return true;
    return false;
}

bool connected(){
    uint64_t seen=1, frontier=1;
    while(frontier){
        int u=__builtin_ctzll(frontier); frontier&=frontier-1;
        uint64_t add=adjm[u]&~seen;
        seen|=add; frontier|=add;
    }
    return seen==ALL;
}

bool has_cycle_32(){
    // For each edge uv, search for a simple u-v path of length 31 after suppressing uv.
    for(int u=0;u<N;u++){
        uint64_t nbrs=adjm[u];
        while(nbrs){
            int v=__builtin_ctzll(nbrs); nbrs&=nbrs-1;
            if(v<=u) continue;
            adjm[u]&=~(1ULL<<v); adjm[v]&=~(1ULL<<u);
            bool found=path_exact_rec(u,v,31,1ULL<<u);
            adjm[u]|=1ULL<<v; adjm[v]|=1ULL<<u;
            if(found) return true;
        }
    }
    return false;
}

bool oddcut_feasible(){
    int totalRem=__builtin_popcountll(unmatched_mask);
    for(int mask:oddMasks){
        int rs=0;
        for(int c=0;c<T;c++) if(mask&(1<<c)) rs+=remC[c];
        if(crossCnt[mask]+min(rs,totalRem-rs)<5) return false;
    }
    return true;
}
void update_cross(int ca,int cb,int delta){
    if(ca==cb) return;
    for(int mask:cutMasks[ca][cb]) crossCnt[mask]+=delta;
}
vector<int> valid_candidates(int u){
    vector<int> out;
    uint64_t cand=unmatched_mask & ~(1ULL<<u) & ~adjm[u];
    while(cand){int v=__builtin_ctzll(cand);cand&=cand-1;
        if(!creates_forbidden(u,v)) out.push_back(v);
    }
    return out;
}

int heuristic_dist(int u,int v){
    if(cycId[u]!=cycId[v]) return 100;
    int m=parts[cycId[u]], d=abs(cycPos[u]-cycPos[v]);
    return min(d,m-d);
}

bool dfs(){
    nodes++;
    if(!oddcut_feasible()) return false;
    if((nodes&((1<<20)-1))==0){
        double t=chrono::duration<double>(chrono::steady_clock::now()-startt).count();
        cerr<<"progress nodes="<<nodes<<" rem="<<__builtin_popcountll(unmatched_mask)<<" t="<<t<<"\n";
        if(t>limitsec) throw runtime_error("TIME");
    }
    if(!unmatched_mask){
        leaves++;
        if(!connected()) return false;
        if(has_cycle_32()) return false;
        cout<<"FOUND parts"; for(int x:parts) cout<<" "<<x; cout<<"\n";
        for(int i=0;i<N;i++) if(i<solmate[i]) cout<<i<<" "<<solmate[i]<<"\n";
        return true;
    }
    int bestu=-1, bestcnt=INT_MAX; vector<int> best;
    uint64_t um=unmatched_mask;
    while(um){int x=__builtin_ctzll(um);um&=um-1;
        auto vc=valid_candidates(x); int cnt=vc.size();
        if(cnt<bestcnt){bestcnt=cnt;bestu=x;best.swap(vc);if(cnt<=1)break;}
    }
    int u=bestu; if(best.empty()) return false;
    sort(best.begin(),best.end(),[&](int a,int b){return heuristic_dist(u,a)>heuristic_dist(u,b);});
    unmatched_mask&=~(1ULL<<u);
    for(int v:best){
        if(!(unmatched_mask&(1ULL<<v))) continue;
        unmatched_mask&=~(1ULL<<v);
        remC[cycId[u]]--; remC[cycId[v]]--; update_cross(cycId[u],cycId[v],+1);
        adjm[u]|=1ULL<<v;adjm[v]|=1ULL<<u;solmate[u]=v;solmate[v]=u;
        if(dfs()) return true;
        adjm[u]&=~(1ULL<<v);adjm[v]&=~(1ULL<<u);solmate[u]=solmate[v]=-1;
        update_cross(cycId[u],cycId[v],-1); remC[cycId[u]]++; remC[cycId[v]]++;
        unmatched_mask|=1ULL<<v;
    }
    unmatched_mask|=1ULL<<u;
    return false;
}

void init_factor(){
    ALL=(1ULL<<N)-1;
    fill(adjm,adjm+N,0);fill(solmate,solmate+N,-1);
    cycStart.clear();cycId.assign(N,-1);cycPos.assign(N,-1);
    int s=0;
    for(int c=0;c<(int)parts.size();c++){
        int m=parts[c];cycStart.push_back(s);
        for(int p=0;p<m;p++){
            int u=s+p, v=s+(p+1)%m;
            adjm[u]|=1ULL<<v;adjm[v]|=1ULL<<u;
            cycId[u]=c;cycPos[u]=p;
        }
        s+=m;
    }
    unmatched_mask=ALL;
    T=parts.size(); remC=parts; oddMasks.clear(); crossCnt.assign(1<<T,0);
    for(int mask=1;mask<(1<<T)-1;mask++){
        if(!(mask&1)) continue;
        int sd=0; for(int c=0;c<T;c++) if(mask&(1<<c)) sd+=parts[c];
        if(sd&1) oddMasks.push_back(mask);
    }
    cutMasks.assign(T,vector<vector<int>>(T));
    for(int a=0;a<T;a++) for(int b=0;b<T;b++) if(a!=b)
        for(int mask:oddMasks) if(((mask>>a)&1)!=((mask>>b)&1)) cutMasks[a][b].push_back(mask);
}

vector<int> partner_orbit_reps(){
    vector<int> reps;
    int a=parts[0];
    for(int d=2;d<=a/2;d++) reps.push_back(d);
    set<int> seenLengths;
    for(int c=1;c<(int)parts.size();c++) if(seenLengths.insert(parts[c]).second) reps.push_back(cycStart[c]);
    return reps;
}

int main(int argc,char**argv){
    if(argc<2){cerr<<"usage: factor40 part1 [part2 ...] [--limit=S]\n";return 2;}
    for(int i=1;i<argc;i++){
        string s=argv[i];
        if(s.rfind("--limit=",0)==0) limitsec=stod(s.substr(8)); else if(s.rfind("--fixed=",0)==0) fixedOnly=stoi(s.substr(8)); else parts.push_back(stoi(s));
    }
    sort(parts.begin(),parts.end());
    if(accumulate(parts.begin(),parts.end(),0)!=N){cerr<<"parts must sum 38\n";return 2;}
    for(int x:parts) if(x<5||x==8||x==16||x==32){cerr<<"invalid/settled factor part "<<x<<"\n";return 2;}
    auto reps=[&](){init_factor();return partner_orbit_reps();}();
    long long totalNodes=0,totalLeaves=0; bool anyFound=false;
    for(int j:reps){
        if(fixedOnly>=0 && j!=fixedOnly) continue;
        init_factor();nodes=leaves=0;
        if(adjm[0]&(1ULL<<j)) continue;
        if(creates_forbidden(0,j)){cerr<<"SKIP fixed="<<j<<" immediate forbidden\n";continue;}
        adjm[0]|=1ULL<<j;adjm[j]|=1ULL;solmate[0]=j;solmate[j]=0;
        unmatched_mask&=~(1ULL|(1ULL<<j));
        remC[cycId[0]]--; remC[cycId[j]]--; update_cross(cycId[0],cycId[j],+1);
        startt=chrono::steady_clock::now();
        try{
            bool f=dfs();
            double t=chrono::duration<double>(chrono::steady_clock::now()-startt).count();
            cerr<<"DONE fixed="<<j<<" found="<<f<<" nodes="<<nodes<<" leaves="<<leaves<<" t="<<t<<"\n";
            totalNodes+=nodes;totalLeaves+=leaves;anyFound|=f;
            if(f) break;
        }catch(exception&e){
            double t=chrono::duration<double>(chrono::steady_clock::now()-startt).count();
            cerr<<"TIME fixed="<<j<<" nodes="<<nodes<<" leaves="<<leaves<<" t="<<t<<"\n";
            return 3;
        }
    }
    cerr<<"SUMMARY parts=";for(int x:parts)cerr<<x<<",";cerr<<" found="<<anyFound<<" nodes="<<totalNodes<<" leaves="<<totalLeaves<<"\n";
    return anyFound?1:0;
}
