from mlsolver.formula import Atom
from mlsolver.kripke import KripkeStructure, World


def test_atom_init():
    atom = Atom('p')
    assert atom.name == 'p'


def test_ks_one_world():
    worlds = [World('1', {'p': True})]
    relations = {}
    ks = KripkeStructure(worlds, relations)
    atom = Atom('p')
    assert True == atom.semantic(ks, '1')


def test_atom_is_false_if_q_not_in_V():
    worlds = [World('1', {'p': True})]
    relations = {}
    ks = KripkeStructure(worlds, relations)
    atom = Atom('q')
    assert False == atom.semantic(ks, '1')
