from src.formula import Atom, And
from src.kripke import KripkeStructure, World


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
    expected = 's', Atom('p'), [('s', Atom('q'))]
    result = f.derive('s')
    assert result == expected


def test_derive_and_three_args():
    f = And(Atom('r'), And(Atom('p'), Atom('q')))

    _, formula_one, children_one = f.derive('s')
    world_name, formula_two, children_two = formula_one.derive('s')
    children_two.append(children_one)
    assert world_name == 's'
    assert formula_one == Atom('r')
    assert children_two[0][0][1] == And(Atom('p'), Atom('q'))
