from mlsolver.tableau import *
from mlsolver.formula import *


def test_derive_p_or_q_and_not_p_implies_q():
    f = And(Or(Atom('p'), Atom('q'))
            , Not(Implies(Atom('p'), Atom('q'))))
    tree = ProofTree(f)
    tree.derive()

    print()
    print(tree)


def test_box_p_and_r_or_r_and_diamond_q():
    f = Or(And(Box(Atom('p')), Atom('r')), And(Atom('r'), Diamond(Atom('q'))))
    tree = ProofTree(f)
    tree.derive()

    print()
    print(tree)