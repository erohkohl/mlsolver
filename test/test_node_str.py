from src.tableau import *


# fixme
def test_str_p_or_q_and_not_p_implies_q():
    f = And(Or(Atom('p'), Atom('q'))
            , Not(Implies(Atom('p'), Atom('q'))))
    tree = ProofTree(f)
    tree.derive()

    expected_str = '((p or q) and not(p -> q))\n' + \
                   '|\n' + \
                   '|\n' + \
                   '(p or q)\n' + \
                   '|\n' + \
                   '|\n' + \
                   'not(p -> q)\n' + \
                   '|\n' + \
                   '/ \ \n' + \
                   'p;q\n' + \
                   '|;|\n' + \
                   'p;p\n' + \
                   '|;|\n' + \
                   'not q;not q\n' + \
                   ';_|_\n'
    assert expected_str == str(tree)


def test_str_or():
    f = Or(Atom('p'), Atom('q'))
    tree = ProofTree(f)
    tree.derive()

    expected_str = '(p or q)\n/ \ \np;q'
    assert expected_str == str(tree)


def test_str_and():
    f = And(Atom('p'), Atom('q'))
    tree = ProofTree(f)
    tree.derive()

    expected_str = '(p and q)\n|\np\n|\nq'
    assert expected_str == str(tree)


# fixme
def test_str_or_and():
    f = And(Or(Atom('p'), Atom('q')), Atom('q'))
    tree = ProofTree(f)
    tree.derive()

    expected_str = '((p or q) and q)\n|\n(p or q)\n|\nq\n/ \ \np;q'
    assert expected_str == str(tree)
