from src.tableau import *
from src.formula import *


def test_derive_p_or_q_and_not_p_implies_q():
    f = And(Or(Atom('p'), Atom('q'))
            , Not(Implies(Atom('p'), Atom('q'))))
    tree = ProofTree(f)
    tree.derive()

    print()
    print(tree.root_node)