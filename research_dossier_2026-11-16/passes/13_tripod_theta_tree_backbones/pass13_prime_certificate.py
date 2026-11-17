#!/usr/bin/env python3
"""Independent small certificate checker: triple-tree dyadic rank-two obstruction."""
import itertools, json, networkx as nx

def audit(label,g6,J,root,qcycle):
 G=nx.from_graph6_bytes(g6.encode());J=set(J)
 assert len(G)>8 and all(d==3 for _,d in G.degree())
 assert nx.node_connectivity(G)==3
 T=G.subgraph(set(G)-J).copy()
 assert nx.is_tree(T) and G.subgraph(J).number_of_edges()==0 and T.degree(root)==3
 # Verify all three-edge cuts are trivial, independently of the generator.
 nontriv=[];triv=0
 for edges in itertools.combinations(G.edges(),3):
  H=G.copy();H.remove_edges_from(edges)
  comp=list(nx.connected_components(H))
  if len(comp)>1:
   if min(map(len,comp))==1:triv+=1
   else:nontriv.append((edges,list(map(len,comp))))
 assert not nontriv
 Z=T.copy();Z.remove_node(root)
 branches=sorted(nx.connected_components(Z),key=min)
 assert len(branches)==3 and all(len(b)==len(J)-1 for b in branches)
 attach={j: [next(iter(set(G[j])&b)) for b in branches] for j in sorted(J)}
 assert all(len(set(G[j])&b)==1 for j in J for b in branches)
 distances=[];cycles2=[]
 for j,k in itertools.combinations(sorted(J),2):
  d=[nx.shortest_path_length(Z,attach[j][i],attach[k][i]) for i in range(3)]
  lens=[4+d[i]+d[h] for i,h in itertools.combinations(range(3),2)]
  distances.append({'pair':[j,k],'branch_distances':d,'two_connector_cycle_lengths':lens})
  cycles2.extend(lens)
 assert all(length not in [4,8] for length in cycles2)
 assert len(qcycle)==8 and len(set(qcycle))==8 and root not in qcycle
 assert len(J.intersection(qcycle))==3
 assert all(G.has_edge(qcycle[i],qcycle[(i+1)%8]) for i in range(8))
 result={'graph':label,'n':len(G),'graph6':g6,'node_connectivity':nx.node_connectivity(G),
         'trivial_three_cuts':triv,'nontrivial_three_cuts':len(nontriv),
         'root':root,'J':sorted(J),'branch_orders':list(map(len,branches)),
         'branch_attachments':attach,'metric_table':distances,
         'two_J_lengths':dict(sorted((int(x),cycles2.count(x)) for x in set(cycles2))),
         'explicit_root_avoiding_8cycle':qcycle}
 return result

if __name__=='__main__':
 p=audit('Petersen','IkE?ISqJ?',{7,8,9},0,[3,4,7,6,5,9,2,8])
 q=audit('Prime-14 rank-two barrier','MHEIGC@AM?AD_CGO_',{0,1,3,7},9,[0,5,6,1,2,3,11,10])
 print(json.dumps({'certificates':[p,q]},indent=2))
 with open('/mnt/data/eg-work/pass13_prime_certificates.json','w') as out:json.dump({'certificates':[p,q]},out,indent=2)
