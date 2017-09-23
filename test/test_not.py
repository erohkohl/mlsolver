from mlsolver.formula import Atom, Not
from mlsolver.kripke import KripkeStructure, World


def test_semantic_not_q():
    worlds = [
        World('1', {'q': False})
    ]
    relations = {('1', '2'), ('1', '3')}
    ks = KripkeStructure(worlds, relations)
    mpl = Not(Atom('q'))
    assert True == mpl.semantic(ks, '1')
