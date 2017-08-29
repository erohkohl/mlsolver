from src.tableau import *
from src.formula import *


def test_derive_atom_correct_tree():
    f = Atom('q')
    tree = ProofTree(f)
    tree_expected = Node('s', Atom('q'), [None])
    tree_expected.is_derived = True
    tree.derive()
    assert tree_expected == tree.root_node


def test_derive_and_two_args_correct_tree():
    f = And(Atom('p'), Atom('q'))
    tree = ProofTree(f)

    tree.derive()
    tree_expected = \
        Node('s', And(Atom('p'), Atom('q')),
             [
                 Node('s', Atom('p'),
                      [
                          Node('s', Atom('q'), [])
                      ]
                      )
             ]
             )
    tree_expected.is_derived = True
    tree_expected.children[0].is_derived = True
    tree_expected.children[0].children[0].is_derived = True
    assert tree_expected == tree.root_node
