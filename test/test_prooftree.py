from src.tableau import *
from src.formula import *


def test_derive_atom():
    f = Atom('q')
    tree = ProofTree(f)
    tree.derive()
    tree_expected = Leaf('s', 'q', [], True)

    assert tree_expected == tree.root_node


def test_derive_and():
    f = And(Atom('p'), Atom('q'))
    tree = ProofTree(f)
    tree.derive()

    node_three = Leaf('s', 'q', [], True)
    node_two = Leaf('s', 'p', [node_three], True)
    tree_expected = Node('s', And(Atom('p'), Atom('q')), [node_two])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_derive_not():
    f = Not(Atom('p'))
    tree = ProofTree(f)
    tree.derive()
    tree_expected = Leaf('s', 'p', [], False)

    assert tree_expected == tree.root_node


def test_derive_p_and_not_q():
    f = And(Atom('p'), Not(Atom('q')))
    tree = ProofTree(f)
    tree.derive()

    node_three = Leaf('s', 'q', [], False)
    node_two = Leaf('s', 'p', [node_three], True)
    tree_expected = Node('s', And(Atom('p'), Not(Atom('q'))), [node_two])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_derive_p_and_q_and_r():
    f = And(And(Atom('p'), Atom('q')), Atom('r'))
    tree = ProofTree(f)
    tree.derive()

    node_four = Leaf('s', 'p', [Leaf('s', 'q', [], True)], True)
    node_three = Leaf('s', 'r', [node_four], True)
    node_two = Node('s', And(Atom('p'), Atom('q')), [node_three])
    node_two.is_derived = True

    tree_expected = Node('s', And(And(Atom('p'), Atom('q')), Atom('r')), [node_two])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_derive_or():
    f = Or(Atom('p'), Atom('q'))
    tree = ProofTree(f)
    tree.derive()

    node_three = Leaf('s', 'q', [], True)
    node_two = Leaf('s', 'p', [], True)
    tree_expected = Node('s', Or(Atom('p'), Atom('q')), [node_two, node_three])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_derive_p_or_not_q():
    f = Or(Atom('p'), Not(Atom('q')))
    tree = ProofTree(f)
    tree.derive()

    node_three = Leaf('s', 'q', [], False)
    node_two = Leaf('s', 'p', [], True)
    tree_expected = Node('s', Or(Atom('p'), Not(Atom('q'))), [node_two, node_three])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_derive_p_or_q_and_r():
    f = And(Or(Atom('p'), Atom('q')), Atom('r'))
    tree = ProofTree(f)
    tree.derive()

    leaf_q = Leaf('s', 'q', [], True)
    leaf_p = Leaf('s', 'p', [], True)
    leaf_r = Leaf('s', 'r', [leaf_p, leaf_q], True)
    node_one = Node('s', Or(Atom('p'), Atom('q')), [leaf_r])
    node_one.is_derived = True
    tree_expected = Node('s', And(Or(Atom('p'), Atom('q')), Atom('r')), [node_one])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_derive_p_implies_q():
    f = Implies(Atom('p'), Atom('q'))
    tree = ProofTree(f)
    tree.derive()

    node_three = Leaf('s', 'q', [], True)
    node_two = Leaf('s', 'p', [], False)
    tree_expected = Node('s', Implies(Atom('p'), Atom('q')), [node_two, node_three])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_derive_not_p_implies_q():
    f = Not(Implies(Atom('p'), Atom('q')))
    tree = ProofTree(f)
    tree.derive()

    node_three = Leaf('s', 'q', [], False)
    node_two = Leaf('s', 'p', [node_three], True)
    tree_expected = Node('s', Not(Implies(Atom('p'), Atom('q'))), [node_two])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_derive_not_not_p():
    f = Not(Not(Atom('p')))
    tree = ProofTree(f)
    tree.derive()

    child_node = Leaf('s', 'p', [], True)
    tree_expected = Node('s', Not(Not(Atom('p'))), [child_node])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_derive_not_not_not_p():
    f = Not(Not(Not(Atom('p'))))
    tree = ProofTree(f)
    tree.derive()

    child_node = Leaf('s', 'p', [], False)
    tree_expected = Node('s', Not(Not(Not(Atom('p')))), [child_node])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_derive_not_p_or_q():
    f = Not(Or(Atom('p'), Atom('q')))
    tree = ProofTree(f)
    tree.derive()

    leaf_q = Leaf('s', 'q', [], False)
    leaf_p = Leaf('s', 'p', [leaf_q], False)
    tree_expected = Node('s', Not(Or(Atom('p'), Atom('q'))), [leaf_p])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_derive_not_p_and_q():
    f = Not(And(Atom('p'), Atom('q')))
    tree = ProofTree(f)
    tree.derive()

    leaf_q = Leaf('s', 'q', [], False)
    leaf_p = Leaf('s', 'p', [], False)
    tree_expected = Node('s', Not(Or(Atom('p'), Atom('q'))), [leaf_p, leaf_q])
    tree_expected.is_derived = True

    assert tree_expected == tree.root_node


def test_derive_not_p_and_q():
    f = And(Or(Atom('p'), Atom('q'))
            , Not(Implies(Atom('p'), Atom('q'))))
    tree = ProofTree(f)
    tree.derive()

    assert False
