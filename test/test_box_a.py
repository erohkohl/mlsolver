from mlsolver.formula import Atom, Box_a
from mlsolver.kripke import KripkeStructure, World


def test_semantic_box_a_true():
    worlds = [
        World('1', {'p': False}),
        World('2', {'p': True})
    ]
    relations = {'a': {('1', '2')}}
    ks = KripkeStructure(worlds, relations)
    mpl = Box_a('a', Atom('p'))
    assert True == mpl.semantic(ks, '1')


def test_semantic_box_a_false():
    worlds = [
        World('1', {'p': False}),
        World('2', {'p': False})]

    relations = {'a': {('1', '2')}}
    ks = KripkeStructure(worlds, relations)
    mpl = Box_a('a', Atom('p'))
    assert False == mpl.semantic(ks, '1')


def test_semantic_box_a_two_agents():
    worlds = [
        World('1', {'p': False}),
        World('2', {'p': False})]

    relations = {'a': {('1', '2')}, 'b': {}}
    ks = KripkeStructure(worlds, relations)
    mpl = Box_a('b', Atom('p'))
    assert True == mpl.semantic(ks, '1')
