import pytest

from mlsolver.kripke import KripkeStructure, World
from mlsolver.formula import And, Atom


def test_kripke_structure_init():
    worlds = [World('1', {'p': True})]
    relations = {}
    ks = KripkeStructure(worlds, relations)
    assert ks.relations == {}
    assert ks.worlds[0].name == '1'
    assert ks.worlds[0].assignment == {'p': True}


def test_ks_wrong_type():
    with pytest.raises(TypeError):
        KripkeStructure("p", [])
    assert True


def test_get_power_set_of_worlds():
    worlds = [World('1', {'p': True}), World('2', {'p': True}), World('3', {'p': True})]
    relations = {('1', '2'), ('1', '1'), ('2', '2')}
    ks = KripkeStructure(worlds, relations)
    expected_result = [{}, {'1'}, {'2'}, {'3'}, {'1', '2'}, {'1', '3'}, {'2', '3'}, {'1', '2', '3'}]
    result = ks.get_power_set_of_worlds();
    for i, j in zip(result, expected_result):
        assert i == j


def test_eq_one_agent():
    worlds = [World('1', {'p': True}), World('2', {'p': True})]
    relations = {'a': {('1', '2')}}
    ks = KripkeStructure(worlds, relations)
    ks_expected = KripkeStructure([World('1', {'p': True}), World('2', {'p': True})], {'a': {('1', '2')}})
    assert ks_expected.__eq__(ks)


def test_eq_two_agents():
    worlds = [World('1', {'p': True}), World('2', {'p': True})]
    relations = {'a': {('1', '2')}, 'b': {('2', '2')}}
    ks = KripkeStructure(worlds, relations)
    ks_expected = KripkeStructure([World('1', {'p': True}), World('2', {'p': True})],
                                  {'a': {('1', '2')}, 'b': {('2', '2')}})
    assert ks_expected.__eq__(ks)


def test_eq_two_agents_not_eq():
    worlds = [World('1', {'p': True}), World('2', {'p': True})]
    relations = {'a': {('1', '2')}, 'b': {('2', '1')}}
    ks = KripkeStructure(worlds, relations)
    ks_expected = KripkeStructure([World('1', {'p': True}), World('2', {'p': True})],
                                  {'a': {('1', '2')}, 'b': {('2', '2')}})
    assert not ks_expected.__eq__(ks)


def test_eq_empty_set():
    ks_one = KripkeStructure([World('2', {'p': True})], {'a': set()})
    ks_two = KripkeStructure([World('2', {'p': True})], {'a': set()})
    assert ks_one.__eq__(ks_two)


def test_eq_empty_one_empty_world():
    ks_one = KripkeStructure([World('s', {'p': True})], {})
    ks_two = KripkeStructure([], {})
    assert not ks_one == ks_two


def test_remove_node_trivial_case():
    worlds = [World('1', {'p': True}), World('2', {'p': True})]
    relations = {('1', '2')}
    ks = KripkeStructure(worlds, relations)
    ks_expected = KripkeStructure([World('2', {'p': True})], {})
    ks.remove_node_by_name('1')
    assert ks_expected.__eq__(ks)


def test_remove_node_one_agent():
    worlds = [World('1', {'p': True}), World('2', {'p': True})]
    relations = {'a': {('1', '2')}}
    ks = KripkeStructure(worlds, relations)
    ks_expected = KripkeStructure([World('2', {'p': True})], {'a': set()})
    ks.remove_node_by_name('1')
    assert ks_expected.__eq__(ks)


def test_remove_node_trivial_case_two_agent():
    worlds = [World('1', {'p': True}), World('2', {'p': True})]
    relations = {'a': {('1', '2')}, 'b': {('2', '2')}}
    ks = KripkeStructure(worlds, relations)
    ks_expected = KripkeStructure([World('2', {'p': True})], {'b': {('2', '2')}})
    ks.remove_node_by_name('1')
    assert ks_expected.__eq__(ks)


def test_remove_node_reflexive_edge():
    worlds = [World('1', {'p': True}), World('2', {'p': True})]
    relations = {('1', '2'), ('1', '1'), ('2', '2')}
    ks = KripkeStructure(worlds, relations)
    ks_expected = KripkeStructure([World('2', {'p': True})], {('2', '2')})
    ks.remove_node_by_name('1')
    assert ks_expected.__eq__(ks)


def test_nodes_not_follow_formula():
    worlds = [World('RWW', {'1:R': True, '2:W': True, '3:W': True}),
              World('RRW', {'1:R': True, '2:R': True, '3:W': True})]
    relations = {}
    ks = KripkeStructure(worlds, relations)
    formula = And(Atom('2:W'), Atom('3:W'))
    expected_result = ['RRW']
    result = ks.nodes_not_follow_formula(formula)
    assert expected_result == result
