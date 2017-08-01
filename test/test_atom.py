from src.formula import Atom, Box, Diamond, Implies, And, Or, Not
from src.kripke import KripkeStructure, World


def test_atom_init():
    atom = Atom('p')
    assert atom.name == 'p'


def test_ks_one_world():
    worlds = [World('1', {'p': True})]
    relations = {}
    ks = KripkeStructure(worlds, relations)
    atom = Atom('p')
    assert True == atom.semantic(ks, '1')
