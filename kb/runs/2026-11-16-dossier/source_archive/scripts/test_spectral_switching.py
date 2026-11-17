"""Independent small graph tests for the pass-XI structural deductions."""
from pathlib import Path
import importlib.util
import random
import networkx as nx

spec = importlib.util.spec_from_file_location('spectral_switching',Path(__file__).with_name('spectral_switching.py'))
ss = importlib.util.module_from_spec(spec); spec.loader.exec_module(ss)


def theta_pole(path_lengths):
    G = nx.Graph()
    s, t = 's','t'
    for num,length in enumerate(path_lengths):
        assert length>=2
        internal = [(num,j) for j in range(length-1)]
        path = [s]+internal+[t]
        G.add_edges_from(zip(path,path[1:]))
    return G, s, t


def add_context(G, s, t, m):
    G=G.copy()
    names = [('context', i) for i in range(m+1)]
    G.add_edges_from(zip(names,names[1:]))
    G.add_edge(s,names[0]); G.add_edge(t,names[-1])
    return G


def all_cycle_lengths(G):
    return {len(c) for c in nx.simple_cycles(G)}


def test_spectral_isolation_exact_graph():
    A,s,t = theta_pole([2,7]); B,_,_ = theta_pole([2,3,7])
    assert not any(ss.is_dyadic(x) for x in all_cycle_lengths(A)|all_cycle_lengths(B))
    m,q = ss.isolated_context_length([2,3,7],3)
    assert q>=8 and m>=1
    AA=add_context(A,s,t,m); BB=add_context(B,s,t,m)
    assert not any(ss.is_dyadic(x) for x in all_cycle_lengths(AA))
    assert q in all_cycle_lengths(BB)
    assert {x for x in all_cycle_lengths(BB) if ss.is_dyadic(x)}=={q}


def test_isolation_random_sets():
    rng=random.Random(20261116)
    for _ in range(60):
        vals=set(rng.sample(range(1,80), rng.randint(1,12)))
        selected=rng.choice(list(vals))
        m,q=ss.isolated_context_length(vals,selected)
        assert m>=1
        assert {x for x in vals if ss.is_dyadic(x+m+2)}=={selected}
        assert q==m+selected+2


def test_complete_sequence_lemma_exact_subsets():
    rng=random.Random(20261116)
    for _ in range(150):
        size=rng.randint(1,9)
        weights=[rng.randint(1,14) for _ in range(size)]
        step=ss.complete_sequence_step(weights)
        all_sums={0}
        for w in weights:
            all_sums |= {s+w for s in list(all_sums)}
        if step:
            assert all_sums==set(range(0,sum(weights)+1,step))


def test_cubic_scale_switch_witness_graph():
    G,C,sw=ss.make_switch_graph(10, [(0,2,4),(3,5,4),(6,8,4)])
    weights=[len(path)-1-(j-i) for i,j,path in sw]
    assert weights==[2,2,2]
    assert ss.complete_sequence_step(weights)==2
    assert ss.independent_switch_lengths(G,C,sw)=={10,12,14,16}
    q, inds=ss.complete_switch_dyadic_witness(10,weights)
    assert q==16
    assert len(ss.reconstruct_switch_cycle(G,C,sw,inds))==16
    # None of the elementary 2-versus-4 path choices gives a dyadic 6-cycle.
    assert all((j-i)+(len(p)-1)==6 for i,j,p in sw)
    assert 16 in all_cycle_lengths(G)


def test_width_only_fails_even_with_no_local_dyadic_cycles():
    G,C,sw=ss.make_switch_graph(10,[(0,2,4),(4,6,10)])
    weights=[len(path)-1-(j-i) for i,j,path in sw]
    assert weights==[2,8]
    assert ss.complete_sequence_step(weights) is None
    assert ss.independent_switch_lengths(G,C,sw)=={10,12,18,20}
    assert 16 not in ss.independent_switch_lengths(G,C,sw)
    # The whole graph (which has degree-2 vertices) truly has no 4/8/16 cycle.
    assert not any(ss.is_dyadic(x) for x in all_cycle_lengths(G)), all_cycle_lengths(G)


def test_dyadic_witness_condition_is_sufficient():
    for L in range(5,40):
        for weights in [(1,1,1,1,1), (2,2,2,2), (2,4,6), (3,3,6), (1,2,4)]:
            result=ss.complete_switch_dyadic_witness(L,list(weights))
            if result:
                q,indices=result
                assert ss.is_dyadic(q)
                assert q==L+sum(weights[i] for i in indices)


def test_one_sided_switching_gluing_to_single_context_path():
    P,(s,t),records=ss.make_series_switch_pole([2,2,2],[4,4,4],tail_length=1)
    internal={len(c) for c in nx.simple_cycles(P)}
    assert internal=={6}
    lengths=ss.terminal_path_lengths(P,s,t)
    assert lengths=={7,9,11,13}
    # The opposite shore has just one path of length one. Its signature is sparse.
    G=add_context(P,s,t,1)
    assert {length+3 for length in lengths}=={10,12,14,16}
    assert 16 in all_cycle_lengths(G)
    assert ss.complete_switch_dyadic_witness(10,[2,2,2])[0]==16


def test_one_sided_gap_witness_not_forced():
    P,(s,t),records=ss.make_series_switch_pole([2,2],[4,10],tail_length=3)
    assert ss.terminal_path_lengths(P,s,t)=={7,9,15,17}
    assert not any(ss.is_dyadic(x) for x in all_cycle_lengths(P))
    G=add_context(P,s,t,1)
    assert not any(ss.is_dyadic(x) for x in all_cycle_lengths(G))


def test_petersen_two_ear_root_avoidance_certificate():
    G=nx.petersen_graph()
    C=[0,1,2,3,8,5]
    ears=[(0,1,[0,4,9,6,1]),(2,5,[2,7,5])]
    lengths=[len(ss.reconstruct_switch_cycle(G,C,ears,choose))
             for choose in [(),(0,),(1,),(0,1)]]
    assert lengths==[6,9,5,8]
    witness=ss.reconstruct_switch_cycle(G,C,ears,(0,1))
    assert witness==[0,4,9,6,1,2,7,5]
    assert 3 not in witness
    assert 8 in all_cycle_lengths(G)


def test_residue_obstruction_despite_large_dense_progression():
    # Every generated length is divisible by 3; no power of two is.
    for n in (2, 4, 8, 20):
        assert ss.complete_sequence_step([3]*n)==3
        assert ss.complete_switch_dyadic_witness(6,[3]*n) is None


def test_rooted_switch_polynomial_petersen_and_independent_cycle_enumeration():
    G=nx.petersen_graph()
    C=[0,1,2,3,8,5]
    ears=[(0,1,[0,4,9,6,1]),(2,5,[2,7,5])]
    assert ss.switching_length_polynomial(6,[3,-1])=={5:1,6:1,8:1,9:1}
    assert ss.rooted_switch_length_polynomial(C,ears,3)=={5:1,8:1}
    assert ss.rooted_switch_length_polynomial(C,ears,0)=={}
    assert ss.rooted_switch_length_polynomial(C,ears,7)=={6:1,9:1}
    for root in G:
        oracle={}
        for mask in range(4):
            selected=[i for i in range(2) if mask&(1<<i)]
            cycle=ss.reconstruct_switch_cycle(G,C,ears,selected)
            if root not in cycle:
                oracle[len(cycle)]=oracle.get(len(cycle),0)+1
        assert ss.rooted_switch_length_polynomial(C,ears,root)==oracle


def test_petersen_falsifies_universal_complete_pair_requirement():
    # Exhaust strictly disjoint external ear pairs over every oriented cycle
    # and all rotations. This does NOT rule out signed subset-sum repair;
    # the explicit root-avoiding +3,-1 witness above demonstrates it.
    from itertools import combinations
    G=nx.petersen_graph()
    inspected=0
    complete=0
    for core in nx.simple_cycles(G):
        for orientation in (core,list(reversed(core))):
            for offset in range(len(orientation)):
                C=orientation[offset:]+orientation[:offset]
                verts=set(C)
                ears=[]
                for i in range(len(C)):
                    for j in range(i+1,len(C)):
                        H=G.subgraph((set(G)-verts)|{C[i],C[j]})
                        for path in nx.all_simple_paths(H,C[i],C[j]):
                            if len(path)==2 and (j==i+1 or (i==0 and j==len(C)-1)):
                                continue
                            ears.append((i,j,path))
                for a,b in combinations(ears,2):
                    i,j,p=a
                    k,l,q=b
                    if set(range(i,j+1))&set(range(k,l+1)):
                        continue
                    if set(p[1:-1])&set(q[1:-1]):
                        continue
                    d1=len(p)-1-(j-i)
                    d2=len(q)-1-(l-k)
                    if not d1 or not d2:
                        continue
                    inspected+=1
                    if ss.complete_sequence_step([abs(d1),abs(d2)]) is not None:
                        complete+=1
    assert inspected>100
    assert complete==0
