import networkx as nx
from itertools import combinations
import sys,time
sys.path.insert(0,'/mnt/data/eg_run7_work')
from bounds_audit import masks,no_4cycle,has_8cycle,grow,graph_from_masks
start=time.time();c8=0;c9=0;ext10=0;rep=[];first=None
for h in nx.graph_atlas_g():
    if len(h)!=7 or max(nx.core_number(h).values())>2:continue
    a=masks(h)
    if not no_4cycle(a):continue
    for j in range(3):
        for sub in combinations(range(7),j):
            b=grow(a,sub)
            if not no_4cycle(b) or has_8cycle(b):continue
            m8=sum(x.bit_count() for x in b)//2
            if m8<10:continue
            c8+=1
            for k in range(3):
                for neigh in combinations(range(8),k):
                    if m8+k!=12:continue
                    c=grow(b,neigh)
                    if not no_4cycle(c) or has_8cycle(c):continue
                    c9+=1
                    if not any(nx.is_isomorphic(graph_from_masks(c),K) for K in rep):
                        rep.append(graph_from_masks(c))
                    for u,v in combinations(range(9),2):
                        d=grow(c,(u,v))
                        if no_4cycle(d) and not has_8cycle(d):
                            ext10+=1
                            if first is None:first=d
                            break
print('time',time.time()-start,'n8 m>=10',c8,'n9 m12 candidates',c9,'n9 m12 iso',len(rep),'n9 m12 extension cases',ext10)
if first:
 H=graph_from_masks(first)
 print('example n10 m',H.number_of_edges(),'g6',nx.to_graph6_bytes(H,header=False).decode().strip())
