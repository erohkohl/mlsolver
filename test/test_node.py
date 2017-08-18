from src.tableau import Node
from src.formula import Atom, Not


def test_node_is_eq_trivial_case():
    node_one = Node('s', Atom('p'), [])
    node_two = Node('s', Atom('p'), [])
    assert node_one == node_two


def test_node_not_eq_trivial_case():
    node_one = Node('s', Atom('p'), [])
    node_two = Node('s', Atom('q'), [])
    assert not node_one == node_two


def test_node_is_eq_with_cild():
    node_one = Node('s', Not(Atom('p')), [Node('s', Atom('p'), [])])
    node_two = Node('s', Not(Atom('p')), [Node('s', Atom('p'), [])])
    assert node_one == node_two


def test_node_not_eq_with_cild():
    node_one = Node('s', Not(Atom('p')), [Node('s', Atom('p'), [])])
    node_two = Node('s', Not(Atom('p')), [Node('s', Atom('q'), [])])
    assert not node_one == node_two
