from src.tableau import *
from src.formula import *


def test_derive_atom_correct_tree():
    f = Atom('q')
    tree = ProofTree(f)

    tree_expected = Node('s', Atom('q'), [])
    tree_expected.is_derived = True
    tree_expected.assignment = True
    tree.derive()

    assert tree_expected == tree.root_node


def test_derive_and_two_args_correct_tree():
    f = And(Atom('p'), Atom('q'))
    tree = ProofTree(f)

    tree.derive()

    node_three = Node('s', Atom('q'), [])
    node_three.is_derived = True

    node_two = Node('s', Atom('p'), [node_three])
    node_two.is_derived = True

    tree_expected = Node('s', And(Atom('p'), Atom('q')), [node_two])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_derive_not_correct_tree():
    f = Not(Atom('p'))
    tree = ProofTree(f)
    tree.derive()

    tree_expected = Node('s', Atom('p'), [])
    tree_expected.is_derived = True
    tree_expected.assignment = False

    assert tree_expected == tree.root_node


def test_derive_p_and_not_q_correct_tree():
    f = And(Atom('p'), Not(Atom('q')))
    tree = ProofTree(f)
    tree.derive()

    node_three = Node('s', Atom('q'), [])
    node_three.is_derived = True
    node_three.assignment = False

    node_two = Node('s', Atom('p'), [node_three])
    node_two.is_derived = True

    tree_expected = Node('s', And(Atom('p'), Not(Atom('q'))), [node_two])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_derive_p_and_q_and_r_correct_tree():
    f = And(And(Atom('p'), Atom('q')), Atom('r'))
    tree = ProofTree(f)
    tree.derive()

    node_four = Node('s', Atom('p'), [Node('s', Atom('q'), [])])
    node_four.is_derived = True
    node_four.assignment = True
    node_four.children[0].is_derived = True
    node_four.children[0].assignment = True

    node_three = Node('s', Atom('r'), [node_four])
    node_three.is_derived = True
    node_three.assignment = True

    node_two = Node('s', And(Atom('p'), Atom('q')), [node_three])
    node_two.is_derived = True

    tree_expected = Node('s', And(And(Atom('p'), Atom('q')), Atom('r')), [node_two])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node
