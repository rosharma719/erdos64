"""Independent bitmask enumerator and exact transversal certificate."""
import networkx as nx,itertools,json
G=nx.from_graph6_bytes(open('coxeter.g6','rb').read().strip())
N=len(G)
assert N==28 and all(d==3 for _,d in G.degree())
# Enumerate cycles with undirected edge-walk DFS, normalize by smallest vertex and orientation.
cy=set()
for start in range(N):
 stack=[(start,[start],1<<start)]
 while stack:
  v,p,used=stack.pop()
  if len(p)==8:
   if start in G[v] and p[1]<p[-1]:cy.add(sum(1<<a for a in p))
   continue
  for w in G[v]:
   if w>start and not (used>>w)&1:stack.append((w,p+[w],used|(1<<w)))
assert len(cy)==21,len(cy)
# A set S hits all C8 iff for every C8 bitmask c, S & c != 0.
for k in range(1,6):
 for S in itertools.combinations(range(N),k):
  mask=sum(1<<v for v in S)
  assert any(mask & c == 0 for c in cy),(k,S)
witness=(0,1,3,6,9,14)
assert all(sum(1<<v for v in witness)&c for c in cy)
print('PASS: 21 C8, transversal number exactly 6; witness',witness)
