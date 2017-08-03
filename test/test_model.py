import src.model as Model
from src.kripke import World, KripkeStructure
from src.formula import And, Atom, Not, Box_a


def test_add_symmetric_edges():
    relations = {'1': {('a', 'b')}}
    expected_realtions = {'1': {('a', 'b'), ('b', 'a')}}
    relations.update(Model.add_symmetric_edges(relations))

    assert expected_realtions == relations


def test_add_symmetric_is_already():
    relations = {'1': {('a', 'b'), ('b', 'a')}}
    expected_realtions = {'1': {('a', 'b'), ('b', 'a')}}
    relations.update(Model.add_symmetric_edges(relations))

    assert expected_realtions == relations


def test_add_reflexive_edges_one_agent():
    worlds = [World('WR', {}), World('RW', {})]
    relations = {'1': {('WR', 'RW')}}
    expected_realtions = {'1': {('WR', 'RW'), ('RW', 'RW'), ('WR', 'WR')}}
    relations = Model.add_reflexive_edges(worlds, relations)

    assert expected_realtions == relations


def test_add_reflexive_edges_two_agents():
    worlds = [World('WR', {}), World('RW', {})]
    relations = {'1': {('WR', 'RW')}, '2': {('RW', 'WR')}}
    expected_realtions = {'1': {('WR', 'RW'), ('WR', 'WR'), ('RW', 'RW')},
                          '2': {('RW', 'WR'), ('RW', 'RW'), ('WR', 'WR')}}
    relations = Model.add_reflexive_edges(worlds, relations)

    assert expected_realtions == relations


def test_nodes_not_follow_formula():
    worlds = [World('RWW', {'1:R': True, '2:W': True, '3:W': True}),
              World('RRW', {'1:R': True, '2:R': True, '3:W': True})]
    relations = {}

    ks = KripkeStructure(worlds, relations)
    formula = And(Atom('2:W'), Atom('3:W'))

    expected_result = ['RRW']
    result = Model.nodes_not_follow_formula(formula, ks)

    assert expected_result == result
