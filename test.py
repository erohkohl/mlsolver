from src.formula.atom import Atom
from src.kripke.structure import KripkeStructure


def test_atom_init():
    atom = Atom("p");
    assert atom.name == "p"


def test_kripke_structure_init():
    assign = {("p", True)}
    worlds = {1}
    relations = {}
    ks = KripkeStructure(worlds, relations, assign)
    assert ks.relations == {}
    assert ks.worlds == {1}
    assert ks.assignments == {("p", True)}
