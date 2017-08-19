from src.formula import Atom, And
from src.kripke import KripkeStructure, World
from src.tableau import Node


def test_semantic_p_and_q():
    worlds = [
        World('1', {'p': True, 'q': True})
    ]
    relations = {}
    ks = KripkeStructure(worlds, relations)
    mpl = And(Atom('p'), Atom('q'))
    assert True == mpl.semantic(ks, '1')


def test_derive_and_two_args():
    f = And(Atom('p'), Atom('q'))
    expected = Node('s', Atom('p'), [Node('s', Atom('q'))])
    result = f.derive('s')
    assert result == expected


def test_derive_and_three_args():
    f = And(Atom('r'), And(Atom('p'), Atom('q')))
    result_node = f.derive('s')
    expected_node= Node('s', Atom('r'), [Node('s', And(Atom('p'), Atom('q')), [])])
    assert result_node == expected_node
