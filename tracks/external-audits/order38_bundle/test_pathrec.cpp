// Standalone extraction of the path_exact_rec / has_cycle_L primitive shared by
// factor38_direct_mrv.cpp, quotient_static38_rot.cpp/nosym.cpp, filter_pair_local38.py
// (Python port) and filter_triple_local38.cpp, for independent cross-validation
// against the already-validated Python detector (verifier/cycle_detect.py).
#include <bits/stdc++.h>
using namespace std;
static int n;
static uint64_t adj[64];

static bool path_exact_rec(int cur,int target,int rem,uint64_t vis){
    if(rem==0) return cur==target;
    if(cur==target) return false;
    uint64_t cand=adj[cur]&~vis;
    while(cand){
        int w=__builtin_ctzll(cand); cand&=cand-1;
        if(rem==1 && w!=target) continue;
        if(rem>1 && w==target) continue;
        if(path_exact_rec(w,target,rem-1,vis|(1ULL<<w))) return true;
    }
    return false;
}

static bool has_cycle_len(int L){
    if(L<3||L>n) return false;
    for(int u=0;u<n;u++){
        uint64_t nbrs=adj[u];
        while(nbrs){
            int v=__builtin_ctzll(nbrs); nbrs&=nbrs-1;
            if(v<=u) continue;
            adj[u]&=~(1ULL<<v); adj[v]&=~(1ULL<<u);
            bool found=path_exact_rec(u,v,L-1,1ULL<<u);
            adj[u]|=1ULL<<v; adj[v]|=1ULL<<u;
            if(found) return true;
        }
    }
    return false;
}

int main(){
    // stdin format: repeated blocks:
    //   n
    //   n lines of adjacency (0/1, space separated) -- full matrix
    //   L
    // outputs: "L <0|1>" (has cycle of exact length L)
    while(cin>>n){
        for(int i=0;i<n;i++) adj[i]=0;
        for(int i=0;i<n;i++) for(int j=0;j<n;j++){
            int x; cin>>x;
            if(x) adj[i]|=(1ULL<<j);
        }
        int L; cin>>L;
        cout << L << " " << (has_cycle_len(L)?1:0) << "\n";
    }
}
