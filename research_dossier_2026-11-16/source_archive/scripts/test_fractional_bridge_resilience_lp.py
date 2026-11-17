"""Optional LP checks of the exact primal/dual structural formulation."""
import pytest
pytest.importorskip('scipy.optimize')

from fractions import Fraction
import networkx as nx

from bridge_reduction import add_edge_bridge
from bridge_family_robustness import cubic_ladder
from fractional_bridge_resilience_lp import solve_fractional_resilience


@pytest.mark.parametrize('name,G,value', [
    ('K4', nx.complete_graph(4), Fraction(0)),
    ('prism6', nx.circular_ladder_graph(3), Fraction(1,4)),
    ('Q8', cubic_ladder(4), Fraction(3,4)),
    ('V8', cubic_ladder(4,mobius=True), Fraction(1,2)),
    ('Petersen', nx.petersen_graph(), Fraction(3,16)),
    ('Q10', cubic_ladder(5), Fraction(3,4)),
    ('V10', cubic_ladder(5,mobius=True), Fraction(3,4)),
    ('Q12', cubic_ladder(6), Fraction(1)),
])
def test_primal_dual_rho(name, G, value):
    result = solve_fractional_resilience(G)
    assert abs(result.resilience - float(value)) < 1e-7, name
    assert abs(result.dual_resilience - float(value)) < 1e-7, name


def test_resilience_not_monotone_but_cannot_drop_by_more_than_one():
    G = cubic_ladder(4)
    B,_,_ = add_edge_bridge(G,(0,1),(2,6))
    a=solve_fractional_resilience(G)
    b=solve_fractional_resilience(B)
    assert abs(a.resilience-0.75)<1e-7
    assert abs(b.resilience-0.5)<1e-7
    assert b.resilience < a.resilience
    assert b.resilience >= a.resilience-1-1e-9


def test_3connected_nonprime_bridge_can_lose_positivity():
    G = nx.circular_ladder_graph(3)
    H,_,_ = add_edge_bridge(G,(0,1),(2,5))
    assert abs(solve_fractional_resilience(G).resilience-0.25)<1e-7
    assert solve_fractional_resilience(H).resilience < 1e-8
