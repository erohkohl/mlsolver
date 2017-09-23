from mlsolver.formula import Box_star, Atom
from mlsolver.kripke import KripkeStructure, World


def test_box_star_empty_relations():
    ks = KripkeStructure([World('1', {'p': True})], {})
    formula = Box_star(Atom('p'))
    assert formula.semantic(ks, '1')


def test_box_star_one_agent():
    ks = KripkeStructure([World('1', {'p': True})], {'a1': {('1', '1')}})
    formula = Box_star(Atom('p'))
    assert formula.semantic(ks, '1')


def test_box_star_two_agents_phi_not_hold():
    ks = KripkeStructure([World('1', {'p': True}), World('2', {'q': True})], {'a1': {('1', '2')}, 'a2': {('1', '2')}})
    formula = Box_star(Atom('q'))
    assert not formula.semantic(ks, '1')


def test_box_star_two_agents_box_phi_hold():
    ks = KripkeStructure([World('1', {'p': True}), World('2', {'p': True})], {'a1': {('1', '2')}, 'a2': {('1', '2')}})
    formula = Box_star(Atom('p'))
    assert formula.semantic(ks, '1')


def test_box_star_two_agents_box_phi_not_hold():
    ks = KripkeStructure([World('1', {'p': True}), World('2', {'p': True}), World('3', {'p': False})],
                         {'agent_1': {('1', '2')}, 'agent_2': {('1', '3'), ('1', '2')}})
    formula = Box_star(Atom('p'))
    assert not formula.semantic(ks, '1')


def test_box_star_three_agents_box_phi_hold():
    ks = KripkeStructure(
        [World('1', {'p': True}), World('2', {'p': True}), World('3', {'p': True}), World('4', {'p': True})],
        {'agent_1': {('1', '2'), ('1', '1')}, 'agent_2': {('1', '3'), ('1', '1')}, 'agent_3': {('1', '4'), ('1', '1')}})
    formula = Box_star(Atom('p'))
    assert formula.semantic(ks, '1')


def test_box_star_three_agents_box_phi_not_hold():
    ks = KripkeStructure(
        [World('1', {'p': True}), World('2', {'p': False}), World('3', {'p': True}), World('4', {'p': True})],
        {'agent_1': {('1', '2'), ('1', '1')}, 'agent_2': {('1', '3'), ('1', '1')}, 'agent_3': {('1', '4'), ('1', '1')}})
    formula = Box_star(Atom('p'))
    assert not formula.semantic(ks, '1')
