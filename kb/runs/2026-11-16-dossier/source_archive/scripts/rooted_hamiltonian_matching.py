"""Exact rooted Hamiltonian cubic census for even orders <= 16.

Fix Hamilton cycle C=(0,1,...,n-1) and root=0. The remaining edges form
one perfect matching disjoint from C. If G-0 has no dyadic cycle, each
matching chord i-j with 1<=i<j must avoid distances 2**k-1 (a root-free
cycle of length 2**k arises from that chord and C[i:j+1]).

Enumerate these constrained matchings and independently check C4/C8 in
G-0. At n<=16 there are no other possible root-avoiding dyadic lengths.
This covers every Hamiltonian cubic graph with a chosen root (label C).
No assertion is made for non-Hamiltonian graphs or larger orders.
"""
from collections import Counter
from time import perf_counter
import sys


def has_four(adj,n):
 for a in range(1,n):
  for b in range(a+1,n):
   if (adj[a]&adj[b]).bit_count()>=2:
    return True
 return False

def has_eight(adj,n):
 for s in range(1,n):
  def dfs(u,used,dep):
   if dep==8:return (adj[u]>>s)&1
   avail=adj[u]&~used&~((1<<(s+1))-1)
   while avail:
    bit=avail&-avail;avail-=bit
    if dfs(bit.bit_length()-1, used|bit, dep+1):return True
   return False
  if dfs(s,1<<s,1):return True
 return False

def census(n):
 if n%2 or n<4 or n>16:
  raise ValueError("implemented and verified for even orders 4..16")
 matched=[-1]*n; count=Counter(); survivors=[]
 def recurse(remaining):
  if not remaining:
   count['admissible']+=1
   adj=[0]*n
   for i in range(1,n):
    for j in ((i+1)%n,(i+n-1)%n,matched[i]):
     if j:adj[i]|=1<<j
   if has_four(adj,n):count['C4']+=1;return
   if has_eight(adj,n):count['C8']+=1;return
   count['survive']+=1
   survivors.append(tuple((i,matched[i]) for i in range(n) if i<matched[i]))
   return
  i=(remaining&-remaining).bit_length()-1
  remaining^=1<<i
  bits=remaining
  while bits:
   j=(bits&-bits).bit_length()-1
   bits &=bits-1
   distance=j-i
   if distance in (1,n-1) or (i!=0 and (distance+1).bit_count()==1 and distance+1>=4):
    continue
   matched[i]=j;matched[j]=i
   recurse(remaining^(1<<j))
   matched[i]=matched[j]=-1
 recurse((1<<n)-1)
 return count,survivors

if __name__=='__main__':
 n=int(sys.argv[1]);t=perf_counter();stats,survivors=census(n)
 print('n',n,'stats',stats,'time',round(perf_counter()-t,2),flush=True)
 print('survivors',survivors[:30])
