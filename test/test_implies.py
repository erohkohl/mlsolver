from mlsolver.formula import Atom, Box, Implies
from mlsolver.kripke import KripkeStructure, World


def test_semantic_box_p_implies_p():
    worlds = [
        World('1', {'p': False}),
        World('2', {'p': True}),
        World('3', {'p': True}),
    ]
    relations = {('1', '2'), ('1', '3')}
    ks = KripkeStructure(worlds, relations)
    mpl = Implies(Box(Atom('p')), Atom('p'))
    assert False == mpl.semantic(ks, '1')
