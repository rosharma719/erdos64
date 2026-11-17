"""Standalone LP verifier for rho and the exact symmetry bound on small graphs.
Requires networkx, scipy; uses exact exhaustive cycle enumeration in edge_transversals.
"""
import networkx as nx
import numpy as np
from scipy.optimize import linprog
from edge_transversals import dyadic_masks,strings

def rho(G):
 E,C=dyadic_masks(G);n=len(G);m=len(E);N=len(C)
 if not N:return 0,None,0
 q=min(vbits.bit_count() for vbits,_ in C)
 mat=[];rhs=[]
 for j in range(m):mat.append([1 if (ebits>>j)&1 else 0 for vb,ebits in C]+[0]);rhs.append(1)
 for v in range(n):mat.append([1 if (vbits>>v)&1 else 0 for vbits,ebits in C]+[-1]);rhs.append(0)
 sol=linprog([-1]*N+[1], A_ub=np.asarray(mat,dtype=float), b_ub=rhs,bounds=[(0,None)]*(N+1),method='highs')
 if not sol.success:raise RuntimeError(sol.message)
 return -sol.fun/2,q,N

def test():
 samples=[('K4',nx.complete_graph(4)),('cube',nx.cubical_graph()),('Petersen',nx.petersen_graph()),('K3,3',nx.complete_bipartite_graph(3,3)),('Heawood',nx.heawood_graph()),('dodecahedron',nx.dodecahedral_graph())]
 for k,g in enumerate(map(lambda s:nx.from_graph6_bytes(s.encode()),strings)):samples.append((f'24near{k+1}',g))
 for name,g in samples:
  v,q,N=rho(g);ub=len(g.edges())*(len(g)-q)/(2*len(g)*q)
  assert v<=ub+1e-7
  if name in ('K4','cube','Petersen','K3,3','Heawood','dodecahedron'):
   assert abs(v-ub)<1e-7
  print(f'{name:14} n={len(g):2} q={q:2} cycles={N:4} rho={v:.7g} upper={ub:.7g}')
if __name__=='__main__':test()
