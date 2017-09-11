"""Modal logic tableau calculus module

This module contains data structures to store the proof tree of modal logic's
tableau calculus.
"""
import copy
from functools import reduce

from src.formula import *

START_WORLD = 's'


class ProofTree:
    """
    Todo
    """

    def __init__(self, formula):
        self.root_node = create_node(START_WORLD, formula, [])
        self.kripke_structure = None
        self.is_closed = None

    def derive(self):
        """Returns a valid Kripke structures if formula is satisfiable.
        """
        next_node = self.root_node.__next__()

        while next_node is not None:
            leafs = next_node.get_all_leafs()
            for leaf in leafs:
                leaf.add_child(next_node.expand_node())
            next_node.is_derived = True
            next_node = self.root_node.__next__()
        check_conflict(self.root_node)

    def __str__(self):
        return str(self.root_node)


def check_conflict(node):
    """Routine walks through each node and checks whether leafs force
    conflict with partial assignment
    """

    if isinstance(node, Leaf):
        try:
            if not node.partial_assign[node.formula] is node.assign:
                node.children = Bottom()
                return
        except:
            node.partial_assign[node.formula] = node.assign
    for child in node.children:
        child.partial_assign.update(copy.deepcopy(node.partial_assign))
        check_conflict(child)


def create_node(world_name, formula, children):
    """Routine decides whether a node must be a leaf node, when it is not
    derivable further, or a classical node.
    """
    if isinstance(formula, Atom):
        return Leaf(world_name, formula.name, children, True)
    elif isinstance(formula, Not) and isinstance(formula.inner, Atom):
        return Leaf(world_name, formula.inner.name, children, False)
    else:
        return Node(world_name, formula, children)
    return None


class Node:
    """
    Class represents one node of the proof tree. Therefore it holds one
    world name, its children and a modal logic formula. The property is_
    derived is true, when this node was processed by the solver.
    """

    def __init__(self, world_name, formula, children):
        self.world_name = world_name
        self.children = children
        self.formula = formula
        self.is_derived = False
        self.partial_assign = dict()

    def expand_node(self):
        """Contains all rules of tableau calculus and tries to match them to a node
        """
        if isinstance(self.formula, Atom):
            return None

        if isinstance(self.formula, Not):
            formula = self.formula.inner
            if isinstance(formula, Not):
                return create_node(START_WORLD, formula.inner, [])
            if isinstance(formula, Or):
                inner_node = create_node(START_WORLD, Not(formula.right), [])
                return create_node(START_WORLD, Not(formula.left), [inner_node])
            if isinstance(formula, And):
                first_node = create_node(START_WORLD, Not(formula.left), [])
                second_node = create_node(START_WORLD, Not(formula.right), [])
                return [first_node, second_node]
            if isinstance(formula, Implies):
                inner_node = create_node(START_WORLD, Not(formula.right), [])
                return create_node(START_WORLD, formula.left, [inner_node])
            return create_node(START_WORLD, formula, [])

        if isinstance(self.formula, And):
            inner_node = create_node(START_WORLD, self.formula.right, [])
            return create_node(START_WORLD, self.formula.left, [inner_node])

        if isinstance(self.formula, Or):
            first_node = create_node(START_WORLD, self.formula.left, [])
            second_node = create_node(START_WORLD, self.formula.right, [])
            return [first_node, second_node]

        if isinstance(self.formula, Implies):
            first_node = create_node(START_WORLD, Not(self.formula.left), [])
            second_node = create_node(START_WORLD, self.formula.right, [])
            return [first_node, second_node]

        return None

    def add_child(self, node):
        """Routine adds one child node or list of children to the current
         instance.
        """
        if isinstance(node, list):
            for n in node:
                self.children.append(n)
        elif not node is None:
            self.children.append(node)

    def get_all_leafs(self):
        """Returns list of nodes, which each node has no children.
        """
        leafs = []

        if self.children == []:
            leafs.append(self)
        else:
            for child in self.children:
                for child_leafs in child.get_all_leafs():
                    leafs.append(child_leafs)
        return leafs

    def __iter__(self):
        return self

    def __next__(self):
        """Return next node, that is not derived yet in post order sequence
        """
        if self.is_derived is False:
            return self
        if isinstance(self.children, Bottom) or isinstance(self, Bottom):
            return None
        else:
            for child in self.children:
                if not child.is_derived:
                    return child
                else:
                    return child.__next__()
        return None

    def __eq__(self, other):
        are_children_eq = True
        if other is None:
            return False

        if isinstance(self.children, Bottom) or isinstance(other.children, Bottom):
            return self.children == other.children
        elif not len(self.children) == len(other.children):
            return False

        for (self_child, other_child) in zip(self.children, other.children):
            are_children_eq = are_children_eq and self_child == other_child

        return self.world_name == other.world_name \
               and self.is_derived == other.is_derived \
               and self.formula == other.formula \
               and are_children_eq

    def __str__(self):
        bind_string = ""
        children_string = ""

        if isinstance(self.formula, And):
            # members are distributed over .children - get over two for
            bind_string += "\n|\n"
            for child in self.children:
                for childchild in child.children:
                    children_string = child.formula + "\n|\n" + childchild.formula
        elif isinstance(self.formula, Or) or isinstance(self.formula, Implies):
            # all member in self.children existing - reduce to one flat child-string
            bind_string += "\n/ \ \n"
            child_name_list = list(map(lambda c: c.formula, self.children))
            children_string = reduce(lambda x, y: x + ";" + y, child_name_list)

        return str(self.formula) + bind_string + children_string


class Leaf(Node):
    """
    This class does not map a leaf of a tree in sense, that it has no children.
    Moreover this leaf is completely derived, thus it stores only propositional
    variables or their negations.
    """

    def __init__(self, world_name, formula, children, assign):
        super().__init__(world_name, None, children)
        self.formula = formula
        self.assign = assign
        self.is_derived = True

    def __eq__(self, other):
        return super().__eq__(other) \
               and self.is_derived \
               and other.is_derived \
               and self.assign == other.assign \
               and self.formula == other.formula

    def __str__(self):
        return str(self.formula)


class Bottom(Node):
    """
    Marks one branch of proof tree as conflict, therefore an instance of this class
    will be assigned to the children of a Leaf node
    """

    def __init__(self):
        self.is_derived = True
        self.children = None

    def __eq__(self, other):
        try:
            return self.is_derived and other.is_derived \
                   and self.children is None and other.children is None
        except:
            return False

    def __str__(self):
        return "\n|\n__\n"
