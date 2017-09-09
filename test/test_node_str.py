from src.tableau import *
from src.formula import *


def test_str_p_or_q_and_not_p_implies_q():
    f = And(Or(Atom('p'), Atom('q'))
            , Not(Implies(Atom('p'), Atom('q'))))
    tree = ProofTree(f)
    tree.derive()

    expected_str = '((p or q) and not(p -> q))\n' + \
                   '           |\n' + \
                   '           |\n' + \
                   '       (p or q)\n' + \
   		           '           |\n' + \
                   '           |\n' + \
                   '      not(p -> q)\n' + \
                   '           |\n' + \
                   '           |\n' + \
                   '          / \ \n' + \
                   '         /   \ \n' + \
                   '        p     q\n' + \
                   '        |	  |\n' + \
                   '        |     |\n' + \
                   '        p	  p\n' + \
                   '        |	  |\n' + \
                   '        |     |\n' + \
                   '      not q   not q\n' + \
                   '             _|_\n'

    assert expected_str == str(tree)