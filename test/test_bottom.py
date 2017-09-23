from mlsolver.tableau import *
from mlsolver.formula import *


def test_p_and_not_p_correct_tree():
    f = And(Atom('p'), Not(Atom('p')))
    tree = ProofTree(f)
    tree.derive()

    not_leaf = Leaf('s', 'p', children=Bottom(), assign=False)
    p_leaf = Leaf('s', 'p', [not_leaf], True)
    tree_expected = Node('s', And(Atom('p'), Not(Atom('p'))), [p_leaf])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_p_and_not_p_correct_assign():
    f = And(Atom('p'), Not(Atom('p')))
    tree = ProofTree(f)
    tree.derive()

    expected_assign = {'s': {'p': True}}

    assert expected_assign == tree.root_node.children[0].partial_assign
