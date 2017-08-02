from src.kripke import KripkeStructure, World
from src.formula import Atom, Or


# Class models the Kripke structure of the "Three wise men example."
class WiseMenWithHat():
    ks = ()

    def __init__(self):
        worlds = [
            World('RWW', {'1:R': True, '2:W': True, '3:W': True}),
            World('RRW', {'1:R': True, '2:R': True, '3:W': True}),
            World('RRR', {'1:R': True, '2:R': True, '3:R': True}),
            World('WRR', {'1:W': True, '2:R': True, '3:R': True}),

            World('WWR', {'1:W': True, '2:W': True, '3:R': True}),
            World('RWR', {'1:R': True, '2:W': True, '3:R': True}),
            World('WRW', {'1:W': True, '2:R': True, '3:W': True}),
            World('WWW', {'1:W': True, '2:W': True, '3:W': True}),
        ]

        relations = {
            '1': {('RWW', 'WWW'), ('RRW', 'WRW'), ('RWR', 'WWR'), ('WRR', 'RRR')},
            '2': {('RWR', 'RRR'), ('RWW', 'RRW'), ('WRR', 'WWR'), ('WWW', 'WRW')},
            '3': {('WWR', 'WWW'), ('RRR', 'RRW'), ('RWW', 'RWR'), ('WRW', 'WRR')}
        }

        relations.update(add_reflexive_edges(worlds, relations))
        relations.update(add_symmetric_edges(relations))

        self.ks = KripkeStructure(worlds, relations)

        # Wise man ONE does not know color of his hat
        self.announcement_one = Or(Atom('2:R'), Atom('3:R'))

        # Wise man TWO does not know color of his hat
        self.announcement_two = Or(Atom('1:R'), Atom('3:R'))

        # Third wise man knows color of his hat
        self.announcement_three = Atom('3:R')


# Routine adds symmetric edges to Kripke frame
def add_symmetric_edges(relations):
    result = {}
    for agent, agents_relations in relations.items():
        result_agents = agents_relations.copy()
        for r in agents_relations:
            x, y = r[1], r[0]
            result_agents.add((x, y))
        result[agent] = result_agents
    return result


# Routine adds reflexive edges to Kripke frame
def add_reflexive_edges(worlds, relations):
    result = {}
    for agent, agents_relations in relations.items():
        result_agents = agents_relations.copy()
        for world in worlds:
            result_agents.add((world.name, world.name))
            result[agent] = result_agents
    return result


# Returns a list with all worlds of Kripke structure, where formula is not satisfiable
def nodes_not_follow_formula(formula, ks):
    nodes_not_follow_formula = []
    for nodes in ks.worlds:
        if not formula.semantic(ks, nodes.name):
            nodes_not_follow_formula.append(nodes.name)
    return nodes_not_follow_formula
