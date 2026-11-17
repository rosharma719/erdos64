"""Additional independent falsification attempts, not an exhaustive graph census."""
import networkx as nx,random
from collections import Counter

def cycle_edge_coverage(G):
    E={frozenset((u,v)) for u,v in G.edges()}
    covered=set()
    short=set()
    for cyc in nx.simple_cycles(nx.to_directed(G), length_bound=8):
        k=len(cyc)
        if k in (4,8): short.add(k)
        if k not in (3,5): continue
        covered.update(frozenset((cyc[i],cyc[(i+1)%k])) for i in range(k))
    return covered==E,short

# All cubic atlas graphs of order 4, 6 (and also all <= 7)
num=0
for G in nx.graph_atlas_g():
    if G.number_of_nodes()<4 or not all(d==3 for _,d in G.degree()):continue
    num+=1
    covered,short=cycle_edge_coverage(G)
    assert not covered or short, ('cubic atlas counterexample', nx.to_graph6_bytes(G))
print('All cubic graphs in NetworkX atlas (n<=7):',num,'checked')

p=nx.petersen_graph()
for name,G in [('Petersen',p),('dodecahedron',nx.dodecahedral_graph()),('triangular_prism',nx.circular_ladder_graph(3))]:
    covered,short=cycle_edge_coverage(G)
    print(name,'n',len(G),'all edges C3/C5-covered?',covered,'C4/C8 present',sorted(short))
    assert covered and short

rng=random.Random(14005)
count=0; covered_samples=0
for n in (10,12,14,16,18,20):
    for r in range(30):
        G=nx.random_regular_graph(3,n,seed=rng.randrange(2**30))
        covered,short=cycle_edge_coverage(G)
        assert not covered or short, ('random counterexample',n,r)
        count+=1;covered_samples+=covered
print('Random cubic samples:',count,'covered samples:',covered_samples,'all pass')
