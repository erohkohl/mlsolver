import pytest

from src.formula.mlp import Atom, Box, Diamond
from src.kripke.structure import KripkeStructure, World


def test_atom_init():
    atom = Atom('p')
    assert atom.name == 'p'


def test_kripke_structure_init():
    worlds = [World('1', {('p', True)})]
    relations = {}
    ks = KripkeStructure(worlds, relations)

    assert ks.relations == {}
    assert ks.worlds[0].name == '1'
    assert ks.worlds[0].assignment == {('p', True)}


def test_ks_wrong_type():
    with pytest.raises(TypeError):
        KripkeStructure([1], [])
    assert True


def test_ks_one_world():
    worlds = [World('1', {('p', True)})]
    relations = {}
    ks = KripkeStructure(worlds, relations)
    atom = Atom('p')
    assert True == atom.semantic(ks, '1')


def test_semantic_box_p_one_world_true():
    worlds = [World('1', {('p', True)})]
    relations = {}
    ks = KripkeStructure(worlds, relations)
    mpl = Box(
        Atom('p')
    )
    assert True == mpl.semantic(ks, '1')


def test_semantic_box_p_one_world_false():
    worlds = [World('1', {('p', False)})]
    relations = {}
    ks = KripkeStructure(worlds, relations)
    mpl = Box(
        Atom('p')
    )
    assert True == mpl.semantic(ks, '1')


def test_semantic_box_p_one_world_reflex_edge_true():
    worlds = [World('1', {('p', True)})]
    relations = {('1', '1')}
    ks = KripkeStructure(worlds, relations)
    mpl = Box(
        Atom('p')
    )
    assert True == mpl.semantic(ks, '1')


def test_semantic_box_p_one_world_reflex_edge_false():
    worlds = [World('1', {('p', False)})]
    relations = {('1', '1')}
    ks = KripkeStructure(worlds, relations)
    mpl = Box(
        Atom('p')
    )
    assert False == mpl.semantic(ks, '1')


def test_semantic_box_p_two_worlds_true():
    worlds = [
        World('1', {('p', False)}),
        World('2', {('p', True)})
    ]
    relations = {('1', '2')}
    ks = KripkeStructure(worlds, relations)
    mpl = Box(
        Atom('p')
    )
    assert True == mpl.semantic(ks, '1')


def test_semantic_box_p_two_worlds_false():
    worlds = [
        World('1', {('p', False)}),
        World('2', {('p', False)})
    ]
    relations = {('1', '2')}
    ks = KripkeStructure(worlds, relations)
    mpl = Box(
        Atom('p')
    )
    assert False == mpl.semantic(ks, '1')


def test_semantic_box_p_three_worlds_true():
    worlds = [
        World('1', {('p', False)}),
        World('2', {('p', True)}),
        World('3', {('p', True)}),
    ]
    relations = {('1', '2'), ('1', '3')}
    ks = KripkeStructure(worlds, relations)
    mpl = Box(
        Atom('p')
    )
    assert True == mpl.semantic(ks, '1')


def test_semantic_box_p_three_worlds_false():
    worlds = [
        World('1', {('p', False)}),
        World('2', {('p', True)}),
        World('3', {('p', False)}),
    ]
    relations = {('1', '2'), ('1', '3')}
    ks = KripkeStructure(worlds, relations)
    mpl = Box(
        Atom('p')
    )
    assert False == mpl.semantic(ks, '1')


def test_semantic_diamond_p_one_world_true():
    worlds = [World('1', {('p', True)})]
    relations = {}
    ks = KripkeStructure(worlds, relations)
    mpl = Diamond(
        Atom('p')
    )
    assert False == mpl.semantic(ks, '1')


def test_semantic_diamond_p_one_world_false():
    worlds = [World('1', {('p', False)})]
    relations = {}
    ks = KripkeStructure(worlds, relations)
    mpl = Diamond(
        Atom('p')
    )
    assert False == mpl.semantic(ks, '1')


def test_semantic_diamond_p_one_world_reflex_edge_true():
    worlds = [World('1', {('p', True)})]
    relations = {('1', '1')}
    ks = KripkeStructure(worlds, relations)
    mpl = Diamond(
        Atom('p')
    )
    assert True == mpl.semantic(ks, '1')


def test_semantic_diamond_p_one_world_reflex_edge_false():
    worlds = [World('1', {('p', False)})]
    relations = {('1', '1')}
    ks = KripkeStructure(worlds, relations)
    mpl = Diamond(
        Atom('p')
    )
    assert False == mpl.semantic(ks, '1')


def test_semantic_diamond_p_two_worlds_true():
    worlds = [
        World('1', {('p', False)}),
        World('2', {('p', True)})
    ]
    relations = {('1', '2')}
    ks = KripkeStructure(worlds, relations)
    mpl = Diamond(
        Atom('p')
    )
    assert True == mpl.semantic(ks, '1')


def test_semantic_diamond_p_two_worlds_false():
    worlds = [
        World('1', {('p', False)}),
        World('2', {('p', False)})
    ]
    relations = {('1', '2')}
    ks = KripkeStructure(worlds, relations)
    mpl = Diamond(
        Atom('p')
    )
    assert False == mpl.semantic(ks, '1')


def test_semantic_diamond_p_three_worlds_true():
    worlds = [
        World('1', {('p', False)}),
        World('2', {('p', True)}),
        World('3', {('p', True)}),
    ]
    relations = {('1', '2'), ('1', '3')}
    ks = KripkeStructure(worlds, relations)
    mpl = Diamond(
        Atom('p')
    )
    assert True == mpl.semantic(ks, '1')


def test_semantic_diamond_p_three_worlds_false():
    worlds = [
        World('1', {('p', False)}),
        World('2', {('p', True)}),
        World('3', {('p', False)}),
    ]
    relations = {('1', '2'), ('1', '3')}
    ks = KripkeStructure(worlds, relations)
    mpl = Diamond(
        Atom('p')
    )
    assert True == mpl.semantic(ks, '1')