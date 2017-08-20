from src.formula import Atom, Not
from src.kripke import KripkeStructure, World
from src.tableau import Node


def test_semantic_not_q():
    worlds = [
        World('1', {'q': False})
    ]
    relations = {('1', '2'), ('1', '3')}
    ks = KripkeStructure(worlds, relations)
    mpl = Not(Atom('q'))
    assert True == mpl.semantic(ks, '1')


def test_derive_not():
    f = Not(Atom('p'))
    expected = Node('s', Atom('p'), [])
    result = f.derive('s')
    assert result == expected
