from mlsolver.formula import *
from mlsolver.kripke import *
from mlsolver.tableau import ProofTree


def test_check_semantic_formula():
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
    assert formula.semantic(ks, '1') is True


def test_tableau_calculus():
    formula = Or(And(Box(Atom('p')), Atom('r')), And(Atom('r'), Diamond(Atom('q'))))
    pt = ProofTree(formula)
    pt.derive()

    print()
    print(pt)
    assert formula.semantic(pt.kripke_structure, 's') is True
