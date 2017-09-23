from mlsolver.kripke import World, KripkeStructure
from mlsolver.model import WiseMenWithHat
import mlsolver.model as Model
from mlsolver.formula import Atom, Box, Or, Box_a, And


def test_add_symmetric_edges():
    relations = {'1': {('a', 'b')}}
    expected_relations = {'1': {('a', 'b'), ('b', 'a')}}
    relations.update(Model.add_symmetric_edges(relations))
    assert expected_relations == relations


def test_add_symmetric_is_already():
    relations = {'1': {('a', 'b'), ('b', 'a')}}
    expected_relations = {'1': {('a', 'b'), ('b', 'a')}}
    relations.update(Model.add_symmetric_edges(relations))
    assert expected_relations == relations


def test_add_reflexive_edges_one_agent():
    worlds = [World('WR', {}), World('RW', {})]
    relations = {'1': {('WR', 'RW')}}
    expected_relations = {'1': {('WR', 'RW'), ('RW', 'RW'), ('WR', 'WR')}}
    relations = Model.add_reflexive_edges(worlds, relations)
    assert expected_relations == relations


def test_add_reflexive_edges_two_agents():
    worlds = [World('WR', {}), World('RW', {})]
    relations = {'1': {('WR', 'RW')}, '2': {('RW', 'WR')}}
    expected_relations = {'1': {('WR', 'RW'), ('WR', 'WR'), ('RW', 'RW')},
                          '2': {('RW', 'WR'), ('RW', 'RW'), ('WR', 'WR')}}
    relations = Model.add_reflexive_edges(worlds, relations)
    assert expected_relations == relations


def test_solve_with_model_first_ann():
    wise_men_model = WiseMenWithHat()
    ks = wise_men_model.ks
    model = ks.solve(wise_men_model.knowledge_base[1])

    worlds_expected = [
        World('RRW', {'1:R': True, '2:R': True, '3:W': True}),
        World('RRR', {'1:R': True, '2:R': True, '3:R': True}),
        World('WRR', {'1:W': True, '2:R': True, '3:R': True}),

        World('WWR', {'1:W': True, '2:W': True, '3:R': True}),
        World('RWR', {'1:R': True, '2:W': True, '3:R': True}),
        World('WRW', {'1:W': True, '2:R': True, '3:W': True}),
    ]

    relations_expected = {
        '1': {('RRW', 'WRW'), ('RWR', 'WWR'), ('WRR', 'RRR')},
        '2': {('RWR', 'RRR'), ('WRR', 'WWR')},
        '3': {('RRR', 'RRW'), ('WRW', 'WRR')}
    }

    relations_expected.update(Model.add_reflexive_edges(worlds_expected, relations_expected))
    relations_expected.update(Model.add_symmetric_edges(relations_expected))
    ks_expected = KripkeStructure(worlds_expected, relations_expected)
    assert ks_expected.__eq__(model)


def test_solve_with_model_second_ann():
    wise_men_model = WiseMenWithHat()
    ks = wise_men_model.ks
    model = ks.solve(wise_men_model.knowledge_base[1])
    model = model.solve(wise_men_model.knowledge_base[3])

    worlds_expected = [
        World('RRR', {'1:R': True, '2:R': True, '3:R': True}),
        World('WRR', {'1:W': True, '2:R': True, '3:R': True}),

        World('WWR', {'1:W': True, '2:W': True, '3:R': True}),
        World('RWR', {'1:R': True, '2:W': True, '3:R': True}),
    ]

    relations_expected = {
        '1': {('RWR', 'WWR'), ('WRR', 'RRR')},
        '2': {('RWR', 'RRR'), ('WRR', 'WWR')},
        '3': set()
    }

    relations_expected.update(Model.add_reflexive_edges(worlds_expected, relations_expected))
    relations_expected.update(Model.add_symmetric_edges(relations_expected))
    ks_expected = KripkeStructure(worlds_expected, relations_expected)
    assert ks_expected.__eq__(model)
