#include <bits/stdc++.h>
using namespace std;
int T; vector<int>D,loopsv,resid; int M[8][8]; vector<int> oddMasks;
vector<vector<int>> allOrders; unordered_set<string> seen; vector<vector<int>> reps;
long long raw=0;

bool connectedQ(){
 vector<int> vis(T);queue<int>q;vis[0]=1;q.push(0);
 while(!q.empty()){int a=q.front();q.pop();for(int b=0;b<T;b++)if(a!=b&&M[a][b]>0&&!vis[b])vis[b]=1,q.push(b);}
 return accumulate(vis.begin(),vis.end(),0)==T;
}
bool cutsok(){
 for(int mask:oddMasks){int c=0;for(int i=0;i<T;i++)for(int j=i+1;j<T;j++)if(((mask>>i)&1)!=((mask>>j)&1))c+=M[i][j];if(c<5)return false;}return true;
}
string encodeOrder(const vector<int>&o){
 string s; s.reserve(T*(T+1)/2);
 for(int k=0;k<T;k++)s.push_back(char(loopsv[o[k]]));
 for(int i=0;i<T;i++)for(int j=i+1;j<T;j++)s.push_back(char(M[o[i]][o[j]]));
 return s;
}
vector<vector<int>> refinedOrders(){
 vector<int> col(T); // canonical initial colors from degree and loop count
 vector<pair<int,int>> init(T);
 for(int i=0;i<T;i++)init[i]={D[i],loopsv[i]};
 {auto z=init;sort(z.begin(),z.end());z.erase(unique(z.begin(),z.end()),z.end());for(int i=0;i<T;i++)col[i]=lower_bound(z.begin(),z.end(),init[i])-z.begin();}
 while(true){
  vector<string> sig(T);
  for(int i=0;i<T;i++){
   vector<pair<int,int>> a;for(int j=0;j<T;j++)if(i!=j)a.push_back({col[j],M[i][j]});sort(a.begin(),a.end());
   string q=to_string(col[i])+":";for(auto [c,m]:a)q+=to_string(c)+","+to_string(m)+";";sig[i]=q;
  }
  auto z=sig;sort(z.begin(),z.end());z.erase(unique(z.begin(),z.end()),z.end());vector<int> nc(T);for(int i=0;i<T;i++)nc[i]=lower_bound(z.begin(),z.end(),sig[i])-z.begin();
  if(nc==col)break;col=nc;
 }
 map<int,vector<int>> groups;for(int i=0;i<T;i++)groups[col[i]].push_back(i);
 vector<vector<vector<int>>> perms;for(auto &kv:groups){vector<vector<int>> pp;auto g=kv.second;sort(g.begin(),g.end());do{pp.push_back(g);}while(next_permutation(g.begin(),g.end()));perms.push_back(move(pp));}
 vector<vector<int>> out(1);for(auto &pp:perms){vector<vector<int>> nx;for(auto &pre:out)for(auto &p:pp){auto z=pre;z.insert(z.end(),p.begin(),p.end());nx.push_back(move(z));}out.swap(nx);}return out;
}
void accept(){
 if(!connectedQ()||!cutsok())return;raw++;
 string best;bool first=true;
 auto orders=refinedOrders();
 for(auto&o:orders){string s=encodeOrder(o);if(first||s<best)best=s,first=false;}
 if(seen.insert(best).second){
  vector<int>v;for(int i=0;i<T;i++)for(int j=i;j<T;j++)v.push_back(i==j?loopsv[i]:M[i][j]);reps.push_back(move(v));
 }
}
void enumEdges(){
 int i=-1;for(int k=0;k<T;k++)if(resid[k]){i=k;break;}if(i<0){accept();return;}
 vector<int>js;for(int j=i+1;j<T;j++)js.push_back(j);int need=resid[i];
 function<void(int,int)>dist=[&](int k,int left){
  if(k==(int)js.size()){
   if(left==0){int old=resid[i];resid[i]=0;enumEdges();resid[i]=old;}return;
  }
  int j=js[k],mx=min(left,resid[j]);
  for(int x=0;x<=mx;x++){M[i][j]=M[j][i]=x;resid[j]-=x;dist(k+1,left-x);resid[j]+=x;}M[i][j]=M[j][i]=0;
 };
 dist(0,need);
}
void enumLoops(int i){
 if(i==T){enumEdges();return;}
 for(int l=0;l<=D[i]/2;l++){loopsv[i]=l;resid[i]=D[i]-2*l;enumLoops(i+1);} }

int main(int argc,char**argv){
 for(int i=1;i<argc;i++)D.push_back(stoi(argv[i]));sort(D.begin(),D.end());T=D.size();if(accumulate(D.begin(),D.end(),0)!=38)return 2;
 loopsv.resize(T);resid.resize(T);memset(M,0,sizeof(M));
 for(int mask=1;mask<(1<<T)-1;mask++)if(mask&1){int sd=0;for(int i=0;i<T;i++)if(mask>>i&1)sd+=D[i];if(sd&1)oddMasks.push_back(mask);}
 // all permutations preserving degree sequence positions
 vector<int>ord(T);iota(ord.begin(),ord.end(),0);
 do{bool ok=true;for(int k=0;k<T;k++)if(D[ord[k]]!=D[k]){ok=false;break;}if(ok)allOrders.push_back(ord);}while(next_permutation(ord.begin(),ord.end()));
 auto st=chrono::steady_clock::now();enumLoops(0);
 string name=string(getenv("OUT_DIR")?getenv("OUT_DIR"):".")+"/skel";for(int x:D)name+="_"+to_string(x);name+=".txt";ofstream out(name);out<<T;for(int x:D)out<<" "<<x;out<<"\n";for(auto&v:reps){for(int i=0;i<(int)v.size();i++)out<<(i?" ":"")<<v[i];out<<"\n";}
 cerr<<name<<" raw="<<raw<<" canonical="<<reps.size()<<" orders="<<allOrders.size()<<" sec="<<chrono::duration<double>(chrono::steady_clock::now()-st).count()<<"\n";
}
