from src.tableau import ProofTree
from src.formula import *
from src.kripke import *


def test_derive_first_atom():
    f = Atom('p')
    tree = ProofTree(f)
    ks_expected = KripkeStructure([World('s', {'p': True})], {})
    assert ks_expected == tree.derive()


def test_derive_second_atom():
    f = Atom('q')
    tree = ProofTree(f)
    ks_expected = KripkeStructure([World('s', {'q': True})], {})
    assert ks_expected == tree.derive()


"""
def test_derive_and():
    f = And(Atom('p'), Atom('q'))
    tree = ProofTree(f)
    ks_expected = KripkeStructure([World('s', {'q': True, 'p': True})], {})

    assert ks_expected == tree.derive()
"""
