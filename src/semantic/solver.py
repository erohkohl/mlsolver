from src.formula.mlp import Atom, Box
from src.kripke.structure import KripkeStructure, World


def is_formula_in_world_sat(ks, world_to_test, formula):
    if not isinstance(ks, KripkeStructure):
        raise TypeError
    if not isinstance(formula, Atom) and not isinstance(formula, Box):
        raise TypeError

    # check whether world_to_test is just String and not type World, because we want to address one world in our KS
    if isinstance(world_to_test, World):
        raise TypeError

    return formula.semantic(ks, world_to_test)
