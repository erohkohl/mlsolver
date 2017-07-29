from src.formula.atom import Atom
from src.kripke.structure import KripkeStructure, World


def is_formula_in_world_sat(ks, world_to_test, atom):
    if not isinstance(ks, KripkeStructure):
        raise TypeError
    if not isinstance(atom, Atom):
        raise TypeError

    # check whether world_to_test is just String and not type World, because we want to address one world in our KS
    if isinstance(world_to_test, World):
        raise TypeError

        # for world in ks.worlds:
        #  if world == world_to_test:
        #     ks.assignments.
