from src.tableau import *
from src.formula import *


def test_derive_atom_correct_tree():
    f = Atom('q')
    tree = ProofTree(f)
    tree.derive()
    tree_expected = Leaf('s', 'q', [], True)

    assert tree_expected == tree.root_node


def test_derive_and_two_args_correct_tree():
    f = And(Atom('p'), Atom('q'))
    tree = ProofTree(f)
    tree.derive()

    node_three = Leaf('s', 'q', [], True)
    node_two = Leaf('s', 'p', [node_three], True)
    tree_expected = Node('s', And(Atom('p'), Atom('q')), [node_two])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_derive_not_correct_tree():
    f = Not(Atom('p'))
    tree = ProofTree(f)
    tree.derive()
    tree_expected = Leaf('s', 'p', [], False)

    assert tree_expected == tree.root_node


def test_derive_p_and_not_q_correct_tree():
    f = And(Atom('p'), Not(Atom('q')))
    tree = ProofTree(f)
    tree.derive()

    node_three = Leaf('s', 'q', [], False)
    node_two = Leaf('s', 'p', [node_three], True)
    tree_expected = Node('s', And(Atom('p'), Not(Atom('q'))), [node_two])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_derive_p_and_q_and_r_correct_tree():
    f = And(And(Atom('p'), Atom('q')), Atom('r'))
    tree = ProofTree(f)
    tree.derive()

    node_four = Leaf('s', 'p', [Leaf('s', 'q', [], True)], True)
    node_three = Leaf('s', 'r', [node_four], True)
    node_two = Node('s', And(Atom('p'), Atom('q')), [node_three])
    node_two.is_derived = True

    tree_expected = Node('s', And(And(Atom('p'), Atom('q')), Atom('r')), [node_two])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node
