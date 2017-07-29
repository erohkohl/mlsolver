import pytest

from src.formula.atom import Atom
from src.kripke.structure import KripkeStructure, World
from src.semantic import solver as Solver


def test_atom_init():
    atom = Atom("p");
    assert atom.name == "p"


def test_kripke_structure_init():
    worlds = [World("1", {("p", True)})]
    relations = {}
    ks = KripkeStructure(worlds, relations)

    assert ks.relations == {}
    assert ks.worlds[0].name == "1"
    assert ks.worlds[0].assignment == {("p", True)}

def test_ks_wrong_type():
    with pytest.raises(TypeError):
        KripkeStructure([1], [])
    assert True

def test_solver_wrong_type():
    with pytest.raises(TypeError):
        Solver.is_formula_in_world_sat([], "1", Atom("p"))
    assert True

    worlds = [World("1", {("p", True)})]
    relations = {}
    ks = KripkeStructure(worlds, relations)
    with pytest.raises(TypeError):
        Solver.is_formula_in_world_sat(ks, "1", [])
    assert True


"""
def test_ks_one_world():
    worlds = [World("1", {("p", True)})]
    relations = {}
    ks = KripkeStructure(worlds, relations)
    atom = Atom("p");
    assert True == Solver.is_formula_in_world_sat(ks, "1", atom)
"""