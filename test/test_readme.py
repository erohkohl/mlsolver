from src.kripke import KripkeStructure, World
from src.formula import *


def test_example_for_readme():
    worlds = [
        World('1', {'p': True, 'q': True}),
        World('2', {'p': True}),
        World('3', {'q': True})
    ]

    relations = {('1', '2'), ('2', '1'), ('1', '3'), ('3', '3')}
    ks = KripkeStructure(worlds, relations)

    formula = Implies(
        Diamond(Atom('p')),
        And(
            Box(Box(Atom('q'))),
            Diamond(Atom('q'))
        )
    )
    assert True == formula.semantic(ks, '1')
