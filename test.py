import pytest

from src.formula.mlp import Atom, Box
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

    with pytest.raises(TypeError):
        Solver.is_formula_in_world_sat(ks, World("1", {("p", True)}), Atom("p"))
    assert True


def test_ks_one_world():
    worlds = [World("1", {("p", True)})]
    relations = {}
    ks = KripkeStructure(worlds, relations)
    atom = Atom("p");
    assert True == Solver.is_formula_in_world_sat(ks, "1", atom)


def test_semantic_box_p_one_world_true():
    worlds = [World("1", {("p", True)})]
    relations = {}
    ks = KripkeStructure(worlds, relations)
    mpl = Box(
        Atom("p")
    );
    assert True == Solver.is_formula_in_world_sat(ks, "1", mpl)


def test_semantic_box_p_one_world_false():
    worlds = [World("1", {("p", False)})]
    relations = {}
    ks = KripkeStructure(worlds, relations)
    mpl = Box(
        Atom("p")
    );
    assert True == Solver.is_formula_in_world_sat(ks, "1", mpl)


def test_semantic_box_p_one_world_reflex_edge_true():
    worlds = [World("1", {("p", True)})]
    relations = {("1", "1")}
    ks = KripkeStructure(worlds, relations)
    mpl = Box(
        Atom("p")
    );
    assert True == Solver.is_formula_in_world_sat(ks, "1", mpl)


def test_semantic_box_p_one_world_reflex_edge_false():
    worlds = [World("1", {("p", False)})]
    relations = {("1", "1")}
    ks = KripkeStructure(worlds, relations)
    mpl = Box(
        Atom("p")
    );
    assert False == Solver.is_formula_in_world_sat(ks, "1", mpl)


def test_semantic_box_p_two_worlds_true():
    worlds = [
        World("1", {("p", False)}),
        World("2", {("p", True)})
    ]
    relations = {("1", "2")}
    ks = KripkeStructure(worlds, relations)
    mpl = Box(
        Atom("p")
    );
    assert True == Solver.is_formula_in_world_sat(ks, "1", mpl)


def test_semantic_box_p_two_worlds_false():
    worlds = [
        World("1", {("p", False)}),
        World("2", {("p", False)})
    ]
    relations = {("1", "2")}
    ks = KripkeStructure(worlds, relations)
    mpl = Box(
        Atom("p")
    );
    assert False == Solver.is_formula_in_world_sat(ks, "1", mpl)


def test_semantic_box_p_three_worlds_true():
    worlds = [
        World("1", {("p", False)}),
        World("2", {("p", True)}),
        World("3", {("p", True)}),
    ]
    relations = {("1", "2"), ("1", "3")}
    ks = KripkeStructure(worlds, relations)
    mpl = Box(
        Atom("p")
    );
    assert True == Solver.is_formula_in_world_sat(ks, "1", mpl)


def test_semantic_box_p_three_worlds_false():
    worlds = [
        World("1", {("p", False)}),
        World("2", {("p", True)}),
        World("3", {("p", False)}),
    ]
    relations = {("1", "2"), ("1", "3")}
    ks = KripkeStructure(worlds, relations)
    mpl = Box(
        Atom("p")
    );
    assert False == Solver.is_formula_in_world_sat(ks, "1", mpl)
