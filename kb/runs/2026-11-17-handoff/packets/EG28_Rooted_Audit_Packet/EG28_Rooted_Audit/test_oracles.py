"""Independent tests of MITM C16 and bounded DFS exact oracles."""
import random
import networkx as nx
from verify_g6 import find_c16_mitm, find_cycle_dfs, cycle_valid


def test_mitm_dfs():
    checks=0
    for n in (16,18,20,24):
        for k in range(4):
            G=nx.random_regular_graph(3,n,seed=31337 + 100*n+k)
            for root in (0,n//3,n-1,None):
                a=find_c16_mitm(G,avoiding=root)
                b=find_cycle_dfs(G,16,avoiding=root)
                assert (a is None)==(b is None),(n,k,root)
                if a is not None:
                    assert cycle_valid(G,a,16,root)
                if b is not None:
                    assert cycle_valid(G,b,16,root)
                checks+=1
    print('MITM-versus-DFS rooted tests passed:',checks)

if __name__=='__main__':
    test_mitm_dfs()
