from mlsolver.formula import Atom, Or
from mlsolver.kripke import KripkeStructure, World


def test_semantic_p_or_q():
    worlds = [
        World('1', {'p': True}),
        World('1', {'q': False})
    ]
    relations = {('1', '2'), ('1', '3')}
    ks = KripkeStructure(worlds, relations)
    mpl = Or(Atom('p'), Atom('q'))
    assert True == mpl.semantic(ks, '1')
