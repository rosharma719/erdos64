"""Independent graph-level checks of the arbitrary-cut composition theorem."""
from itertools import combinations
from pathlib import Path
import importlib.util
import random
import networkx as nx

spec = importlib.util.spec_from_file_location(
    'boundary_linkage', Path(__file__).with_name('boundary_linkage.py'))
bl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bl)


def all_cycles(graph, forbidden=()):
    H = graph.subgraph(set(graph) - set(forbidden))
    return [frozenset(zip(cycle, cycle[1:] + cycle[:1])) for cycle in nx.simple_cycles(H)]


def oracle_crossing_lengths(graph, side, forbidden=()):
    A = set(side)
    B = set(graph) - A
    return {len(c) for c in nx.simple_cycles(graph.subgraph(set(graph) - set(forbidden)))
            if set(c) & A and set(c) & B}


def test_four_edge_cube():
    G = nx.cubical_graph()
    # The top/bottom square shore partition: 4 vertical cut edges.
    square = next(c for c in nx.simple_cycles(G) if len(c)==4)
    A = set(square)
    assert len(list(nx.edge_boundary(G, A))) == 4
    predicted, states = bl.crossing_cycle_lengths(G, A)
    assert predicted == oracle_crossing_lengths(G, A)
    for root in G:
        assert bl.crossing_cycle_lengths(G, A, root=root)[0] == oracle_crossing_lengths(G, A, (root,))
    assert any(len(k[0]) == 4 for k in states)


def test_four_crossings_are_essential():
    # Shore A: path 0--1--2--3. Shore B: path 0--3--1--2.
    # All four matching cut edges 0--0', 1--1', ... are present.
    G = nx.Graph()
    G.add_edges_from([(0,1),(1,2),(2,3)])
    G.add_edges_from([('b0','b3'),('b3','b1'),('b1','b2')])
    G.add_edges_from((i,'b'+str(i)) for i in range(4))
    A = set(range(4))
    predicted, states = bl.crossing_cycle_lengths(G,A)
    assert 8 in predicted
    assert 8 not in {length for (used,_,_),lens in states.items() if len(used)==2 for length in lens}
    assert 8 in {length for (used,_,_),lens in states.items() if len(used)==4 for length in lens}
    assert predicted == oracle_crossing_lengths(G,A)


def test_matching_cut_reconstruction_random():
    rng = random.Random(20261116)
    for n in (8,10,12):
        for _ in range(14):
            G=nx.random_regular_graph(3,n,seed=rng.randrange(10**9))
            # Partition until finding a matching cut, otherwise skip.
            for _ in range(160):
                A=set(rng.sample(list(G.nodes),rng.randrange(3,n-2)))
                cut=list(nx.edge_boundary(G,A))
                if 2<=len(cut)<=5 and len(set(u for u,v in cut))==len(cut) and len(set(v for u,v in cut))==len(cut):
                    break
            else:
                continue
            predicted, states = bl.crossing_cycle_lengths(G,A)
            actual=oracle_crossing_lengths(G,A)
            assert predicted==actual,(n,G,A,predicted,actual)
            for root in rng.sample(list(G.nodes),2):
                pred,_=bl.crossing_cycle_lengths(G,A,root=root)
                actual=oracle_crossing_lengths(G,A,(root,))
                assert pred==actual,(n,G,A,root,pred,actual)


def test_density_witness_and_sharpness():
    result=bl.dyadic_density_certificate({1,2,4},{2,3,5},shift=2,exponent=3,lo=1,hi=4)
    assert result['certified'] and result['witness'][0]+result['witness'][1]+2==8
    # A={1}, B={0,1,2} on a 4-slot reflected window: equality is not enough.
    equality=bl.dyadic_density_certificate({1},{0,1,2},shift=2,exponent=3,lo=1,hi=4)
    assert not equality['certified'] and equality['witness'] is None


def test_matchings_and_gluing():
    for count, number in [(2,1),(4,3),(6,15)]:
        matching=list(bl.perfect_matchings(range(count)))
        assert len(matching)==number
        for ma in matching:
            for mb in matching:
                if count==2:
                    assert bl.alternating_connected(ma,mb)
                elif ma==mb:
                    assert not bl.alternating_connected(ma,mb)


def test_general_cuts_with_repeated_boundary_vertices():
    # A=two adjacent branches of a bridged K4; cut edges can share endpoints.
    G = nx.complete_graph(4)
    u, v = 4, 5
    G.remove_edges_from([(0,1),(2,3)])
    G.add_edges_from([(0,u),(1,u),(2,v),(3,v),(u,v)])
    # Multiple cut edges meet the vertices 4 and 5.
    A = {4, 5}
    predicted, _ = bl.crossing_cycle_lengths(G, A)
    assert predicted == oracle_crossing_lengths(G, A)
    for root in G:
        pred, _ = bl.crossing_cycle_lengths(G,A,root=root)
        assert pred == oracle_crossing_lengths(G,A,(root,))


def test_arbitrary_shores_random():
    rng = random.Random(314159)
    for n in (8,10):
        for _ in range(20):
            G = nx.random_regular_graph(3, n, seed=rng.randrange(10**9))
            A = set(rng.sample(list(G),rng.randrange(2,n-1)))
            # With arbitrary cuts, the cut width can exceed four; keep
            # the exact oracle economical by selecting width <= 6.
            if len(list(nx.edge_boundary(G,A))) > 6:
                continue
            prediction,_=bl.crossing_cycle_lengths(G,A)
            assert prediction == oracle_crossing_lengths(G,A)


def test_context_independent_composition_cube():
    G=nx.cubical_graph()
    square = next(c for c in nx.simple_cycles(G) if len(c)==4)
    A=set(square)
    cut=sorted((u,v) if u in A else (v,u)
               for u,v in G.edges() if (u in A)!=(v in A))
    B=set(G)-A
    SA=bl.boundary_signature(G.subgraph(A),[u for u,v in cut])
    SB=bl.boundary_signature(G.subgraph(B),[v for u,v in cut])
    assert bl.compose_signatures(SA,SB)==frozenset(map(len,nx.simple_cycles(G)))
    for root in G:
        if root in A:
            SAroot=bl.boundary_signature(G.subgraph(A),[u for u,v in cut],forbidden=(root,))
            SBroot=SB
        else:
            SAroot=SA
            SBroot=bl.boundary_signature(G.subgraph(B),[v for u,v in cut],forbidden=(root,))
        oracle=frozenset(map(len,nx.simple_cycles(G.subgraph(set(G)-{root}))))
        assert bl.compose_signatures(SAroot,SBroot)==oracle


def test_bridge_is_four_port_composition_including_new_roots():
    parent=nx.complete_graph(4)
    A=parent.copy()
    A.remove_edges_from([(0,1),(2,3)])
    B=nx.Graph()
    B.add_edge('x','y')
    ports_A=[0,1,2,3]
    ports_B=['x','x','y','y']
    joined=bl.glue_poles(A,ports_A,B,ports_B)
    sigA=bl.boundary_signature(A,ports_A)
    sigB=bl.boundary_signature(B,ports_B)
    assert bl.compose_signatures(sigA,sigB)==frozenset(map(len,nx.simple_cycles(joined)))
    # The bridged graph contains both new roots, here 4 and 5.
    # Node mapping left is 0..3, right is 4,5 in B's enumeration.
    for root in list(A.nodes())+list(B.nodes()):
        if root in A:
            SAroot=bl.boundary_signature(A,ports_A,forbidden=(root,))
            SBroot=sigB
            actual_root=list(A.nodes()).index(root)
        else:
            SAroot=sigA
            SBroot=bl.boundary_signature(B,ports_B,forbidden=(root,))
            actual_root=len(A)+list(B.nodes()).index(root)
        expected=frozenset(map(len,nx.simple_cycles(joined.subgraph(set(joined)-{actual_root}))))
        assert bl.compose_signatures(SAroot,SBroot)==expected


def test_composition_random_even_with_repeated_ports():
    rng=random.Random(1730)
    for _ in range(35):
        na, nb = rng.randrange(2,6),rng.randrange(2,6)
        A=nx.gnp_random_graph(na,0.37,seed=rng.randrange(10**6))
        B=nx.gnp_random_graph(nb,0.37,seed=rng.randrange(10**6))
        h=rng.randrange(2,6)
        pa=[rng.choice(list(A.nodes())) for _ in range(h)]
        pb=[rng.choice(list(B.nodes())) for _ in range(h)]
        if len(set(zip(pa,pb)))<h:
            continue  # Avoid parallel gluing edges in simple graph
        G=bl.glue_poles(A,pa,B,pb)
        predicted=bl.compose_signatures(bl.boundary_signature(A,pa),bl.boundary_signature(B,pb))
        oracle=frozenset(map(len,nx.simple_cycles(G)))
        assert predicted==oracle,(A.edges(),B.edges(),pa,pb,predicted,oracle)


def theta_pole(lengths):
    H = nx.Graph()
    H.add_nodes_from(['s','t'])
    for path_index, length in enumerate(lengths):
        path=['s']+[(path_index,i) for i in range(1,length)]+['t']
        H.add_edges_from(zip(path,path[1:]))
    return H


def test_equal_endpoint_windows_but_different_dyadic_cycles():
    # Both poles have minimum s--t path length 2 and maximum 7.
    # The extra length 3 in the second pole is structurally decisive.
    A1=theta_pole([2,7])
    A2=theta_pole([2,3,7])
    B=nx.path_graph(4)  # path of length 3
    s1=bl.boundary_signature(A1,['s','t'])
    s2=bl.boundary_signature(A2,['s','t'])
    sb=bl.boundary_signature(B,[0,3])
    assert min(s1['linkages'][((0,1),((0,1),))])==2
    assert max(s1['linkages'][((0,1),((0,1),))])==7
    assert min(s2['linkages'][((0,1),((0,1),))])==2
    assert max(s2['linkages'][((0,1),((0,1),))])==7
    cycles1=bl.compose_signatures(s1,sb)
    cycles2=bl.compose_signatures(s2,sb)
    assert 8 not in cycles1
    assert 8 in cycles2
    assert not ({4,8,16,32} & cycles1)
    assert {4,8,16,32} & cycles2 == {8}


def test_parity_aware_additive_density():
    A={2,4,8}
    B={2,4,6}
    cert=bl.reflected_density_certificate(A,B,shift=4,exponent=4,window={4,6,8})
    assert cert['certified']
    assert cert['witness'][0] + cert['witness'][1] + 4 == 16


def test_density_implication_random():
    rng=random.Random(1713)
    for _ in range(500):
        A=set(rng.sample(range(2,20),rng.randrange(1,10)))
        B=set(rng.sample(range(2,20),rng.randrange(1,10)))
        W=set(rng.sample(range(2,20),rng.randrange(1,10)))
        q=2**rng.choice((3,4,5))
        shift=rng.randrange(2,9)
        cert=bl.reflected_density_certificate(A,B,shift, int(q.bit_length()-1),W)
        if cert['certified']:
            assert q in {shift+a+b for a in A for b in B}
