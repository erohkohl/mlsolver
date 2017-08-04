import pytest

from src.kripke import KripkeStructure, World


def test_kripke_structure_init():
    worlds = [World('1', {'p': True})]
    relations = {}
    ks = KripkeStructure(worlds, relations)

    assert ks.relations == {}
    assert ks.worlds[0].name == '1'
    assert ks.worlds[0].assignment == {'p': True}


def test_ks_wrong_type():
    with pytest.raises(TypeError):
        KripkeStructure([1], [])
    assert True


def test_remove_node_trivial_case():
    worlds = [World('1', {'p': True}), World('2', {'p': True})]
    relations = {('1', '2')}
    ks = KripkeStructure(worlds, relations)
    ks_expected = KripkeStructure([World('2', {'p': True})], {})
    ks.remove_node('1')

    assert ks_expected.__eq__(ks)


def test_remove_node_reflexive_edge():
    worlds = [World('1', {'p': True}), World('2', {'p': True})]
    relations = {('1', '2'), ('1', '1'), ('2', '2')}
    ks = KripkeStructure(worlds, relations)
    ks_expected = KripkeStructure([World('2', {'p': True})], {('2', '2')})
    ks.remove_node('1')

    assert ks_expected.__eq__(ks)
