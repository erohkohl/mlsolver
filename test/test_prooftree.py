from mlsolver.tableau import *
from mlsolver.formula import *
from mlsolver.kripke import *


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


def test_derive_p_or_q_and_not_p_implies_q_correct_tree():
    f = And(Or(Atom('p'), Atom('q'))
            , Not(Implies(Atom('p'), Atom('q'))))
    tree = ProofTree(f)
    tree.derive()

    node_not_q_bottom = Leaf('s', 'q', Bottom(), False)
    node_p_bottom = Leaf('s', 'p', [node_not_q_bottom], True)
    node_right = Leaf('s', 'q', [node_p_bottom], True)

    node_not_q = Leaf('s', 'q', [], False)
    node_p = Leaf('s', 'p', [node_not_q], True)
    node_left = Leaf('s', 'p', [node_p], True)

    node_implies = Node('s', Not(Implies(Atom('p'), Atom('q'))), [node_left, node_right])
    node_implies.is_derived = True
    node_or = Node('s', Or(Atom('p'), Atom('q')), [node_implies])
    node_or.is_derived = True
    node_root = Node('s', And(Or(Atom('p'), Atom('q')),
                              Not(Implies(Atom('p'), Atom('q')))), [node_or])
    node_root.is_derived = True

    assert node_root == tree.root_node


def test_derive_p_or_q_and_not_p_implies_q_correct_ks():
    f = And(Or(Atom('p'), Atom('q'))
            , Not(Implies(Atom('p'), Atom('q'))))
    tree = ProofTree(f)
    tree.derive()

    expected_ks = KripkeStructure([World('s', {'p': True, 'q': False})], set())
    assert expected_ks == tree.kripke_structure


def test_derive_p_or_not_p_check_part_assign():
    f = Or(Atom('p'), Not(Atom('p')))
    tree = ProofTree(f)
    tree.derive()

    child_one = tree.root_node.children[0]
    child_two = tree.root_node.children[1]

    assert child_one.partial_assign['s'] == {'p': True}
    assert child_two.partial_assign['s'] == {'p': False}


def test_derive_p_and_q_or_not_p_check_part_assign():
    f = And(Atom('p'), Or(Atom('q'), Not(Atom('p'))))
    tree = ProofTree(f)
    tree.derive()

    child_one = tree.root_node.children[0]
    child_two = child_one.children[0]
    child_two_q = child_two.children[0]
    child_two_not_p = child_two.children[1]

    assert child_one.partial_assign['s'] == {'p': True}
    assert child_two.partial_assign['s'] == {'p': True}
    assert child_two_q.partial_assign['s'] == {'p': True, 'q': True}
    assert child_two_not_p.partial_assign['s'] == {'p': True}  # Branch contains bottom symbol
    assert isinstance(child_two_not_p.children, Bottom)


def test_not_box_p():
    f = Not(Box(Atom('p')))
    tree = ProofTree(f)
    tree.derive()

    leaf_p = Leaf('t', 'p', [], False)
    child_node = Node('s', Diamond(Not(Atom('p'))), [leaf_p])
    child_node.is_derived = True
    root = Node('s', Not(Box(Atom('p'))), [child_node])
    root.is_derived = True
    assert root == tree.root_node


def test_box_p():
    f = Box(Atom('p'))
    tree = ProofTree(f)
    tree.derive()

    root = Node('s', Box(Atom('p')), [])
    root.is_derived = True
    assert root == tree.root_node


def test_not_diamond_p():
    f = Not(Diamond(Atom('p')))
    tree = ProofTree(f)
    tree.derive()

    child_node = Node('s', Box(Not(Atom('p'))), [])
    child_node.is_derived = True
    root = Node('s', Not(Diamond(Atom('p'))), [child_node])
    root.is_derived = True
    assert root == tree.root_node


def test_diamond_p_correct_tree():
    f = Diamond(Atom('p'))
    tree = ProofTree(f)
    tree.derive()

    leaf_p = Leaf('t', 'p', [], True)
    expected_root = Node('s', Diamond(Atom('p')), [leaf_p])
    expected_root.is_derived = True

    assert expected_root == tree.root_node


def test_diamond_p_correct_ks():
    f = Diamond(Atom('p'))
    tree = ProofTree(f)
    tree.derive()

    worlds = [World('s', {}), World('t', {'p': True}), ]
    expected_ks = KripkeStructure(worlds, {('s', 't')})
    assert expected_ks == tree.kripke_structure


def test_box_p_and_diamond_q():
    f = And(Box(Atom('p')), Diamond(Atom('q')))
    tree = ProofTree(f)
    tree.derive()

    leaf_p = Leaf('t', 'p', [], True)
    leaf_q = Leaf('t', 'q', [leaf_p], True)
    diamond_q = Node('s', Diamond(Atom('q')), [leaf_q])
    diamond_q.is_derived = True
    box_p = Node('s', Box(Atom('p')), [diamond_q])
    box_p.is_derived = True
    root = Node('s', And(Box(Atom('p')), Diamond(Atom('q'))), [box_p])
    root.is_derived = True

    assert root == tree.root_node


def test_box_p_and_r_and_diamond_q_correct_tree():
    f = And(Box(Atom('p')), And(Atom('r'), Diamond(Atom('q'))))
    tree = ProofTree(f)
    tree.derive()

    leaf_p = Leaf('t', 'p', [], True)
    leaf_q = Leaf('t', 'q', [leaf_p], True)

    diamond_q = Node('s', Diamond(Atom('q')), [leaf_q])
    diamond_q.is_derived = True
    leaf_r = Leaf('s', 'r', [diamond_q], True)

    r_and_diamond_q = Node('s', And(Atom('r'), Diamond(Atom('q'))), [leaf_r])
    r_and_diamond_q.is_derived = True

    box_p = Node('s', Box(Atom('p')), [r_and_diamond_q])
    box_p.is_derived = True
    root = Node('s', And(Box(Atom('p')), And(Atom('r'), Diamond(Atom('q')))), [box_p])
    root.is_derived = True

    assert root == tree.root_node


def test_box_p_and_r_and_diamond_q_correct_relations():
    f = And(Box(Atom('p')), And(Atom('r'), Diamond(Atom('q'))))
    tree = ProofTree(f)
    tree.derive()

    test_node = tree.root_node.children[0].children[0].children[0].children[0].children[0]
    assert test_node.relations == {('s', 't')}
    assert test_node.children[0].relations == {('s', 't')}


def test_box_p_and_r_and_diamond_q_correct_ks():
    f = And(Box(Atom('p')), And(Atom('r'), Diamond(Atom('q'))))
    tree = ProofTree(f)
    tree.derive()

    worlds = [World('s', {'r': True}), World('t', {'p': True, 'q': True, })]
    expected_ks = KripkeStructure(worlds, {('s', 't')})
    assert expected_ks == tree.kripke_structure


def test_box_p_or_r_and_diamond_q_correct_tree():
    f = Or(Box(Atom('p')), And(Atom('r'), Diamond(Atom('q'))))
    tree = ProofTree(f)
    tree.derive()

    leaf_q = Leaf('t', 'q', [], True)

    diamond_q = Node('s', Diamond(Atom('q')), [leaf_q])
    diamond_q.is_derived = True
    leaf_r = Leaf('s', 'r', [diamond_q], True)

    r_and_diamond_q = Node('s', And(Atom('r'), Diamond(Atom('q'))), [leaf_r])
    r_and_diamond_q.is_derived = True

    box_p = Node('s', Box(Atom('p')), [])
    box_p.is_derived = True
    root = Node('s', Or(Box(Atom('p')), And(Atom('r'), Diamond(Atom('q')))), [box_p, r_and_diamond_q])
    root.is_derived = True

    assert root == tree.root_node


def test_box_p_or_r_and_diamond_q_correct_relations():
    f = Or(Box(Atom('p')), And(Atom('r'), Diamond(Atom('q'))))
    tree = ProofTree(f)
    tree.derive()

    assert tree.root_node.children[0].relations == set()
    assert tree.root_node.children[1].children[0].children[0].children[0].relations == {('s', 't')}
