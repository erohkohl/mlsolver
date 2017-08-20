from src.tableau import ProofTree, Node
from src.formula import *
from src.kripke import *


def test_derive_first_atom_correct_ks():
    f = Atom('p')
    tree = ProofTree(f)
    ks_expected = KripkeStructure([World('s', {'p': True})], {})
    assert ks_expected == tree.derive()


def test_derive_second_atom_correct_ks():
    f = Atom('q')
    tree = ProofTree(f)
    ks_expected = KripkeStructure([World('s', {'q': True})], {})
    assert ks_expected == tree.derive()


def test_derive_second_atom_correct_tree():
    f = Atom('q')
    tree = ProofTree(f)
    tree_expected = Node('s', Atom('q'), [])
    tree.derive()
    assert tree_expected == tree.root_node


def test_derive_and_two_args_correct_tree():
    f = And(Atom('p'), Atom('q'))
    tree = ProofTree(f)
    tree_expected = Node('s', And(Atom('p'), Atom('q')),
                         [Node('s', Atom('p'),
                               [Node('s', Atom('q'), [])])])
    tree.derive()
    assert tree_expected == tree.root_node


def test_derive_and_two_args_incorrect_tree():
    f = And(Atom('p'), Atom('q'))
    tree = ProofTree(f)
    tree_expected = Node('s', And(Atom('p'), Atom('q')),
                         [Node('s', Atom('p'),
                               [Node('s', Atom('q'), []), Node('s', Atom('p'), [])])])
    tree.derive()
    assert not tree_expected == tree.root_node


def test_derive_and_true_correct_ks():
    f = And(Atom('p'), Atom('q'))
    tree = ProofTree(f)
    ks_expected = KripkeStructure([World('s', {'q': True, 'p': True})], {})
    assert ks_expected == tree.derive()


def test_derive_and_false_correct_ks():
    f = Not(Atom('q'))
    tree = ProofTree(f)
    ks_expected = KripkeStructure([World('s', {'q': False})], {})
    assert ks_expected == tree.derive()


def test_derive_and_false_correct_tree():
    f = Not(Atom('q'))
    tree = ProofTree(f)
    tree_expected = Node('s', Not(Atom('q')), [
        Node('s', Atom('q'), [])])
    tree.derive()
    assert tree_expected == tree.root_node
