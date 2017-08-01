from src.formula import Atom, Box, Diamond, Implies, And, Or, Not
from src.kripke import KripkeStructure, World


def test_semantic_p_and_q():
    worlds = [
        World('1', {('p', True)}),
        World('1', {('q', True)})
    ]
    relations = {('1', '2'), ('1', '3')}
    ks = KripkeStructure(worlds, relations)
    mpl = And(Atom('p'), Atom('q'))
    assert True == mpl.semantic(ks, '1')
