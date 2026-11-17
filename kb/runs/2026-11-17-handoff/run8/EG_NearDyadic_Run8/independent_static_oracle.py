from itertools import combinations, permutations
import time, collections
N=9
base=set(tuple(sorted((i,(i+1)%9))) for i in range(9))

def check_static(seq,girth=False):
 adj=[set() for i in range(16)]
 for a,b in base:adj[a].add(b);adj[b].add(a)
 e2=[]
 for a,b in zip([1]+list(seq),list(seq)+[0]):
  if b in adj[a]:continue
  adj[a].add(b);adj[b].add(a);e2.append((a,b))
 if not e2 or max(len(x) for x in adj)>3:return False
 lens=(3,4,5,6,7,8,16) if girth else (4,8,16)
 # for every start s only allow other vertices >s, ensure oriented cycles duplicates irrelevant
 def search(s,u,used,level,L):
  if level==L:return s in adj[u]
  for w in adj[u]:
   if w>s and not (used>>w)&1:
    if search(s,w,used|1<<w,level+1,L):return True
  return False
 for L in lens:
  for s in range(16):
   if len(adj[s])<2:continue
   if search(s,s,1<<s,1,L):return False
 return True

if __name__=='__main__':
 t=time.time();c=0;gc=0;stats=collections.Counter()
 for r in range(8):
  for poss in combinations(range(7),r):
   posset=set(poss)
   for olds in permutations(range(2,9),r):
    it=iter(olds); seq=[]; new=9
    for pos in range(7):
     if pos in posset:seq.append(next(it))
     else: seq.append(new);new+=1
    x=check_static(seq,False)
    if x:
     c+=1; stats[r]+=1
     if check_static(seq,True):gc+=1
 print('count',c,'girth9',gc,'by shared',stats,'seconds',time.time()-t)
